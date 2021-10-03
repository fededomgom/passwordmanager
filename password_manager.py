import sqlite3, hashlib
from tkinter import *

window = Tk()

window.title("Holocrón")

def loginScreen():

    window.geometry("350x150")
    
    label = Label(window, text="Ingresa la contraseña maestra, jóven padawan.")
    label.config(anchor=CENTER)
    label.pack()

    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()

    label1 = Label(window)
    label1.pack()

    def checkPassword():
        password = "test"

        if password == txt.get():
            print("Contraseña correcta.")
        else:
            label1.config(text = "Contraseña incorrecta. No serás un sith, no?")


    button = Button(window, text="Aceptar", command=checkPassword)
    button.pack(pady=5)
def passwordVault():
    for widget in window.winfo_children():
        widget.destroy()

loginScreen()
window.mainloop()