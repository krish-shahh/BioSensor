import RPi.GPIO as GPIO
import time

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

servo_pwm = GPIO.PWM(25, 50)
buzzer_pwm = GPIO.PWM(23, 400)
servo_pwm.start(0)
buzzer_pwm.start(0)

button_states = {17: False, 27: False, 22: False}

def check_button(pin):
    current_state = GPIO.input(pin) == GPIO.LOW
    if current_state and not button_states[pin]:
        button_states[pin] = True
        return True
    elif not current_state:
        button_states[pin] = False
    return False

try:
    while True:
        if check_button(17):
            print("Increase button pressed")
            servo_pwm.ChangeDutyCycle(7.5)  # 90 degrees
            time.sleep(0.5)
            servo_pwm.ChangeDutyCycle(0)
        if check_button(27):
            print("Decrease button pressed")
            servo_pwm.ChangeDutyCycle(2.5)  # 0 degrees
            time.sleep(0.5)
            servo_pwm.ChangeDutyCycle(0)
        if check_button(22):
            print("Confirm button pressed")
            buzzer_pwm.ChangeDutyCycle(50)
            time.sleep(1)
            buzzer_pwm.ChangeDutyCycle(0)
        time.sleep(0.01)  # Reduce CPU usage
finally:
    servo_pwm.stop()
    buzzer_pwm.stop()
    GPIO.cleanup()
