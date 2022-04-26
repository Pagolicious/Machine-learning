from threading import Timer
from tkinter import *
import tkinter as tk

root = Tk()
root.geometry('300x300')

v = tk.IntVar()

radiobutton2 = Radiobutton(root, variable=v, value=0, text='Scale')
radiobutton1 = Radiobutton(root, variable=v, value=1, text='Crop')

radiobutton2.pack()
radiobutton1.pack()

def hello():
    print(v.get())

t = Timer(5.0, hello)
t.start()

root.mainloop()
