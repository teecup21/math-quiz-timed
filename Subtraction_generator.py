import random
from inputimeout import inputimeout, TimeoutOccurred
import time
def generate_exp():  # Generate the math problem and the answer
    left = random.randint(2, 40)
    right = random.randint(2, 40)
    expr = f"{left} - {right}"
    answer = left - right
    return expr, answer

def generate_fake_answers(answer):
    fake_answers = []
    while len(fake_answers) < 3:
        fake_answer = answer + random.randint(-5, 5)
        if fake_answer != answer and fake_answer not in fake_answers:
            fake_answers.append(fake_answer)
    return fake_answers

def assign_choices(answer):
    options = ['a', 'b', 'c', 'd']
    numbers = generate_fake_answers(answer) + [answer]  # Include the correct answer
    random.shuffle(numbers)  # Shuffle the numbers

    # Create a dictionary of assignments
    assignments = {option: number for option, number in zip(options, numbers)}

    # Determine the correct choice
    correct_choice = [option for option, number in assignments.items() if number == answer][0]

    return assignments, correct_choice

def present_problem(start_time, z):
    global time_up
    print("\nWhat is the answer to the following problem?")
    expr, answer = generate_exp()  # Call generate_exp() once and store the result
    print(f"{expr} = ?")  # Print the problem
    assignments, correct_choice = assign_choices(answer)  # Assign choices

    # Print the choices
    for letter, number in assignments.items():
        print(f"{letter}. {number}")

    try:
        # Get user input with a timeout
        user_choice = inputimeout(prompt="Enter your choice (a, b, c, or d): ", timeout=z - (time.time() - start_time)).strip().lower()
    except TimeoutOccurred:
        return

    # Check if the user's choice is correct
    if user_choice == correct_choice:
        print("Correct! 🎉")
    else:
        print(f"Wrong! The correct answer is {correct_choice}. 😢")