import turtle
import random
import time

def display_confetti():
    screen = turtle.Screen()
    screen.bgcolor("black")  # Set background to black for better visibility
    screen.title("Congratulations!")
    screen.tracer(0)  # Turn off animation updates (for manual update)

    # Create confetti turtles
    confetti = []
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "gold", "silver"]
    shapes = ["circle", "square", "triangle"]

    for _ in range(150):  # Increase number for more confetti
        t = turtle.Turtle()
        t.shape(random.choice(shapes))
        t.shapesize(random.uniform(0.1, 0.8))  # Varying sizes of confetti
        t.color(random.choice(colors))
        t.penup()
        t.speed(0)
        t.goto(random.randint(-screen.window_width()//2, screen.window_width()//2),
               random.randint(-screen.window_height()//2, screen.window_height()//2))
        t.setheading(random.randint(0, 360))  # Random starting angle
        confetti.append(t)

    # Animate confetti
    for _ in range(50):  # Controls the duration of the animation
        for t in confetti:
            t.right(random.randint(-20, 20))  # Randomly rotate confetti
            t.forward(random.randint(10, 20))  # Move forward to simulate falling
        screen.update()  # Update the animation frame
        time.sleep(0.05)  # Control the speed of the animation

    # Wait a moment before clearing the screen
    time.sleep(2)
    screen.clearscreen()
    screen.bye()  # Close the turtle graphics window

display_confetti()
