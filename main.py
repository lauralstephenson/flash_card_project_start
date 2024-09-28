from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

#Use pandas as pd to read the csv file with the words
try:
    data = pandas.read_csv(r".\data\words_to_learn.csv")
#If this file does not exist, it should use the words in the french_words.csv
except FileNotFoundError:
    original_data = pandas.read_csv(r".\data\french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

#_____________________FLASHCARD ACTIONS__________________#
#Every time wrong_button or right_button are pressed,
#Get a new random word to display
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    # Pick a random French word from our dataframe
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    # change back to the front image after a flip
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

#Now we need to flip the card on a 3-second delay to show the English language card
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

#_____________________REMOVE KNOWN CARDS__________________#

#If the user presses the right_button, then that word should be
#removed from the dictionary
def is_known():
    #Remove(current_card)
    to_learn.remove(current_card)
    #Save the list to a new dataframe
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

#_______________________USER INTERFACE____________________#
#Opens a window
window = Tk()
window.title("FlashLanguage")
#Padding
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
#Sleep 3000 seconds, then flip card
flip_timer = window.after(3000, func=flip_card)

#Using Canvas to upload a picture, Row 0, Column 1
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file=r".\images\card_front.png")
#Image for the back when flip the card
card_back_img = PhotoImage(file=r".\images\card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0,row=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)

#Language label
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
#Language word
card_word = canvas.create_text(400, 263, text="", font=("Arial", 40, "bold"))

#Buttons
#Wrong Button, 50X padding, center, row 1, column 0, uses pic
photo_wrong = PhotoImage(file=r".\images\wrong.png")
wrong_button = Button(image=photo_wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

#Right Button, 50X padding, center, row 1, column 1, uses pic
photo_right = PhotoImage(file=r".\images\right.png")
right_button = Button(image=photo_right, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

#listens to what user will do
#Goes at the end of the program
window.mainloop()