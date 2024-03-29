from heartrate_monitor import HeartRateMonitor
import threading
import time
from tkinter import Tk, Label, simpledialog

# Function to update the heart rate label in the GUI
def update_heart_rate_label():
    while not stop_event.is_set():
        bpm = hrm.bpm
        if bpm > 0:
            heart_rate_label.config(text=f"Heart Rate: {bpm:.2f} bpm")
            if bpm > target_heart_rate:
                heart_rate_label.config(fg="red")
            else:
                heart_rate_label.config(fg="black")
        else:
            heart_rate_label.config(text="Place your finger on the sensor")
        time.sleep(1)

# Create the main window
root = Tk()
root.withdraw()  # Hide the main window

# Ask the user for their target heart rate
target_heart_rate = simpledialog.askinteger("Target Heart Rate", "Enter your target heart rate (bpm):", parent=root)

root.deiconify()  # Show the main window
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
update_thread.start()

# Function to stop the heart rate monitor and close the window
def on_close():
    stop_event.set()
    update_thread.join()
    hrm.stop_sensor()
    root.destroy()

# Set the on_close function to be called when the window is closed
root.protocol("WM_DELETE_WINDOW", on_close)

# Bind the Escape key to the on_close function
root.bind('<Escape>', lambda e: on_close())

# Start the Tkinter event loop
root.mainloop()
