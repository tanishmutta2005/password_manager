from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project


def generate_password():
    pass_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(3, 5))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(1, 2))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(1, 3))]
    password_list = password_symbols + password_letters + password_numbers

    # Above is list comprehension
    """for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)"""

    random.shuffle(password_list)
    password = "".join(password_list)
    pass_input.insert(0, password)
    pyperclip.copy(password)
    # print(f"Your password is: {password}")


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search():
    web = web_input.get()
    if len(web) == 0:
        messagebox.showerror(title="Empty Field", message="Please enter the field")
    else:
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError as fnt:
            messagebox.showerror(title=f"{fnt}", message="File doesn't exists.")
        except JSONDecodeError:
            messagebox.showerror(title="File Empty", message=f"The file {data_file} is empty.")
        else:
            if web in data:
                email = data[web]['email']
                password = data[web]['password']
                messagebox.showinfo(title=f"{web}", message=f"'email/username: {email}'\n'password:' {password}")
            else:
                messagebox.showerror(title="Error", message=f"No data found for {web}.")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    web = web_input.get()
    user = user_input.get()
    password = pass_input.get()
    # save_format = f"{web} | {user} | {password}\n"
    new_data = {
        web: {
            "email": user,
            "password": password,
        }
    }
    if len(user) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops!", message="Please make sure all fields are filled.")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                # reading old data
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            # updating the new data -> (old + add new)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
                # writing the new data (old +new)
        finally:
            web_input.delete(0, END)
            pass_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
img = PhotoImage(file="my_logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

# Labels
website = Label(text="Website:")
website.grid(row=1, column=0)
username_label = Label(text="Username/E-mail:")
username_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
web_input = Entry(width=32)
web_input.grid(row=1, column=1, columnspan=1)
web_input.focus()
user_input = Entry(width=50)
user_input.grid(row=2, column=1, columnspan=2)
user_input.insert(0, "@gmail.com")
pass_input = Entry(width=32)
pass_input.grid(row=3, column=1)

# Buttons
generate = Button(text="Generate Password", command=generate_password)
generate.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search = Button(text="Search", width=14, command=search)
search.grid(row=1, column=2)

window.mainloop()
