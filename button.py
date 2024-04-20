import RPi.GPIO as GPIO
import time

# GPIO Pin Definitions:
button_increase = 17
button_decrease = 27
button_confirm = 22
servo_pin = 25
buzzer_pin = 23

# Setup GPIO:
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(button_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_decrease, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_confirm, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Setup PWM for Servo and Buzzer:
servo = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)
buzzer = GPIO.PWM(buzzer_pin, 400)  # 400 Hz initial frequency
servo.start(0)  # Start PWM with 0% duty cycle (pulse off)
buzzer.start(0)

def set_servo_angle(angle):
    duty_cycle = (angle / 18) + 2
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    servo.ChangeDutyCycle(0)

def buzz_on():
    buzzer.ChangeDutyCycle(50)  # Set duty cycle to 50% for audible volume

def buzz_off():
    buzzer.ChangeDutyCycle(0)  # Turn buzzer off

try:
    while True:
        if GPIO.input(button_increase) == GPIO.LOW:
            print("Increase button pressed")
            set_servo_angle(90)  # Set servo to 90°
        if GPIO.input(button_decrease) == GPIO.LOW:
            print("Decrease button pressed")
            set_servo_angle(0)  # Reset servo to 0°
        if GPIO.input(button_confirm) == GPIO.LOW:
            print("Confirm button pressed")
            buzz_on()
            time.sleep(1)
            buzz_off()

        time.sleep(0.1)  # Delay for button debouncing

except KeyboardInterrupt:
    print("Program stopped")

finally:
    servo.stop()
    buzzer.stop()
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
