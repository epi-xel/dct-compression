import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import numpy as np
import converter as cv
from PIL import ImageTk, Image
import sv_ttk

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=3)
        self.rowconfigure(index=2, weight=1)
        
        self.columnconfigure(index=0, weight=1)

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value="Test")
        self.var_5 = tk.DoubleVar(value=75.0)

        self.setup_widgets()


    def setup_widgets(self):

        def open_file():
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
                    self.image.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
                    set_intervals(file)

        def set_intervals(file):
            min_F, max_F, min_d, max_d = cv.get_intervals(cv.get_pixel_map(file))
            self.scale1.configure(from_=min_F, to=max_F)
            self.scale2.configure(from_=min_d, to=max_d)
            self.scale1.set(min_F)
            self.scale2.set(min_d)
            self.label_scale1.configure(text="Macro-blocks size: " + str(min_F))
            self.label_scale2.configure(text="Frequency threshold: " + str(min_d))
            self.min_label1.configure(text=str(min_F))
            self.max_label1.configure(text=str(max_F))
            self.min_label2.configure(text=str(min_d))
            self.max_label2.configure(text=str(max_d))
        
        def get_scale_value():
            return self.scale1.get(), self.scale2.get()
        
        def set_new_value1(value):
            self.label_scale1.configure(text="Macro-blocks size: " + str(int(float(value))))

        def set_new_value2(value):
            self.label_scale2.configure(text="Frequency threshold: " + str(int(float(value))))

        self.frame = ttk.LabelFrame(self, text="Set properties", padding=(20, 10))
        self.frame.grid(
            row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew",
        )

        self.head = ttk.LabelFrame(self, text="File", padding=(20, 10))
        self.head.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew"
        )

        self.frame.columnconfigure(index=0, weight=1)
        self.frame.columnconfigure(index=1, weight=4)
        self.frame.columnconfigure(index=2, weight=1)

        self.convert_button = ttk.Button(
            self,
            text='Convert and View',
        )
        self.convert_button.grid(column=0, row=2, sticky='s', padx=10, pady=40)

        self.open_button = ttk.Button(
            self.head,
            text='Open a File',
            command=open_file
        )

        self.open_button.grid(column=0, row=0, sticky='w', padx=10, pady=10)

        self.image = ttk.Label(self.head)
        self.image.grid(column=0, row=2, sticky='w', padx=10, pady=10)

        #self.label = ttk.Label(self.head, text="")
        #self.label.grid(column=1, row=0, sticky='w', padx=10, pady=10)

        self.label_scale1 = ttk.Label(self.frame, text="Macro-blocks size:")
        self.label_scale1.grid(row=0, padx=5, pady=10, columnspan = 3, sticky="ew")
        self.label_scale2 = ttk.Label(self.frame, text="Frequency threshold:")
        self.label_scale2.grid(row=2, padx=5, pady=10, columnspan = 3, sticky="ew")

        self.min_label1 = ttk.Label(self.frame, text="0")
        self.min_label1.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="e")

        self.max_label1 = ttk.Label(self.frame, text="100")
        self.max_label1.grid(row=1, column=2, padx=5, pady=(5, 5), sticky="w")

        self.min_label2 = ttk.Label(self.frame, text="0")
        self.min_label2.grid(row=3, column=0, padx=5, pady=(5, 5), sticky="e")

        self.max_label2 = ttk.Label(self.frame, text="100")
        self.max_label2.grid(row=3, column=2, padx=5, pady=(5, 5), sticky="w")

        #self.current_value_label = ttk.Label(self.frame, textvariable=self.scale1)
        #self.current_value_label.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Scale
        self.scale1 = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
            value=75,
            cursor="hand2",
            command=set_new_value1,
        )
        self.scale1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.scale2 = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
            value=75,
            cursor="hand2",
            command=set_new_value2,
        )
        self.scale2.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    


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
    root.geometry("800x800")
    #block resizing
    root.resizable(False, False)
    #place in center
    root.eval('tk::PlaceWindow . center')

    root.mainloop()