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
    screen.bgcolor("black")  # Set background to black for better visibility
    screen.title("Congratulations!")
    screen.tracer(0)  # Turn off automatic updates for manual control

    # Create confetti turtles
    confetti = []
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "gold", "silver"]
    shapes = ["circle", "square", "triangle"]

    for _ in range(150):  # More pieces of confetti for a fuller effect
        t = turtle.Turtle()
        t.shape(random.choice(shapes))
        t.shapesize(random.uniform(0.1, 0.8))  # Random size of confetti
        t.color(random.choice(colors))
        t.penup()
        t.speed(0)
        t.goto(random.randint(-screen.window_width()//2, screen.window_width()//2),
               random.randint(-screen.window_height()//2, screen.window_height()//2))
        t.setheading(random.randint(0, 360))
        confetti.append(t)

    # Animate confetti
    for _ in range(50):  # Controls the duration of the animation
        for t in confetti:
            t.right(random.randint(-20, 20))  # Rotate randomly
            t.forward(random.randint(10, 20))  # Move to simulate falling
        screen.update()  # Update the animation frame manually
        time.sleep(0.05)  # Control the speed of the animation

    time.sleep(2)  # Keep the window open for 2 seconds after the animation
    screen.clearscreen()
    screen.bye()  # Close the turtle graphics window

# Other functions and Tkinter setup remain the same...

# Start the Tkinter event loop
root.mainloop()
