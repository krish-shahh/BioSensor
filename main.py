from heartrate_monitor import HeartRateMonitor
import threading
import time
from tkinter import Tk, Label, messagebox
import turtle
import random
import RPi.GPIO as GPIO

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Increase button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Decrease button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enter button

# Function to display confetti
def display_confetti():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Congratulations!")

    # Create confetti turtles
    confetti = []
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    for _ in range(50):
        t = turtle.Turtle()
        t.shape("circle")
        t.color(random.choice(colors))
        t.penup()
        t.speed(0)
        t.goto(random.randint(-200, 200), random.randint(-200, 200))
        confetti.append(t)

    # Animate confetti
    for _ in range(100):
        for t in confetti:
            t.sety(t.ycor() - random.randint(10, 20))
            t.setx(t.xcor() + random.randint(-10, 10))
        screen.update()
        time.sleep(0.1)

    screen.bye()  # Close the turtle graphics window

# Function to update the heart rate label in the GUI
def update_heart_rate_label():
    global target_heart_rate
    while not stop_event.is_set():
        bpm = hrm.bpm
        if bpm > 0:
            heart_rate_label.config(text=f"Heart Rate: {bpm:.2f} bpm")
            if bpm > target_heart_rate:
                heart_rate_label.config(fg="red")
                messagebox.showinfo("Congratulations!", "You've exceeded your target heart rate!")
                display_confetti()
            else:
                heart_rate_label.config(fg="black")
        else:
            heart_rate_label.config(text="Place your finger on the sensor")
        time.sleep(1)

# Function to handle button presses
def handle_buttons():
    global target_heart_rate
    max_heart_rate = 200  # Set the maximum heart rate
    while not stop_event.is_set():
        if GPIO.input(17) == GPIO.LOW:  # Increase button pressed
            target_heart_rate = min(target_heart_rate + 5, max_heart_rate)
            time.sleep(0.3)  # Debounce delay
        elif GPIO.input(27) == GPIO.LOW:  # Decrease button pressed
            target_heart_rate = max(0, target_heart_rate - 5)
            time.sleep(0.3)  # Debounce delay
        elif GPIO.input(22) == GPIO.LOW:  # Enter button pressed
            messagebox.showinfo("Target Heart Rate Set", f"Target heart rate set to {target_heart_rate} bpm")
            time.sleep(0.3)  # Debounce delay
        time.sleep(0.1)

# Initial target heart rate
target_heart_rate = 100

# Create the main window
root = Tk()
root.title("Heart Rate Monitor")

# Create a label to display the heart rate
heart_rate_label = Label(root, text="Place your finger on the sensor", font=("Arial", 20))
heart_rate_label.pack(pady=20)

# Start the heart rate monitor
hrm = HeartRateMonitor(print_raw=False, print_result=False)
hrm.start_sensor()

# Create a stop event for the update thread
stop_event = threading.Event()

# Start a thread to update the heart rate label
update_thread = threading.Thread(target=update_heart_rate_label)
button_thread = threading.Thread(target=handle_buttons)
update_thread.start()
button_thread.start()

# Function to stop the heart rate monitor and close the window
def on_close():
    stop_event.set()
    update_thread.join()
    button_thread.join()
    hrm.stop_sensor()
    GPIO.cleanup()
    root.destroy()

# Set the on_close function to be called when the window is closed
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter event loop
root.mainloop()
