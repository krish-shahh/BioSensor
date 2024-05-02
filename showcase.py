import pyrebase
import os
import RPi.GPIO as GPIO
from tkinter import *
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import random
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Decrease button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Increase button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enter button (Start Monitoring)
GPIO.setup(23, GPIO.OUT)  # Buzzer
GPIO.setup(25, GPIO.OUT)  # Servo
servo = GPIO.PWM(25, 50)  # Set PWM frequency to 50 Hz
servo.start(0)  # Start servo with 0 duty cycle to avoid unnecessary movement at start

def initialize_firebase():
    config = {
        "apiKey": "AIzaSyB3IazSdfYdGKat0oU6Mvtnl42BJ_XWZtU",
        "authDomain": "pulsepro-c9c42.firebaseapp.com",
        "databaseURL": "https://pulsepro-c9c42-default-rtdb.firebaseio.com",
        "storageBucket": "pulsepro-c9c42.appspot.com",
        "serviceAccount": "pulsepro-c9c42-firebase-adminsdk-dgk23-5e786b7921.json"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase.database()

def fetch_data(db):
    user_id = 'J0ZaMMElhpPKr6Uf8kX8wqPh3J83'
    try:
        readings = db.child("UsersData").child(user_id).child("readings").order_by_key().limit_to_last(1).get()
        if readings.each():
            for reading in readings.each():
                return int(reading.val().get('heart'))
    except pyrebase.exceptions.HTTPError as e:
        print(f'Failed to retrieve data: {e}')
        return 60  # Default value or previous value if error occurs

def calculate_calories_burned(duration_in_seconds, average_heart_rate):
    weight_in_kg = 70
    age = 21
    calories_per_minute = ((age * 0.2017) + (weight_in_kg * 0.1988) + (average_heart_rate * 0.6309) - 55.0969) / 4.184
    total_calories = (calories_per_minute * (duration_in_seconds / 60))
    return total_calories

def animate(i, ys, label, ax, target_heart_rate, start_time, end_screen, db, main_frame):
    if not end_screen[0]:
        heart_rate = fetch_data(db)
        ys.append(heart_rate)
        ys = ys[-50:]  # Keep last 50 data points

        label.config(text=f"{heart_rate} bpm")
        
        ax.clear()
        ax.plot(ys, color='red', linewidth=2, linestyle='-')
        ax.set_facecolor('white')
        ax.figure.set_facecolor('white')
        ax.tick_params(colors='black')
        ax.set_title("Real-Time EKG", color='black')
        ax.set_xlabel("Measurements", color='black')
        ax.set_ylabel("Heart Rate (bpm)", color='black')
        ax.grid(True, which='both', linestyle=':', linewidth=0.5, color='gray')

        if heart_rate >= target_heart_rate[0]:
            duration = (datetime.now() - start_time[0]).total_seconds()
            calories_burned = calculate_calories_burned(duration, heart_rate)
            end_workout(label, heart_rate, duration, calories_burned, main_frame)
            end_screen[0] = True

def end_workout(label, max_heart_rate, duration, calories, main_frame):
    GPIO.output(23, True)  # Turn on buzzer
    servo.ChangeDutyCycle(7.5)  # Move servo to 90 degrees
    time.sleep(1)
    GPIO.output(23, False)  # Turn off buzzer
    servo.ChangeDutyCycle(0)  # Stop sending signal to servo to hold position without force

    message = f"Workout Complete\nMax Heart Rate: {max_heart_rate} bpm\nDuration: {duration:.2f} seconds\nCalories Burned: {calories:.2f} calories"
    end_label = Label(main_frame, text=message, font=("Arial", 24), bg='white', fg='black')
    end_label.pack(side=TOP, fill=BOTH, expand=True)

def button_callback(channel):
    global target_heart_rate, setup_label
    if channel == 17:
        target_heart_rate[0] = max(50, target_heart_rate[0] - 1)  # Decrease target HR by 1
        setup_label.config(text=f"Target Heart Rate: {target_heart_rate[0]} bpm")
    elif channel == 22:
        target_heart_rate[0] = min(200, target_heart_rate[0] + 1)  # Increase target HR by 1
        setup_label.config(text=f"Target Heart Rate: {target_heart_rate[0]} bpm")
    elif channel == 27:
        start_monitoring()  # Start monitoring when the enter button is pressed

def start_monitoring():
    global setup_frame, main_frame
    setup_frame.pack_forget()  # Hide the setup frame
    main_frame.pack(fill=BOTH, expand=True)  # Show the main frame

def reset_program():
    global window
    servo.ChangeDutyCycle(2.5)  # Reset servo to initial position
    time.sleep(1)
    servo.ChangeDutyCycle(0)  # Stop sending signal to servo
    window.destroy()  # Close the current window
    main()  # Restart the program

GPIO.add_event_detect(17, GPIO.FALLING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(22, GPIO.FALLING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(27, GPIO.FALLING, callback=button_callback, bouncetime=200)

def main():
    global window, ax, target_heart_rate, setup_frame, main_frame, setup_label
    target_heart_rate = [100]  # Default target heart rate

    window = Tk()
    window.title("Heart Rate Monitor Simulator")
    window.state('zoomed')
    window.configure(bg='white')
    window.bind("<Escape>", lambda e: window.quit())

    # Setup Frame for setting the target heart rate
    setup_frame = Frame(window, bg='white')
    setup_frame.pack(fill=BOTH, expand=True)
    setup_label = Label(setup_frame, text=f"Target Heart Rate: {target_heart_rate[0]} bpm", font=("Arial", 24), bg='white', fg='black')
    setup_label.pack(pady=20)

    # Main Frame for displaying the heart rate and EKG
    main_frame = Frame(window, bg='white')
    heart_rate_label = Label(main_frame, text="Current Heart Rate: -- bpm", font=("Arial", 100, "bold"), bg='white', fg='black')
    heart_rate_label.pack(side=TOP, pady=20)

    fig = Figure(figsize=(4, 10), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    ys = []
    start_time = [datetime.now()]
    end_screen = [False]
    db = initialize_firebase()
    ani = FuncAnimation(fig, animate, fargs=(ys, heart_rate_label, ax, target_heart_rate, start_time, end_screen, db, main_frame), interval=1000, blit=False)

    window.mainloop()

if __name__ == "__main__":
    main()
