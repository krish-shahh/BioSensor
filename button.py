import RPi.GPIO as GPIO
import time

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Increase button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Decrease button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Confirm button
GPIO.setup(25, GPIO.OUT)  # Servo motor
GPIO.setup(23, GPIO.OUT)  # Buzzer

servo_pwm = GPIO.PWM(25, 50)  # Initialize PWM on GPIO25 at 50Hz
buzzer_pwm = GPIO.PWM(23, 400)  # Initialize PWM on GPIO23 at 400Hz

servo_pwm.start(0)
buzzer_pwm.start(0)

def set_servo_angle(angle):
    duty = angle / 18 + 2
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    servo_pwm.ChangeDutyCycle(0)

def buzzer_on():
    buzzer_pwm.ChangeDutyCycle(50)  # 50% duty cycle for buzzer

def buzzer_off():
    buzzer_pwm.ChangeDutyCycle(0)

try:
    while True:
        if GPIO.input(17) == GPIO.HIGH:  # Check if increase button is pressed
            print("Increase button pressed")
            set_servo_angle(90)  # Set servo to 90 degrees
            time.sleep(0.3)  # Debouncing delay

        if GPIO.input(27) == GPIO.HIGH:  # Check if decrease button is pressed
            print("Decrease button pressed")
            set_servo_angle(0)  # Reset servo to 0 degrees
            time.sleep(0.3)  # Debouncing delay

        if GPIO.input(22) == GPIO.HIGH:  # Check if confirm button is pressed
            print("Confirm button pressed")
            buzzer_on()
            time.sleep(1)  # Keep buzzer on for 1 second
            buzzer_off()
            time.sleep(0.3)  # Debouncing delay

        time.sleep(0.1)  # Short delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program stopped")

finally:
    servo_pwm.stop()
    buzzer_pwm.stop()
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
