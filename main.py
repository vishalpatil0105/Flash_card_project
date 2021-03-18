import pandas
from tkinter import *
import random

try:
    with open("data/words_to_learn.csv") as data_file:
        words = pandas.read_csv(data_file)
        to_learn = words.to_dict(orient="records")
except FileNotFoundError:
    with open("data/french_words.csv") as data_file:
        words = pandas.read_csv(data_file)
        to_learn = words.to_dict(orient="records")

current_choice = {}


def next_card():
    global current_choice, flip_timer
    window.after_cancel(flip_timer)
    current_choice = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{current_choice['French']}",  fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def remove_word():
    to_learn.remove(current_choice)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv")
    next_card()


def flip_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f"{current_choice['English']}", fill="white")


window = Tk()
window.title("Guess The Word")
window.config(padx=50, pady=50, bg="cyan")
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="French", font=("Ariel", 40))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 40))

canvas.config(bg="cyan", highlightthickness=0)
dont_know_imag = PhotoImage(file="images/wrong.png")
dont_know = Button(image=dont_know_imag, command=next_card)
dont_know.grid(row=1, column=0)
know_image = PhotoImage(file="images/right.png")
know = Button(image=know_image, command=remove_word)
know.grid(row=1, column=1)

next_card()

window.mainloop()
