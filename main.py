"""
Purpose: This program create a GUI password manager that can generate strong random passwords, store new passwords
in a local JSON file, and search for existing passwords with the same website name.
Tools: Tkinter, JSON, Pyperclip
"""
from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json


#Method to search for an existing password with the website name.
def search():
    try:
        #Open the file and retreive the email and password
        with open("data.json", "r") as file:
            data = json.load(file)
            name = website_box.get()
            data_email = data.get(name).get("email")
            data_password = data.get(name).get("password")
            messagebox.showinfo(title=name, message=f"Email: {data_email}\nPassword: {data_password}")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"No Data File Found")
    except json.decoder.JSONDecodeError:
        messagebox.showinfo(title="Error", message=f"No Data File Found")
    except AttributeError:
        messagebox.showinfo(title="Error", message=f"Password Not Found")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


#Generate a random password with random amount of letters, numbers, and symbols shuffled
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = letter_list + number_list + symbols_list
    shuffle(password_list)
    new_password = "".join(password_list)

    #Copy the password into the field and the clipboard
    password_box.delete(0, END)
    password_box.insert(0, new_password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


#Save the data in JSON format in a local json file
def save_password():
    user_website = website_box.get()
    user_username = email_box.get()
    user_password = password_box.get()
    new_data = {
        user_website: {
            "email": user_username,
            "password": user_password
        }
    }

    if len(user_website) == 0 or len(user_password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        #If user already have the file, update it. If not, create a new file.
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            #Update old file
            data.update(new_data)

            with open("data.json", mode="w") as file:
                # Write updated data
                json.dump(data, file, indent=4)
        #Empty the UI fields
        finally:
            website_box.delete(0, END)
            password_box.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

mypass_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(column=1, row=0)

#Labels
website = Label(text="Website:")
website.grid(column=0, row=1)

email = Label(text="Email/Username:")
email.grid(column=0, row=2)

password = Label(text="Password:")
password.grid(column=0, row=3)

#Entries
website_box = Entry()
website_box.focus()
website_box.grid(column=1, columnspan=2, row=1, sticky="EW")

email_box = Entry()
email_box.insert(0, "@gmail.com")
email_box.grid(column=1, columnspan=2, row=2, sticky="EW")

password_box = Entry()
password_box.grid(column=1, row=3, sticky="EW")

#Buttons
search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, columnspan=2, row=4, sticky="EW")


window.mainloop()