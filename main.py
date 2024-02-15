from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

WHITE = "white"


def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for char in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for char in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for char in range(random.randint(2, 4))]
    random.shuffle(password_list)

    password = ''.join(password_list)

    entry_3.delete(0, END)
    entry_3.insert(0, password)
    pyperclip.copy(password)



def save():
    website = entry_1.get()
    email = entry_2.get()
    password = entry_3.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                entry_1.delete(0, END)
                entry_3.delete(0, END)


def search():
    try:
        with open("data.json", "r") as data_file:
            loaded_data = json.load(data_file)
            if entry_1.get() in loaded_data:
                messagebox.showinfo(title="Found password", message=f"Website: {entry_1.get()}"
                                                                    f"\nEmail: {loaded_data[entry_1.get()]['email']}"
                                                                    f"\nPassword: {loaded_data[entry_1.get()]['password']}")
            else:
                messagebox.showinfo(title="Not found", message=f"No details for {entry_1.get()} exists."
                                                               f" Check your spelling or add a password.")
    except FileNotFoundError:
        messagebox.showinfo(title="No file found", message="No data file found.")


# UI


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)
# image
display_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, background=WHITE, highlightthickness=0)
canvas.grid(row=0, column=1)
canvas.create_image(100, 100, image=display_image)
# labels
label_1 = Label(text="Website:", bg=WHITE)
label_1.grid(column=0, row=1)

label_2 = Label(text="Email/Username:", bg=WHITE)
label_2.grid(column=0, row=2)

label_3 = Label(text="Password:", bg=WHITE)
label_3.grid(column=0, row=3)

# entries
entry_1 = Entry(width=33, bg="lightgray")
entry_1.grid(row=1, column=1)
entry_1.focus()

entry_2 = Entry(width=52, bg="lightgray")
entry_2.grid(row=2, column=1, columnspan=2)
entry_2.insert(0, "example@gmail.com")

entry_3 = Entry(width=33, bg="lightgray")
entry_3.grid(row=3, column=1)

# buttons
button_gen = Button(text="Generate Password", border=0, width=15, command=pass_gen)
button_gen.grid(column=2, row=3)

button_search = Button(text="Search", border=0, width=15, command=search)
button_search.grid(column=2, row=1)

button_add = Button(text="Add", width=30, border=0, command=save)
button_add.grid(row=4, column=1, columnspan=2, pady=5)

window.mainloop()
