import random
import time
from inputimeout import inputimeout, TimeoutOccurred
import threading
from Subtraction_generator import generate_exp, generate_fake_answers, assign_choices, present_problem
time_up = False  # Global variable to track if time is up
z = int(input("Enter the time limit for the quiz in seconds: "))

def timer(z):
    """Runs a z-second timer in a separate thread."""
    global time_up
    time.sleep(z)
    time_up = True
    print("\n⏳ Time's up! Quiz over. Thanks for playing! 🎉")

# Define z above the timer

# Start the timer thread
timer_thread = threading.Thread(target=timer, args=(z,), daemon=True)
timer_thread.start()

start_time = time.time()
try:
    while not time_up:  # Continue until the global timer is up
        try:
            present_problem(start_time, z)
        except TimeoutOccurred:
            print("\n⏳ Time's up for this question! Moving to the next one.")
except Exception as e:
    print(f"An error occurred: {e}")

# Wait for the timer thread to finish (if needed)
timer_thread.join()
