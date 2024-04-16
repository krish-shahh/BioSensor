import paho.mqtt.client as mqtt
import pygame
import sys
import RPi.GPIO as GPIO
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Heart Rate Monitor Game")
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)
background_color = (0, 0, 0)

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

# Initial target heart rate
target_heart_rate = 100
current_heart_rate = None
display_message = f"Target Heart Rate: {target_heart_rate} BPM"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/esp8266/health")

def on_message(client, userdata, message):
    global current_heart_rate, display_message
    msg = message.payload.decode()
    if "No finger detected" in msg:
        display_message = "No finger detected"
    elif "Avg BPM" in msg:
        current_heart_rate = int(msg.split('=')[-1].split(',')[1].strip().split(' ')[-1])
        display_message = f"Current Heart Rate: {current_heart_rate} BPM"

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def draw_interface():
    screen.fill(background_color)
    hr_text = font.render(display_message, True, text_color)
    target_text = font.render(f"Target Heart Rate: {target_heart_rate} BPM", True, text_color)
    screen.blit(hr_text, (50, 50))
    screen.blit(target_text, (50, 100))
    pygame.display.flip()

def check_buttons():
    global target_heart_rate
    if GPIO.input(button_increase) == GPIO.HIGH:
        target_heart_rate += 1
        time.sleep(0.3)  # Debounce delay
    elif GPIO.input(button_decrease) == GPIO.HIGH:
        target_heart_rate -= 1
        time.sleep(0.3)
    elif GPIO.input(button_confirm) == GPIO.HIGH:
        if current_heart_rate and current_heart_rate >= target_heart_rate:
            set_angle(180)  # Move servo to indicate success
        time.sleep(0.3)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.x.x', 1883)  # Replace with your MQTT broker's IP address
    client.loop_start()

    try:
        running = True
        while running:
            check_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            draw_interface()
            if current_heart_rate and current_heart_rate >= target_heart_rate:
                display_message = "Target achieved! Great job!"
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
    print('Starting Heart Rate Monitor Game')
    main()
