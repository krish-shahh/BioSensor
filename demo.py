import pygame
import sys
import RPi.GPIO as GPIO
import time
import random

# Initialize Pygame
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
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
        x = random.randint(0, infoObject.current_w)
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
current_heart_rate = 50  # Start from 50

def simulate_heart_rate():
    global current_heart_rate, confetti_list
    if current_heart_rate < 130:
        current_heart_rate += random.choice([5, 7, 9])
    if current_heart_rate >= 130:
        current_heart_rate = 50  # Reset to 50
    if current_heart_rate >= target_heart_rate and not confetti_list:
        create_confetti()
        pwm.ChangeDutyCycle(12)  # Move servo to indicate success (180 degrees)

def draw_interface():
    screen.fill(background_color)
    hr_text = font.render(f"Current Heart Rate: {current_heart_rate} BPM", True, text_color)
    screen.blit(hr_text, (50, 50))
    for confetto in confetti_list:
        confetto.fall()
        confetto.draw()
    pygame.display.flip()

def main():
    try:
        running = True
        while running:
            simulate_heart_rate()  # Simulate heart rate updates
            check_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            draw_interface()
            pygame.time.wait(100)
    except KeyboardInterrupt:
        pass
    finally:
        pwm.stop()
        GPIO.cleanup()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    print('Starting Heart Rate Monitor Game')
    main()
