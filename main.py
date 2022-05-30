import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from gui_class import SuperResolutionGuiClass


def main():
    # Creating the window object. (Window is the window without any controls)
    # the object uw (uw = user window) will hold all atributes and objects, functions from the class.
    # All stuff we add should go between window = tk.Tk() and window.mainloop()
    # Otherwise it won't show up in the window.
    window = tk.Tk()

    # Creating the user window object that holds all the attributes and functions of the window the
    # user see on the screen.
    SuperResolutionGuiClass(window)

    # This line is the command that keeps the window open, so we can see it.
    window.mainloop()


if __name__ == '__main__':
    main()
