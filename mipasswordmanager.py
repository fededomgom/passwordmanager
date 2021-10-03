import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os
import random
import string
import pyperclip

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("500x500")
        self.master.resizable(False, False)
        self.master.configure(background = "light blue")
        self.master.bind("<Return>", self.add_password)
        self.master.bind("<Delete>", self.delete_password)
        self.master.bind("<Escape>", self.exit_program)
        self.master.bind("<Control-s>", self.save_passwords)
        self.master.bind("<Control-o>", self.load_passwords)
        self.master.bind("<Control-n>", self.new_password_file)
        self.master.bind("<Control-q>", self.exit_program)

        self.password_file = "passwords.pkl"
        self.passwords = {}
        self.load_passwords()

        self.main_frame = tk.Frame(self.master, bg = "light blue")
        self.main_frame.pack(fill = tk.BOTH, expand = True)

        self.password_list_frame = tk.Frame(self.main_frame, bg = "light blue")
        self.password_list_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        self.password_list_label = tk.Label(self.password_list_frame, text = "Passwords", bg = "light blue")
        self.password_list_label.pack(side = tk.TOP, fill = tk.X)

        self.password_list = tk.Listbox(self.password_list_frame, selectmode = "SINGLE", bg = "white", relief = tk.FLAT)
        self.password_list.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.password_list.bind("<<ListboxSelect>>", self.display_password)

        self.password_list_scrollbar = ttk.Scrollbar(self.password_list_frame, orient = tk.VERTICAL, command = self.password_list.yview)
        self.password_list_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.password_list.configure(yscrollcommand = self.password_list_scrollbar.set)

        self.password_entry_frame = tk.Frame(self.main_frame, bg = "light blue")
        self.password_entry_frame.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

        self.password_entry_label = tk.Label(self.password_entry_frame, text = "Password", bg = "light blue")
        self.password_entry_label.pack(side = tk.TOP, fill = tk.X)

        self.password_entry = tk.Entry(self.password_entry_frame, bg = "white", relief = tk.FLAT)
        self.password_entry.pack(side = tk.TOP, fill = tk.X)
        self.password_entry.focus()

        self.password_entry_button_frame = tk.Frame(self.password_entry_frame, bg = "light blue")
        self.password_entry_button_frame.pack(side = tk.BOTTOM, fill = tk.X)

        self.add_password_button = tk.Button(self.password_entry_button_frame, text = "Add Password", command = self.add_password)
        self.add_password_button.pack(side = tk.LEFT)

        self.delete_password_button = tk.Button(self.password_entry_button_frame, text = "Delete Password", command = self.delete_password)
        self.delete_password_button.pack(side = tk.RIGHT)

        self.display_password_frame = tk.Frame(self.main_frame, bg = "light blue")
        self.display_password_frame.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

        self.display_password_label = tk.Label(self.display_password_frame, text = "Password", bg = "light blue")
        self.display_password_label.pack(side = tk.TOP, fill = tk.X)

        self.display_password_entry = tk.Entry(self.display_password_frame, bg = "white", relief = tk.FLAT)
        self.display_password_entry.pack(side = tk.TOP, fill = tk.X)

        self.display_password_button_frame = tk.Frame(self.display_password_frame, bg = "light blue")
        self.display_password_button_frame.pack(side = tk.BOTTOM, fill = tk.X)

        self.copy_password_button = tk.Button(self.display_password_button_frame, text = "Copy Password", command = self.copy_password)
        self.copy_password_button.pack(side = tk.LEFT)

        self.generate_password_button = tk.Button(self.display_password_button_frame, text = "Generate Password", command = self.generate_password)
        self.generate_password_button.pack(side = tk.RIGHT)

    def add_password(self, event = None):
        if self.password_entry.get() != "":
            self.passwords[self.password_entry.get()] = ""
            self.password_list.insert(tk.END, self.password_entry.get())
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
            self.save_passwords()

    def delete_password(self, event = None):
        if self.password_list.curselection() != ():
            self.passwords.pop(self.password_list.get(self.password_list.curselection()))
            self.password_list.delete(self.password_list.curselection())
            self.save_passwords()

    def display_password(self, event = None):
        if self.password_list.curselection() != ():
            self.display_password_entry.delete(0, tk.END)
            self.display_password_entry.insert(0, self.passwords[self.password_list.get(self.password_list.curselection())])
            self.display_password_entry.focus()

    def copy_password(self, event = None):
        if self.display_password_entry.get() != "":
            pyperclip.copy(self.display_password_entry.get())

    def generate_password(self, event = None):
        self.display_password_entry.delete(0, tk.END)
        self.display_password_entry.insert(0, "".join(random.choice(string.ascii_letters + string.digits) for i in range(16)))
        self.display_password_entry.focus()

    def save_passwords(self, event = None):
        with open(self.password_file, "wb") as file:
            pickle.dump(self.passwords, file)

    def load_passwords(self, event = None):
        if os.path.exists(self.password_file):
            with open(self.password_file, "rb") as file:
                self.passwords = pickle.load(file)
            for password in self.passwords:
                self.password_list.insert(tk.END, password)

    def new_password_file(self, event = None):
        if messagebox.askyesno("New Password File", "Are you sure you want to create a new password file? All passwords will be lost."):
            self.passwords = {}
            self.password_list.delete(0, tk.END)
            self.save_passwords()

    def exit_program(self, event = None):
        if messagebox.askyesno("Exit?", "Are you sure you want to exit?"):
            self.master.destroy()

def main():
    root = tk.Tk()
    PasswordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    