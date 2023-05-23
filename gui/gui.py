import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import sv_ttk

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)


        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value="Test")
        self.var_5 = tk.DoubleVar(value=75.0)

        self.setup_widgets()


    def setup_widgets(self):

        def open_text_file():
            filetypes = (
                ('BMP files', '*.bmp'),
            )
            f = fd.askopenfile(filetypes=filetypes)
            if f:
                with open(f.name, 'rb') as file:
                    image = Image.open(file)
                    target_height = 400
                    width, height = image.size
                    relative_width = int((target_height / height) * width)
                    image.thumbnail((target_height, relative_width))
                    img = ImageTk.PhotoImage(image)
                    self.image.configure(image=img)
                    self.image.image = img
                    self.image.grid(row=2, column=0, padx=10, pady=10, sticky='w')


        self.frame = ttk.LabelFrame(self, text="Set properties", padding=(20, 10))
        self.frame.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew",
        )

        self.head = ttk.LabelFrame(self, text="File", padding=(20, 10))
        self.head.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        self.open_button = ttk.Button(
            self.head,
            text='Open a File',
            command=open_text_file
        )

        self.open_button.grid(column=0, row=0, sticky='w', padx=10, pady=10)

        self.image = ttk.Label(self.head)
        self.image.grid(column=0, row=2, sticky='w', padx=10, pady=10)

        #self.label = ttk.Label(self.head, text="")
        #self.label.grid(column=1, row=0, sticky='w', padx=10, pady=10)

        # Scale
        self.scale1 = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
        )
        self.scale1.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        self.scale2 = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
        )
        self.scale2.grid(row=3, column=0, padx=5, pady=10, sticky="ew")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    #root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    root.geometry("800x600")
    #block resizing
    root.resizable(False, False)
    #place in center
    root.eval('tk::PlaceWindow . center')

    root.mainloop()