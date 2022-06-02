import tkinter as tk
from gui_class import SuperResolutionGuiClass


def main():
    window = tk.Tk()

    SuperResolutionGuiClass(window)

    window.mainloop()


if __name__ == '__main__':
    main()
