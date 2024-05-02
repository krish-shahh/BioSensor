import pyrebase
import os
from tkinter import *
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import random

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

        # Check if target heart rate is reached
        if heart_rate >= target_heart_rate[0]:
            duration = (datetime.now() - start_time[0]).total_seconds()
            calories_burned = calculate_calories_burned(duration, heart_rate)
            end_workout(label, heart_rate, duration, calories_burned, main_frame)
            end_screen[0] = True

def end_workout(label, max_heart_rate, duration, calories, main_frame):
    for widget in main_frame.winfo_children():
        widget.pack_forget()  # Temporarily hide widgets without destroying them

    # Create a canvas that fills the entire main frame
    canvas = Canvas(main_frame, bg='white')
    canvas.pack(expand=True, fill=BOTH)

    # Wait until the canvas is mapped (rendered) and then create confetti
    canvas.bind("<Map>", lambda event: create_confetti(canvas))

    # Display the message over the confetti
    message = f"Workout Complete\nMax Heart Rate: {max_heart_rate} bpm\nDuration: {duration:.2f} seconds\nCalories Burned: {calories:.2f} calories"
    end_label = Label(canvas, text=message, font=("Arial", 72), bg='white', fg='black')
    end_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Bind Enter to reset the program
    main_frame.master.bind("<Return>", lambda e: reset_program(main_frame))

def create_confetti(canvas):
    confetti_count = 800
    window_width = canvas.winfo_width()
    window_height = canvas.winfo_height()

    confetti = [
        canvas.create_line(
            random.randint(0, window_width), 0, random.randint(0, window_width), random.randint(10, 30),
            fill=f"#{random.randint(0x100000, 0xFFFFFF):06x}", width=2
        ) for _ in range(confetti_count)
    ]

    def move_confetti():
        for line in confetti:
            canvas.move(line, 0, random.randint(10, 20))
            if canvas.coords(line)[3] > window_height:  # Reset the line if it moves out of view
                x = random.randint(0, window_width)
                canvas.coords(line, x, -10, x, -10 + random.randint(10, 30))
        canvas.after(50, move_confetti)

    move_confetti()

def reset_program(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    main(main_frame)  # Re-initialize the main program within the same frame

def main(main_frame=None):
    global window, ax, ani
    if not main_frame:
        window = Tk()
        window.title("Heart Rate Monitor Simulator")
        window.state('zoomed')
        window.configure(bg='white')
        window.bind("<Escape>", lambda e: window.quit())
        main_frame = Frame(window, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

    target_heart_rate = [100]  # Default target heart rate
    target_heart_rate_label = Label(main_frame, text=f"Target Heart Rate: {target_heart_rate[0]} bpm", font=("Arial", 24), bg='white', fg='black')
    target_heart_rate_label.pack(side=TOP, pady=20)

    heart_rate_label = Label(main_frame, text="Current Heart Rate: -- bpm", font=("Arial", 100, "bold"), bg='white', fg='black')
    heart_rate_label.pack(side=TOP, pady=20)

    fig = Figure(figsize=(4, 10), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=TOP, fill=BOTH, expand=True)

    ys = []
    start_time = [datetime.now()]
    end_screen = [False]
    db = initialize_firebase()
    ani = FuncAnimation(fig, animate, fargs=(ys, heart_rate_label, ax, target_heart_rate, start_time, end_screen, db, main_frame), interval=1000, blit=False)

    window.mainloop()

if __name__ == "__main__":
    main()
