import json
import random
from tkinter import *
from tkinter import messagebox

import pyperclip
import requests


class WiseGuru:
    def __init__(self):
        self.quote = ''
        # window
        self.window = Tk()
        self.window.title('Wise Guru')
        self.window.config(bg='#F4F2DE')

        # Canvas
        self.canvas = Canvas(width=400, height=560)
        sadhu_image = PhotoImage(file='sadhu_back1.png')  # 800 * 543
        self.canvas.create_image(200, 280, image=sadhu_image)
        self.canvas.grid(row=0, column=2)
        self.canvas.config(highlightthickness=0, bg='white')

        # Canvas2
        self.quote_canvas = Canvas(width=800, height=100, bg='#FFFEC4')
        self.quote_canvas.grid(row=1, column=2)

        # Label
        self.quote_text = self.quote_canvas.create_text(350, 50, text='', fill='#F11A7B',
                                                        font=('arial', 20, 'bold'), width=700)
        # Next Button
        self.next_button = Button(text='Next From Baba', command=self.new_quote, bg='#F11A7B', fg='white',
                                  font=('arial', 14, 'bold'), padx=10, pady=5, relief=RAISED, bd=3)
        self.next_button.grid(row=2, column=0)

        # Copy Button
        self.copy_button = Button(text='Copy to clipboard', command=self.copy_quote, bg='#F11A7B', fg='white',
                                  font=('arial', 14, 'bold'), padx=10, pady=5, relief=RAISED, bd=3)
        self.copy_button.grid(row=3, column=0)

        # Like Button
        self.like_button = Button(text='Like', command=self.like_quote, bg='#78C1F3', fg='white',
                                  font=('arial', 14, 'bold'), padx=10, pady=5, relief=RAISED, bd=3)
        self.like_button.grid(row=2, column=3)

        # Show Liked Button
        self.show_liked_button = Button(text='Liked Quotes', command=self.show_liked, bg='#78C1F3', fg='white',
                                        font=('arial', 14, 'bold'), padx=10, pady=5, relief=RAISED, bd=3)
        self.show_liked_button.grid(row=3, column=3)
        self.new_quote()  # Display the initial quote
        self.window.mainloop()

    def new_quote(self):
        response = requests.get('https://api.adviceslip.com/advice')
        response.raise_for_status()
        self.quote = response.json()['slip']['advice']
        self.write_quote()

    def write_quote(self):
        self.quote_canvas.itemconfig(self.quote_text, text=self.quote)

    def copy_quote(self):
        pyperclip.copy(self.quote)

    def like_quote(self):
        new_quote = {
            'Quote': self.quote
        }
        try:
            with open(file='quotes.json', mode='r') as quotes_data:
                data = json.load(quotes_data)
        except FileNotFoundError:
            data = {'LikedQuotes': []}

        data['LikedQuotes'].append(new_quote)  # Add the new quote to the list of liked quotes

        with open(file='quotes.json', mode='w') as quotes_data:
            json.dump(data, quotes_data, indent=5)

    def show_liked(self):
        try:
            with open(file='quotes.json', mode='r') as quotes_data:
                data = json.load(quotes_data)
        except FileNotFoundError:
            messagebox.showinfo(title='Create Your Wisdom Library',
                                message="Oops! It looks like you haven't liked any quotes yet.")
        else:
            liked_quotes = data["LikedQuotes"]
            self.quote = "Liked Quote : " + random.choice(liked_quotes)['Quote']
            self.write_quote()


wiseguru = WiseGuru()
