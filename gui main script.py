import time
from inputimeout import inputimeout, TimeoutOccurred
import threading
from Subtraction_generator import generate_exp, generate_fake_answers, assign_choices
import tkinter as tk
from tkinter import messagebox
import pygame
#global variables 
time_up = False
start_time = 0
z=0
#timer function
def timer(z): 
    global time, right_ans
    time.sleep(z)
    time_up=True
    quiz_frame.pack_forget()
    score_label.config(text=f"You got {right_ans} pts!")
    finish_frame.pack()
    stop_music()

def update_timer():
    elapsed_time = time.time() - start_time
    remaining_time =z - elapsed_time
    timer_label.config(text=f"{remaining_time:.0f}s")    
    if remaining_time >0: 
        root.after(1000, update_timer)
def present_problem(): 
    if time_up: 
        return
    expr, answer = generate_exp()
    assignments, correct_choice = assign_choices(answer) #redundant?
    #display the problem
    problem_label.config(text=f"{expr} = ?")
    i=0
    for number in assignments.values():
        choice_buttons[i].config(text=f"{number}", command=lambda number=number: check_answer(number, answer))
        i+=1

    update_timer() #call the update_timer function

right_ans=0
wrong_ans=0
def check_answer(number, answer):
    global right_ans, wrong_ans
    if number == answer:
        correctmusic.play()
        right_ans+=1
        verdict_label.config(text="Correct! 🎉", fg="green")
    else:
        wrongmusic.play()
        verdict_label.config(text=f"😢 Wrong! The answer is {answer}.", fg="red")
        wrong_ans+=1
    present_problem()


def start_quiz():
    global z, start_time, time_up
    try: 
        z=int(duration_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return 
    #hide the start screen to show the quiz 
    start_frame.pack_forget()
    quiz_frame.pack(expand=True, fill=tk.BOTH, pady=100)
    bgmusic()
    #Start timer thread
    start_time=time.time()
    timer_thread=threading.Thread(target=timer, args=(z,), daemon=True)
    timer_thread.start()
    present_problem()

pygame.mixer.init()
#music player 
def bgmusic(): 
    pygame.mixer.music.load("Pixify.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
correctmusic= pygame.mixer.Sound("correct.wav")
wrongmusic=pygame.mixer.Sound("wrong.wav")
def stop_music():
    pygame.mixer.music.stop()

# Create the main window
root = tk.Tk()
root.title("Math Quiz")
root.geometry("1000x800")

# Start screen
start_frame = tk.Frame(root)
start_frame.pack()

duration_label = tk.Label(start_frame, text="Enter the quiz duration in seconds:", font=("Comic Sans MS", 25))
duration_label.pack()

duration_entry = tk.Entry(start_frame, font=("Comic Sans MS", 25))
duration_entry.pack()

start_button = tk.Button(start_frame, text="Start Quiz", command=start_quiz, font=("Comic Sans MS", 25))
start_button.pack()
image = tk.PhotoImage(file="mathclip.png")  # Replace with your image file
image_label = tk.Label(start_frame, image=image)
image_label.pack(pady=20)  # Add padding below the image


# Quiz screen
quiz_frame = tk.Frame(root)
problem_label=tk.Label(quiz_frame, text="", font=("Arial", 27), bg="White")
problem_label.pack()

# Frame to hold buttons (ensures they are in a row)
button_frame = tk.Frame(quiz_frame, pady=20)
button_frame.pack(side=tk.TOP)  # Keep it above the timer label
choice_buttons = []
for i in range(4):
    button = tk.Button(button_frame, text="", font=("Arial", 24))
    button.pack(side=tk.LEFT, expand=True, padx=10)  
    choice_buttons.append(button)
#timer display 
timer_label = tk.Label(quiz_frame, text="", font=("Arial", 16))
timer_label.pack(side=tk.BOTTOM, fill=tk.X,pady=10)
#correct and wrong answer display
verdict_label = tk.Label(quiz_frame, text="", font=("Arial", 24))
verdict_label.pack()

#Finish screen 
finish_frame = tk.Frame(root)
finish_label = tk.Label(finish_frame, text="Quiz Over! Thanks for playing!", font=("Arial", 24))
finish_label.pack()
score_label = tk.Label(finish_frame, text=f"You got {right_ans} pts!", font=("Arial", 24))
score_label.pack()
#run the application
root.mainloop()