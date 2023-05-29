import utils.converter as cv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from threading import Thread
from multiprocessing import Process, Queue
from gui.zoom import *
from gui.filechooser import *


class App(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=4)
        self.rowconfigure(index=2, weight=2)
        self.rowconfigure(index=3, weight=1)
        
        self.columnconfigure(index=0, weight=1)

        self.file_name = tk.StringVar(value=None)

        self.setup_widgets()

    def set_intervals(self, file):

        min_F, max_F = cv.get_intervals(cv.get_pixel_map(file))
        self.scale1.configure(from_=min_F, to=max_F)
        scale1_value = int((min_F + max_F) // 2)
        self.scale1.set(scale1_value)
        self.label_scale1.configure(text="Macro-blocks size: " + str(scale1_value))
        self.min_label1.configure(text=str(min_F))
        self.max_label1.configure(text=str(max_F))
        self.set_scale2_values(scale1_value)
        self.frame.grid(
            row=2, column=0, padx=20, pady=10, sticky="nsew",
        )
        self.file.grid(
            row=1, column=0, padx=20, pady=(10, 0), sticky="nsew",
        )
        self.convert_button.grid(column=0, row=3, padx=10, pady=20)
        self.file_name.set(file.name)

    def open_file_thread(self):
        queue = Queue()
        p = Process(target=open_file_chooser, args=(queue,))
        p.start()
        p.join()
        f = queue.get()
        if f:
            with open(f, 'rb') as file:
                image = Image.open(file)
                self.canvas = CanvasImage(self.file, path=image)
                self.canvas.grid(row=0, column=1, padx=10, pady=0,sticky="nsew")
                self.set_intervals(file)

    def open_file(self):
        Thread(target=self.open_file_thread).start()

    def convert_and_show(self):
        F, d = self.get_scale_value()
        old_image = Image.open(self.file_name.get())
        image = cv.convert(cv.get_pixel_map(self.file_name.get()), int(F), int(d))
        
        nw = Toplevel(self)
        nw.title("Comparison")

        nw.columnconfigure(index=0, weight=1)
        nw.columnconfigure(index=1, weight=1)
        nw.rowconfigure(index=0, weight=1)
        nw.rowconfigure(index=1, weight=10)

        nw.old = CanvasImage(nw, path=old_image)
        nw.new = CanvasImage(nw, path=image)

        nw.old.add_twin(nw.new)
        nw.new.add_twin(nw.old)

        nw.old.grid(row=1, column=0, padx=10, pady=(10, 5))
        nw.new.grid(row=1, column=1, padx=10, pady=(10, 5))

        nw.label_new = ttk.Label(nw, text="Converted image")
        nw.label_old = ttk.Label(nw, text="Original image")

        nw.label_new.grid(row=0, column=1, padx=10, pady=(10, 5))
        nw.label_old.grid(row=0, column=0, padx=10, pady=(10, 5))

        
    def get_scale_value(self):
        return self.scale1.get(), self.scale2.get()
    
    def set_scale2_values(self, value):
        min_d = 1
        max_d = 2 * int(float(value)) - 2
        self.scale2.configure(from_=min_d, to=max_d)
        scale2_value = int((min_d + max_d) // 2)
        self.scale2.set(scale2_value)
        self.label_scale2.configure(text="Frequency threshold: " + str(scale2_value))
        self.min_label2.configure(text=str(min_d))
        self.max_label2.configure(text=str(max_d))

    def set_new_value1(self, value):
        self.label_scale1.configure(text="Macro-blocks size: " + str(int(float(value))))
        self.set_scale2_values(value)

    def set_new_value2(self, value):
        self.label_scale2.configure(text="Frequency threshold: " + str(int(float(value))))

    def setup_widgets(self):  

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
        self.file.rowconfigure(index=0, weight=1)
    
        self.frame = ttk.LabelFrame(self, text="Set properties", padding=(20, 10))

        self.frame.grid_forget()

        self.frame.columnconfigure(index=0, weight=1)
        self.frame.columnconfigure(index=1, weight=4)
        self.frame.columnconfigure(index=2, weight=1)

        self.convert_button = ttk.Button(
            self,
            text='Convert and View',
            command=self.convert_and_show
        )

        self.convert_button.grid_forget()

        self.open_button = ttk.Button(
            self.head,
            text='Open a File',
            command=self.open_file
        )

        self.open_button.grid(column=0, row=1, pady=10)

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

        self.scale1 = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
            value=75,
            cursor="hand2",
            command=self.set_new_value1,
        )
        self.scale1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.scale2 = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
            value=75,
            cursor="hand2",
            command=self.set_new_value2,
        )
        self.scale2.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
