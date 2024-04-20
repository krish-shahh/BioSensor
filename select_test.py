import RPi.GPIO as GPIO
import time
import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Target Heart Rate Selection")
font = pygame.font.Font(None, 36)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Increase button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Decrease button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Confirm button
GPIO.setup(25, GPIO.OUT)  # Servo pin
GPIO.setup(23, GPIO.OUT)  # Buzzer pin

servo_pwm = GPIO.PWM(25, 50)  # Initialize PWM for the servo
buzzer_pwm = GPIO.PWM(23, 400)  # Initialize PWM for the buzzer
servo_pwm.start(0)
buzzer_pwm.start(0)

# Variables
target_heart_rate = 100  # Initial target heart rate

# Display function
def display_target(rate):
    screen.fill((0, 0, 0))
    target_text = font.render(f"Target Heart Rate: {rate} BPM", True, (255, 255, 255))
    screen.blit(target_text, (50, 50))
    pygame.display.flip()

# Button handling function
def handle_buttons():
    global target_heart_rate
    if GPIO.input(17) == GPIO.LOW:
        target_heart_rate += 1
        time.sleep(0.3)
    elif GPIO.input(27) == GPIO.LOW:
        target_heart_rate -= 1
        time.sleep(0.3)
    elif GPIO.input(22) == GPIO.LOW:
        print("Confirm button pressed")
        time.sleep(0.3)

# Main loop
try:
    running = True
    while running:
        handle_buttons()
        display_target(target_heart_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
finally:
    servo_pwm.stop()
    buzzer_pwm.stop()
    GPIO.cleanup()
    pygame.quit()
    sys.exit()
