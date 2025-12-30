import csv
import customtkinter as ctk
import subprocess
import tkinter as tk
import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Relative paths for assets
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')
IMAGES_DIR = os.path.join(RESOURCES_DIR, 'images')
FONTS_DIR = os.path.join(RESOURCES_DIR, 'fonts')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')
VIDEOS_DIR = os.path.join(RESOURCES_DIR, 'videos')
# Dynamic path for Tesseract (finds it in system PATH)
TESSERACT_PATH = shutil.which('tesseract')
if not TESSERACT_PATH:
    TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def signup():
    username = name.get()
    password = passw.get()
    
    if username and password:
        users_file = os.path.join(DATA_DIR, 'users.csv')
        if not os.path.exists(users_file):
            # No users yet
            pass
        else:
            with open(users_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 1 and row[0] == username:
                        status.configure(text="Username already exists. Please choose another.", text_color="red", height=50, width=200, font=("Arial", 20))
                        return

        with open(users_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
        status.configure(text="Signup successful!", text_color="green",height=50,width=200,font=("Arial", 20))
    else:
        status.configure(text="Please fill in all fields.", text_color="red",height=50,width=200,font=("Arial", 20))

def login():
    username = name.get()
    password = passw.get()
    
    if username=="" or password=="":
        status.configure(text="ENTER ALL THE VALUES.", text_color="red",height=50,width=200,font=("Arial", 20))
    else:
        x=0
        users_file = os.path.join(DATA_DIR, 'users.csv')
        with open(users_file,'r') as loginfile:
            reader=csv.reader(loginfile)
            for row in reader:
                if row[0] == username and row[1] == password:
                    status.configure(text="Logged in successfully!!", text_color="green", height=50, width=200, font=("Arial", 20))
                    braille_script = os.path.join(BASE_DIR, 'braille1.py')
                    subprocess.Popen(['python', braille_script])
                    sys.exit()
            status.configure(text="Wrong credentials, sorry.", text_color="red", height=50, width=200, font=("Arial", 20))

def delete_account():
    username = name.get()
    password = passw.get()
    if not username or not password:
        status.configure(text="Please enter username and password.", text_color="red", height=50, width=200, font=("Arial", 20))
        return

    found = False
    users = []
    users_file = os.path.join(DATA_DIR, 'users.csv')
    if os.path.exists(users_file):
        with open(users_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2 and row[0] == username and row[1] == password:
                    found = True
                    continue  # Skip this user (delete)
                users.append(row)

    if found:
        with open(users_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)
        status.configure(text="Account deleted successfully.", text_color="green", height=50, width=200, font=("Arial", 20))
    else:
        status.configure(text="Account not found or wrong credentials.", text_color="red", height=50, width=200, font=("Arial", 20))

root = ctk.CTk()
root.geometry("1009x565")
root.title("Login to the Braille Network")

Bg = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'Chicagohenge.png'))
background1 = ctk.CTkLabel(root, text="", image=Bg)
background1.configure(width=600,height=600)
background1.pack(pady=0)

namelabel = ctk.CTkLabel(root, text="Username:",height=30,width=100,font=("Arial", 20))
namelabel.place(x=450,y=60)

name = ctk.CTkEntry(root,width=400,height=30)
name.place(x=300,y=110)

passwlabel = ctk.CTkLabel(root, text="Password:",height=30,width=100,font=("Arial", 20))
passwlabel.place(x=450,y=180)
passw = ctk.CTkEntry(root, show="*",width=400,height=30)
passw.place(x=300,y=230)

signUp = ctk.CTkButton(root, text="Sign Up", command=signup)
signUp.place(x=425,y=300)

logIn = ctk.CTkButton(root, text="Login", command=login)
logIn.place(x=425,y=350)

delete = ctk.CTkButton(root, text="Delete Account", command=delete_account)
delete.place(x=425,y=400)

status = ctk.CTkLabel(root, text="")
status.place(x=375,y=50)

def view_all_records():
    def show_records(order="asc"):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, f"{'Email':<30} {'Password':<30}\n")
        text_widget.insert(tk.END, "-"*60 + "\n")
        sorted_records = sorted(records, key=lambda row: row[0], reverse=(order=="desc"))
        for row in sorted_records:
            if len(row) >= 2:
                masked_pw = '*' * len(row[1])
                text_widget.insert(tk.END, f"{row[0]:<30} {masked_pw:<30}\n")
        text_widget.config(state=tk.DISABLED)

    records_popup = ctk.CTkToplevel(root)
    records_popup.geometry("500x450")

    records_popup.title("All User Records")
    records_popup.grab_set()

    users_file = os.path.join(DATA_DIR, 'users.csv')
    with open(users_file, 'r') as file:
        reader = csv.reader(file)
        records = list(reader)

    text_widget = tk.Text(records_popup, width=60, height=20, font=("Arial", 12))
    text_widget.pack(padx=10, pady=10)

    btn_frame = ctk.CTkFrame(records_popup)
    btn_frame.pack(pady=5)

    asc_btn = ctk.CTkButton(btn_frame, text="Ascending", command=lambda: show_records("asc"))
    asc_btn.pack(side=tk.LEFT, padx=10)

    desc_btn = ctk.CTkButton(btn_frame, text="Descending", command=lambda: show_records("desc"))
    desc_btn.pack(side=tk.LEFT, padx=10)

    show_records("asc")

def updtpass():
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x250")
    popup.title("Update Password")
    popup.grab_set()
    Bg = tk.PhotoImage(file=os.path.join(IMAGES_DIR, '20250404.png'))
    background1 = ctk.CTkLabel(popup, text="", image=Bg)
    background1.configure(width=10,height=10)
    background1.pack(pady=0)

    label = ctk.CTkLabel(popup, text="Update Password", font=("Arial", 20))
    label.place(x=100, y=10)

    old_label = ctk.CTkLabel(popup, text="Old Password:", font=("Arial", 16))
    old_label.place(x=30, y=60)
    oldpassentry = ctk.CTkEntry(popup, show="*", width=200, height=30)
    oldpassentry.place(x=160, y=60)


    new_label = ctk.CTkLabel(popup, text="New Password:", font=("Arial", 16))
    new_label.place(x=30, y=110)
    newpassentry = ctk.CTkEntry(popup, show="*", width=200, height=30)
    newpassentry.place(x=160, y=110)

    def update_password_popup():
        username = name.get()
        old_password = oldpassentry.get()
        new_password = newpassentry.get()
        if not username or not old_password or not new_password:
            status.configure(text="Please fill all update fields.", text_color="red", height=50, width=200, font=("Arial", 20))
            return

        updated = False
        users = []

        users_file = os.path.join(DATA_DIR, 'users.csv')
        with open(users_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == old_password:
                    users.append([username, new_password])
                    updated = True
                else:
                    users.append(row)

        if updated:
            with open(users_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(users)
            status.configure(text="Password updated successfully.", text_color="green", height=50, width=200, font=("Arial", 20))
            popup.destroy()
        else:
            status.configure(text="Old password incorrect.", text_color="red", height=50, width=200, font=("Arial", 20))

    update_btn = ctk.CTkButton(popup, text="Update Password", command=update_password_popup)
    update_btn.place(y=175,x=125)

update_popup_btn = ctk.CTkButton(root, text="Update Password", command=updtpass)
update_popup_btn.place(x=425, y=450)

view_btn = ctk.CTkButton(root, text="View All Records", command=view_all_records)
view_btn.place(x=425, y=500)


root.mainloop()