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
        self.rowconfigure(index=1, weight=4)
        self.rowconfigure(index=2, weight=2)
        self.rowconfigure(index=3, weight=2)
        
        self.columnconfigure(index=0, weight=1)

        # Create control variables
        self.file_name = tk.StringVar(value=None)

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
                    self.image.configure(image=img, anchor="center")
                    self.image.image = img
                    self.image.grid(row=0, column=1, padx=10, pady=(10, 5), columnspan=3)
                    set_intervals(file)

        def set_intervals(file):

            min_F, max_F = cv.get_intervals(cv.get_pixel_map(file))
            self.scale1.configure(from_=min_F, to=max_F)
            self.scale1.set(max_F / 2)
            min_d = 1
            max_d = 2 * max_F - 2
            self.scale2.configure(from_=min_d, to=max_d)
            self.scale2.set(max_d / 2)
            self.label_scale1.configure(text="Macro-blocks size: " + str(min_F))
            self.label_scale2.configure(text="Frequency threshold: " + str(min_d))
            self.min_label1.configure(text=str(min_F))
            self.max_label1.configure(text=str(max_F))
            self.min_label2.configure(text=str(min_d))
            self.max_label2.configure(text=str(max_d))
            self.frame.grid(
                row=2, column=0, padx=20, pady=10, sticky="nsew",
            )
            self.file.grid(
                row=1, column=0, padx=20, pady=(10, 0), sticky="nsew",
            )
            self.convert_button.grid(column=0, row=3, padx=10, pady=10)
            self.file_name.set(file.name)

        def convert_and_show():
            F, d = get_scale_value()
            old_image = Image.open(self.file_name.get())
            image = cv.convert(cv.get_pixel_map(self.file_name.get()), int(F), int(d))
            width, height = image.size
            
            if width > height:
                target_width = 800
                relative_height = int((target_width / width) * height)
                image.thumbnail((target_width, relative_height))
                old_image.thumbnail((target_width, relative_height))
            else:
                target_height = 800
                relative_width = int((target_height / height) * width)
                image.thumbnail((relative_width, target_height))
                old_image.thumbnail((relative_width, target_height))

            nw = Toplevel(self)
            nw.title("Comparison")
            nw.resizable(False, False)
            geometry = str(image.size[0] + old_image.size[0]) + "x" + str(image.size[1] + 50)
            if((image.size[0] + old_image.size[0]) < 300):
                geometry = "300x" + str(image.size[1] + 70)
            nw.geometry(geometry)

            nw.columnconfigure(index=0, weight=1)
            nw.columnconfigure(index=1, weight=1)
            nw.rowconfigure(index=0, weight=1)
            nw.rowconfigure(index=1, weight=10)
            
            nw.old = ttk.Label(nw, text="Original image")
            nw.new = ttk.Label(nw, text="Converted image")
            img_new = ImageTk.PhotoImage(image)
            img_old = ImageTk.PhotoImage(old_image)
            
            nw.new.configure(image=img_new)
            nw.old.configure(image=img_old)
            
            nw.new.image = img_new
            nw.old.image = img_old
            
            nw.old.grid(row=1, column=0, padx=10, pady=(10, 5))
            nw.new.grid(row=1, column=1, padx=10, pady=(10, 5))

            nw.label_new = ttk.Label(nw, text="Converted image")
            nw.label_old = ttk.Label(nw, text="Original image")

            nw.label_new.grid(row=0, column=1, padx=10, pady=(10, 5))
            nw.label_old.grid(row=0, column=0, padx=10, pady=(10, 5))

        
        def get_scale_value():
            return self.scale1.get(), self.scale2.get()
        
        def set_new_value1(value):
            self.label_scale1.configure(text="Macro-blocks size: " + str(int(float(value))))
            min_d = 1
            max_d = int(2 * int(float(value)) - 2)
            self.scale2.configure(from_=min_d, to=max_d)
            self.scale2.set(max_d / 2)
            self.label_scale2.configure(text="Frequency threshold: " + str(min_d))
            self.min_label2.configure(text=str(min_d))
            self.max_label2.configure(text=str(max_d))

        def set_new_value2(value):
            self.label_scale2.configure(text="Frequency threshold: " + str(int(float(value))))

        self.head = ttk.Frame(self)
        self.head.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 10)
        )

        self.intro = ttk.Label(
            self.head,
            text="This application allows you to convert a BMP image into a JPEG one.\nClick the button below to open a file"
                 + " and then set the properties of the conversion. \nWhen you are ready, click the button below to convert the image.",
            padding=(20, 10),
            justify="center"
        )

        self.intro.grid(column=0, row=0, padx=10, pady=10)
        
        self.file = ttk.LabelFrame(self, text="File selected", padding=(10, 10))
        self.file.columnconfigure(index=0, weight=0)
        self.file.columnconfigure(index=1, weight=10) 
        self.file.columnconfigure(index=2, weight=0)
        self.file.rowconfigure(index=2, weight=1)

        self.frame = ttk.LabelFrame(self, text="Set properties", padding=(20, 10))

        self.frame.grid_forget()

        self.frame.columnconfigure(index=0, weight=1)
        self.frame.columnconfigure(index=1, weight=4)
        self.frame.columnconfigure(index=2, weight=1)

        self.convert_button = ttk.Button(
            self,
            text='Convert and View',
            command=convert_and_show
        )

        self.convert_button.grid_forget()

        self.open_button = ttk.Button(
            self.head,
            text='Open a File',
            command=open_file
        )

        self.open_button.grid(column=0, row=1)

        self.image = ttk.Label(self.file, anchor="center")
        #self.image.grid(column=0, row=2, padx=10, pady=5, sticky="nsew", columnspan=3)

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
    root.title("JPEG Converter")

    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    #root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    root.geometry("900x800")
    #block resizing
    root.resizable(False, False)
    #place in center
    #root.eval('tk::PlaceWindow . center')

    root.mainloop()