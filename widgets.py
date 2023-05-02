import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class FwCombobox(ttk.Frame):
    def __init__(self, master, name, values, default_index, state="readonly"):
        super().__init__(master)

        self.values = values

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.StringVar()
        self.widget = ttk.Combobox(self, textvariable=self.var_widget, state=state)
        self.widget.config(values=tuple(self.values.keys()))
        self.set(default_index)

        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        return self.values[self.var_widget.get()]


    def set(self, index):
        self.widget.current(newindex=index)


class FwScale(ttk.Frame):
    def __init__(self, master, name, from_value, to_value, default_value, resolution=1, orient=tk.HORIZONTAL):
        super().__init__(master)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.DoubleVar()
        self.widget = tk.Scale(self, variable=self.var_widget, from_=from_value, to=to_value, resolution=resolution, orient=orient)
        self.set(default_value)

        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        return self.var_widget.get()


    def set(self, value):
        self.widget.set(value)


class FwEntry(ttk.Frame):
    def __init__(self, master, name, default_value, state="readonly"):
        super().__init__(master)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.StringVar()
        self.widget = ttk.Entry(self, textvariable=self.var_widget, state=state)
        self.set(default_value)

        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        return self.var_widget.get()


    def set(self, value):
        self.var_widget.set(value)


class FwImage(ttk.Frame):
    def __init__(self, master, name, default_image="resources/gears_400.jpg"):
        super().__init__(master)

        self.input = "src"

        self.lbl_input = ttk.Label(self, text=self.input)
        self.lbl_name = ttk.Label(self, text=name)
        self.lbl_image = ttk.Label(self)

        # self.lbl_name.pack()
        self.lbl_image.pack()
        # self.lbl_input.pack()

        imagetk = ImageTk.PhotoImage(Image.open(default_image))
        self.lbl_image.configure(image=imagetk)
        self.lbl_image.image = imagetk


    def get(self):
        pass


    def set(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imagetk = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.lbl_image.configure(image=imagetk)
        self.lbl_image.image = imagetk
