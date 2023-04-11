import tkinter as tk
from tkinter import messagebox
import pandas as pd
import sys
import os
from pygame import mixer


def resource_path(relative_path):
    """Code allows pandas package to be handled by PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


random_country_chosen = None
flag_image_path = None
flag_image = None


def next_flag():
    """Generate random country name"""
    # Build dataframe from country_list.csv"""
    global random_country_chosen, flag_image_path, flag_image
    df = pd.read_csv("country_list.csv")

    # Using sample method from pandas to pick a random row from dataframe
    random_row = df.sample()
    random_country_chosen = random_row["Country"].item()
    print(random_country_chosen)
    flag_image_path = random_row["File_Name"].item()
    flag_image = tk.PhotoImage(file=f"flag_images/{flag_image_path}")
    return flag_image_path, flag_image


score = 0


def submit_answer(event=None):
    """Keeping score, exit option, message box with correct answer"""
    # Using "event=None" as parameter in function to allow for an optional event parameter (default set to "none")
    # when submit button is pressed, submit_answer function does need a parameter (event=None);
    # however, when enter button is pressed (answer.bind("<Return>", submit_answer), submit answer function needs a parameter (event)

    global score, flag_image_path, flag_image, random_country_chosen
    if random_country_chosen == answer.get().title():
        mixer.init()
        sound = mixer.Sound("mixkit-correct-answer-reward-952.wav")
        sound.play()
        score += 1
        score_label.config(text=f"Score: {score}")
    elif answer.get().title() == "Exit":
        window.destroy()
        return
    else:
        messagebox.showinfo(title="Correct Answer:", message=random_country_chosen)

    next_flag()
    canvas.itemconfig(canvas_background, image=flag_image)
    answer.delete(0, tk.END)


# GUI layout
window = tk.Tk()
window.title("Uncle Neenee's World Flags Game")
window.config(padx=30, pady=30, bg="yellow")

next_flag()

canvas = tk.Canvas(width=800, height=450, highlightthickness=0)
canvas_background = canvas.create_image(400, 200, image=flag_image)
canvas.create_text(400, 400, text="Which Country Has This Flag?", font=("Arial", 24, "bold", "italic"))
canvas.pack(pady=10)

answer = tk.Entry(width=30, fg="blue", font=("Arial", 18), borderwidth=4)
answer.bind("<Return>", submit_answer)
answer.pack(pady=10)


score_label = tk.Label(text="Score: ", bg="yellow", font=("Arial", 16, "bold"), )
score_label.pack(pady=10)

submit_button = tk.Button(text="Submit Answer", bg="green", fg="white", font=("Arial", 12, "bold"),
                          borderwidth=2, relief="raised", command=submit_answer)
submit_button.pack(pady=10)

window.mainloop()
