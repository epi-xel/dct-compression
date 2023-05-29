import sv_ttk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from gui.app import App

if __name__ == "__main__":
    root = tk.Tk()
    root.title("JPEG Converter")

    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    style = ttk.Style()
    style.configure("Custom.TFiledialog",
                    foreground="#fafafa",
                    background="#1c1c1c")

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    #h = root.winfo_screenheight()
    #root.geometry("900x600")

    root.mainloop()
