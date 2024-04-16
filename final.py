import paho.mqtt.client as mqtt
import pygame
import sys
import RPi.GPIO as GPIO
import time
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Heart Rate Monitor Game")
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)
background_color = (0, 0, 0)

# Confetti class
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size = random.randint(5, 15)

    def fall(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

confetti_list = []

def create_confetti():
    for _ in range(100):  # Create 100 pieces of confetti
        x = random.randint(0, 600)
        y = random.randint(-400, 0)
        confetti_list.append(Confetti(x, y))

# GPIO setup for buttons and servo
button_increase = 17
button_decrease = 27
button_confirm = 22
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_increase, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_decrease, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_confirm, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # Set PWM to 50Hz
pwm.start(0)

target_heart_rate = 100
current_heart_rate = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/esp8266/health")

def on_message(client, userdata, message):
    global current_heart_rate, confetti_list
    msg = message.payload.decode()
    if "No finger detected" in msg:
        display_message = "No finger detected"
    elif "Avg BPM" in msg:
        current_heart_rate = int(msg.split('=')[-1].split(',')[1].strip().split(' ')[-1])
        if current_heart_rate >= target_heart_rate and not confetti_list:
            create_confetti()
            set_angle(180)  # Move servo to indicate success

def draw_interface():
    screen.fill(background_color)
    if current_heart_rate:
        hr_text = font.render(f"Current Heart Rate: {current_heart_rate} BPM", True, text_color)
        screen.blit(hr_text, (50, 50))
    for confetto in confetti_list:
        confetto.fall()
        confetto.draw()
    pygame.display.flip()

def check_buttons():
    global target_heart_rate
    if GPIO.input(button_increase) == GPIO.HIGH:
        target_heart_rate += 1
        time.sleep(0.3)  # Debounce delay
    elif GPIO.input(button_decrease) == GPIO.HIGH:
        target_heart_rate -= 1
        time.sleep(0.3)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.x.x', 1883)  # MQTT broker IP address
    client.loop_start()

    try:
        running = True
        while running:
            check_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            draw_interface()
            pygame.time.wait(100)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        pwm.stop()
        GPIO.cleanup()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()
