from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- RETRIEVE INFO ------------------------------- #


def search_in_json():
    with open("data.json", 'r') as data_file:
        try:
            data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            data = {}
        if website_input.get().title() in data.keys():
            messagebox.showinfo(title=website_input.get().title(),
                                message=f"Email : {data[website_input.get().title()]['email']}\n"
                                f"Password : {data[website_input.get().title()]['password']}")
            pyperclip.copy(data[website_input.get().title()]['password'])
        elif len(website_input.get()) == 0:
            messagebox.showinfo(message="Please enter a website to search")
        else:
            messagebox.showinfo(message="No such website exists in the database")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_to_file():
    if website_input.get() == "" or email_input.get() == "" or password_input.get() == "":
        messagebox.showerror(message="Please complete all the fields")
    else:
        new_data = {
            website_input.get().title(): {
                "email": email_input.get(),
                "password": password_input.get()
            }
        }
        with open("data.json", "r") as data_file:
            try:
                data = json.load(data_file)
            except json.decoder.JSONDecodeError:
                data = new_data
            else:
                data.update(new_data)
        with open("data.json", "w") as data_file:
            json.dump(data, data_file)
        website_input.delete(0, END)
        email_input.delete(0, END)
        password_input.delete(0, END)
        website_input.focus()
        messagebox.showinfo(message="Info successfully added")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
picture = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=picture)
canvas.grid(column=0, row=0, sticky='e', columnspan=2, padx=20, pady=20)

website_label = Label(text="website", font=("Courier", 20))
website_label.grid(column=0, row=1, sticky='w')

website_input = Entry(width=21)
website_input.grid(column=1, row=1, padx=10, sticky='w')
website_input.focus()

search_button = Button(text="Search", width=16, command=search_in_json)
search_button.grid(column=2, row=1, sticky='w')

email_label = Label(text="Email/Username", font=("Courier", 20))
email_label.grid(column=0, row=2)

email_input = Entry(width=43)
email_input.grid(column=1, row=2, padx=10, columnspan=2, sticky='w')

password_label = Label(text="password", font=("Courier", 20))
password_label.grid(column=0, row=3, sticky='w')

password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky='w', padx=10)

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3, sticky='w')

add_button = Button(text="Add", width=70, command=add_to_file)
add_button.grid(column=0, row=4, columnspan=3, sticky='w')

window.mainloop()
