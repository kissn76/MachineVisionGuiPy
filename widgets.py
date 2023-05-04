import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class FwCombobox(ttk.Frame):
    def __init__(self, master, name, values, default_value, state="readonly"):
        super().__init__(master)

        self.values = values

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.StringVar()
        self.widget = ttk.Combobox(self, textvariable=self.var_widget, state=state)
        self.widget.config(values=tuple(self.values.keys()))
        self.set(default_value)

        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        value = self.values[self.var_widget.get()]
        return value


    def set(self, value):
        index = tuple(self.values.values()).index(value)
        self.widget.current(newindex=index)


class FwScale(ttk.Frame):
    def __init__(self, master, name, from_value, to_value, default_value, resolution=1, value_type=float, orient=tk.HORIZONTAL):
        super().__init__(master)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = None
        if value_type is float:
            self.var_widget = tk.DoubleVar()
        elif value_type is int:
            self.var_widget = tk.IntVar()
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


class FwCheckbutton(ttk.Frame):
    def __init__(self, master, name, text, default_value, onvalue=True, offvalue=False):
        super().__init__(master)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.BooleanVar()
        self.widget = ttk.Checkbutton(self, text=text, variable=self.var_widget, onvalue=onvalue, offvalue=offvalue)
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

        self.lbl_image = ttk.Label(self)
        self.lbl_image.pack()

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
