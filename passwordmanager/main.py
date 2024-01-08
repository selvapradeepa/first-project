

import json
from tkinter import *
from tkinter import messagebox

from random import randint, choice, shuffle

import pyperclip


# ------------------------------PASSWORD GENERATOR-------------------#


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '@', '#', '$', '%', '*', '+']

    letter_list = [choice(letters) for char in range(randint(8, 10))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letter_list + symbol_list + number_list

    shuffle(password_list)
    genpassword = "".join(password_list)
    password_entry.insert(0, genpassword)
    pyperclip.copy(genpassword)


# -------------------------------SAVE PASSWORD-----------------------------#

def save():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="oops", message="please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as file:
                # Saving update data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    website_entry.get()
    try:
        with open("data.json", "r") as file:
            rdata = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in rdata:
            email = rdata[website]["email"]
            password = rdata[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:"
                                                       f"{email}\nPassword:{password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for the {website}exists.")


# --------------------------------UI SETUP---------------------#
window = Tk()
window.title("password manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=243, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

website_entry = Entry()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

website_label = Label(text="website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(row=3, column=2, stick="EW")

add = Button(text="Add", width=36, command=save)
add.grid(row=4, column=1, columnspan=2, sticky="EW")

search = Button(text="Search", width=13, command=find_password)
search.grid(row=1, column=2)

window.mainloop()
