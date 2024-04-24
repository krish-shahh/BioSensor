import pygame
import sys
import time
import random
import numpy as np
import RPi.GPIO as GPIO  # Import GPIO library for Raspberry Pi

# Initialize GPIO for buttons and outputs
button_increase = 17
button_decrease = 27
button_confirm = 22
servo_pin = 25  # Example servo pin
buzzer_pin = 23  # Example buzzer pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_decrease, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_confirm, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)
servo.start(0)
buzzer = GPIO.PWM(buzzer_pin, 400)  # 400 Hz
buzzer.start(0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Heart Rate Monitor Game")
font_large = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 36)
text_color = (0, 0, 0)
background_color = (255, 255, 255)  # Background color set to white

# Load running images
running_images = []
num_images = 6  # Update this to reflect the number of running images you have
for i in range(num_images):
    img = pygame.image.load(f'running{i}.png')
    img = pygame.transform.scale(img, (50, 50))  # Adjust size if necessary
    running_images.append(img)

# Load trophy image
trophy_image = pygame.image.load('trophy.png')
trophy_image = pygame.transform.scale(trophy_image, (30, 30))

class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size = random.randint(5, 15)

    def fall(self):
        self.y += self.speed
        if self.y > 480:
            self.y = random.randint(-100, 0)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

class Trophy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8

    def fall(self):
        self.y += self.speed
        if self.y > 480:
            self.y = random.randint(-100, 0)

    def draw(self):
        screen.blit(trophy_image, (self.x, self.y))

class Runner:
    def __init__(self):
        self.x = 0  # Start at the leftmost point
        self.y = 480  # Start at the bottom of the screen
        self.step = 10  # Increment for each step to the right
        self.current_frame = 0

    def move(self):
        self.x += self.step
        if self.x >= 640:
            self.x = 0
        self.y = 480 - (self.x * 480 // 640)  # Calculate the y-coordinate for the triangle ascent
        self.current_frame = (self.current_frame + 1) % num_images

    def draw(self):
        screen.blit(running_images[self.current_frame], (self.x, self.y - 50))  # Adjust Y to position runner above ground

# Initialize game variables
target_heart_rate = 100
current_heart_rate = 50
heart_rate_history = []
heart_rate_set = False
target_reached = False
confetti_list = [Confetti(random.randint(0, 640), random.randint(-400, 0)) for _ in range(100)]
trophies = [Trophy(random.randint(0, 640), random.randint(-400, 0)) for _ in range(10)]
runner = Runner()

def activate_hardware():
    """Activate servo and buzzer when the target heart rate is reached."""
    servo.ChangeDutyCycle(7.5)  # Example position for servo
    buzzer.ChangeDutyCycle(50)  # Example duty cycle for buzzer

def deactivate_hardware():
    """Deactivate servo and buzzer."""
    servo.ChangeDutyCycle(0)
    buzzer.ChangeDutyCycle(0)

def draw_interface():
    screen.fill(background_color)
    if not heart_rate_set:
        target_text = font_large.render("Set Target Heart Rate", True, text_color)
        target_rect = target_text.get_rect(center=(320, 100))
        screen.blit(target_text, target_rect)
        hr_text = font_large.render(f"{target_heart_rate} BPM", True, text_color)
        hr_rect = hr_text.get_rect(center=(320, 180))
        screen.blit(hr_text, hr_rect)
    else:
        hr_text = font_small.render(f"Current Heart Rate: {current_heart_rate} BPM", True, text_color)
        hr_rect = hr_text.get_rect(center=(320, 50))
        screen.blit(hr_text, hr_rect)
        # Draw Triangle Path
        pygame.draw.polygon(screen, (200, 200, 200), [(0, 480), (640, 0), (640, 480)])  # Light grey triangle for visual guide
        runner.draw()

    if target_reached:
        for confetti in confetti_list:
            confetti.fall()
            confetti.draw()
        for trophy in trophies:
            trophy.fall()
            trophy.draw()

    pygame.display.flip()

def check_buttons():
    global target_heart_rate, heart_rate_set, target_reached
    if not GPIO.input(button_increase):  # Button pressed
        if not heart_rate_set and target_heart_rate < 180:
            target_heart_rate += 1
        time.sleep(0.2)  # Debounce delay
    elif not GPIO.input(button_decrease):
        if not heart_rate_set and target_heart_rate > 80:
            target_heart_rate -= 1
        time.sleep(0.2)
    elif not GPIO.input(button_confirm):
        if not heart_rate_set:
            heart_rate_set = True
        elif target_reached:
            reset_game()
        time.sleep(0.2)

def reset_game():
    global current_heart_rate, target_heart_rate, heart_rate_set, target_reached, heart_rate_history, confetti_list, trophies, runner
    current_heart_rate = 50
    target_heart_rate = 100
    heart_rate_set = False
    target_reached = False
    heart_rate_history = []
    confetti_list = [Confetti(random.randint(0, 640), random.randint(-400, 0)) for _ in range(100)]
    trophies = [Trophy(random.randint(0, 640), random.randint(-400, 0)) for _ in range(10)]
    runner = Runner()
    deactivate_hardware()

def simulate_heart_rate():
    global current_heart_rate, target_reached
    if heart_rate_set and not target_reached:
        if current_heart_rate < target_heart_rate:
            increment = random.choice([2, 4, 5])
            current_heart_rate += increment
            heart_rate_history.append(current_heart_rate)
            if len(heart_rate_history) > 64:  # keep history size managed
                heart_rate_history.pop(0)
            time.sleep(2)
        if current_heart_rate >= target_heart_rate:
            current_heart_rate = target_heart_rate
            target_reached = True
            activate_hardware()

def main():
    global heart_rate_set
    running = True
    while running:
        check_buttons()
        draw_interface()
        if heart_rate_set:
            simulate_heart_rate()
        runner.move([])
        pygame.time.wait(100)

    GPIO.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    print('Starting Heart Rate Monitor Game')
    main()
