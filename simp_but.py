import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button connected to GPIO17
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button connected to GPIO27
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button connected to GPIO22

def button_callback(channel):
    print(f"Button on GPIO {channel} pressed!")

# Add event detection to each button
GPIO.add_event_detect(17, GPIO.FALLING, callback=button_callback, bouncetime=200)  # Bouncetime in milliseconds
GPIO.add_event_detect(27, GPIO.FALLING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(22, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    message = input("Press any button or type 'exit' to quit\n")
    while message.lower().strip() != 'exit':
        message = input()
finally:
    GPIO.cleanup()  # Clean up GPIO assignments

