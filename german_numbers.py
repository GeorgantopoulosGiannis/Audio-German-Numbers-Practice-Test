import random
from gtts import gTTS
import pygame
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence  # Import ImageSequence for GIF

# Define global variables
correct_count = 0
question_count = 0

def generate_random_number(question_count):
    """Generate a random number based on the number of questions answered."""
    if question_count < 2:
        return random.randint(10, 99)  # Return a 2-digit number for the first 2 questions
    elif question_count < 6:
        return random.randint(100, 999)  # Return a 3-digit number for the next 4 questions
    else:
        return random.randint(1000, 9999)  # Return a 4-digit number for the remaining questions

def say_number_in_german(number, next_button):
    """Convert the number to German speech and play it using gTTS and pygame."""
    tts = gTTS(text=str(number), lang='de')
    tts.save('number.mp3')  # Save the spoken number as an mp3 file
    pygame.mixer.init()  # Initialize pygame mixer
    pygame.mixer.music.load('number.mp3')  # Load the mp3 file
    pygame.mixer.music.play()  # Play the mp3 file
    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():  # Wait until the mp3 file finishes playing
        clock.tick(30)  # Adjust the delay as needed
    pygame.mixer.quit()  # Quit the mixer after playing
    next_button.config(state=tk.NORMAL)  # Enable the "Next" button

def test_listening(number, user_input):
    """Check if the user's input matches the spoken number."""
    return user_input.strip() == str(number)

def on_submit(user_input, random_number, correct_count_var, next_button, window):
    """Handle the submission of the user's input."""
    global correct_count, question_count
    if test_listening(random_number, user_input.get()):
        correct_count += 1  # Increment correct count if the user's input is correct
        messagebox.showinfo("Correct!", "Well done!")  # Show success message
    else:
        messagebox.showerror("Incorrect", f"Sorry, the correct number is {random_number}")  # Show error message
    user_input.set('')  # Clear the entry for the next question
    question_count += 1  # Increment question count

    correct_count_var.set(f"Correct Answers: {correct_count}/{question_count}")  # Update score display

    if question_count == 10:
        show_result(correct_count_var, window)  # Show result after last question
    else:
        on_next(random_number_var, correct_count_var, next_button, window)  # Proceed to next question

def on_next(random_number_var, correct_count_var, next_button, window):
    """Generate and speak the next random number."""
    random_number = generate_random_number(len(random_number_var))
    random_number_var.append(random_number)  # Append the new number to the list
    say_number_in_german(random_number, next_button)  # Say the number in German

def show_result(correct_count_var, window):
    """Display the final result."""
    for widget in window.winfo_children():
        widget.destroy()
    
    result_label = tk.Label(window, text=f"Your final score is {correct_count_var.get()}", bg='lightblue', font=('Arial', 18, 'bold'))
    result_label.pack(pady=20)
    
    restart_button = tk.Button(window, text="Restart Test", command=restart_test, bg='#f44336', fg='white', font=('Arial', 12, 'bold'))
    restart_button.pack(pady=20)

def restart_test():
    """Reset the test to the start screen."""
    global correct_count, question_count
    correct_count = 0
    question_count = 0
    start_game(root)

def start_game(window):
    """Initialize the game, setting up the game frame."""
    global correct_count, question_count
    correct_count = 0
    question_count = 0

    for widget in window.winfo_children():
        widget.destroy()

    window.configure(bg='lightblue')

    game_frame = tk.Frame(window, bg='lightblue', padx=20, pady=20)
    game_frame.pack(fill=tk.BOTH, expand=True)

    # Load and animate GIF
    gif_path = "bar.gif"  # Ensure the GIF is in the same directory as the script
    gif = Image.open(gif_path)
    gif_frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(gif)]

    gif_label = tk.Label(game_frame)
    gif_label.pack()

    def animate(index):
        gif_label.config(image=gif_frames[index])
        index += 1
        if index == len(gif_frames):
            index = 0
        gif_label.after(50, animate, index)

    animate(0)

    random_number_var = []  # List to keep track of the random numbers generated
    next_button = tk.Button(game_frame, text="Play next audio", state=tk.DISABLED, command=lambda: on_next(random_number_var, correct_count_var, next_button, game_frame), bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
    next_button.pack(pady=10)

    user_input = tk.StringVar()
    entry_label = tk.Label(game_frame, text="Enter the number you heard in German:", bg='lightblue', font=('Arial', 14))
    entry_label.pack()
    entry = tk.Entry(game_frame, textvariable=user_input, font=('Arial', 14), width=10)
    entry.pack(pady=5)

    submit_button = tk.Button(game_frame, text="Submit", command=lambda: on_submit(user_input, random_number_var[-1], correct_count_var, next_button, game_frame), bg='#008CBA', fg='white', font=('Arial', 12, 'bold'))
    submit_button.pack(pady=10)

    correct_count_var = tk.StringVar()
    correct_count_var.set(f"Correct Answers: {correct_count}/{question_count+1}")  # Initialize score display
    correct_count_label = tk.Label(game_frame, textvariable=correct_count_var, bg='lightblue', font=('Arial', 14))
    correct_count_label.pack(pady=10)

    restart_button = tk.Button(game_frame, text="Restart Test", command=restart_test, bg='#f44336', fg='white', font=('Arial', 12, 'bold'))
    restart_button.pack(pady=20)

    on_next(random_number_var, correct_count_var, next_button, game_frame)  # Start the quiz by generating the first number

def start_screen(window):
    """Display the start screen."""
    start_frame = tk.Frame(window, bg='white', padx=20, pady=20)
    start_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(start_frame, text="Welcome to the German Numbers Quiz!", bg='white', font=('Arial', 18, 'bold'))
    title_label.pack(pady=20)

    instruction_label = tk.Label(start_frame, text="Press the 'Start' button to begin the quiz.", bg='white', font=('Arial', 14))
    instruction_label.pack(pady=10)

    start_button = tk.Button(start_frame, text="Start", command=lambda: start_game(start_frame), bg='#4CAF50', fg='white', font=('Arial', 14, 'bold'))
    start_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("German Numbers Quiz")
    root.geometry("600x450")  # Set the size of the start window
    root.configure(bg='white')

    start_screen(root)

    root.mainloop()
