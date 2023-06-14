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
    def __init__(self, master, name, default_value, state="readonly", info_label=None, info_description=None):
        super().__init__(master)

        if bool(info_description):
            self.lbl_info = Info(self, self, info_label, info_description)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.StringVar()
        self.widget = ttk.Entry(self, textvariable=self.var_widget, state=state)
        self.set(default_value)

        if bool(info_description):
            self.lbl_info.pack(side=tk.LEFT)
        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        return self.var_widget.get()


    def set(self, value):
        self.var_widget.set(value)


class FwCheckbutton(ttk.Frame):
    def __init__(self, master, name, text, default_value, onvalue=True, offvalue=False, info_label=None, info_description=None):
        super().__init__(master)

        self.lbl_info = Info(self, self, info_label, info_description)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.BooleanVar()
        self.widget = ttk.Checkbutton(self, text=text, variable=self.var_widget, onvalue=onvalue, offvalue=offvalue)
        self.set(default_value)

        self.lbl_info.pack(side=tk.LEFT)
        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        return self.var_widget.get()


    def set(self, value):
        self.var_widget.set(value)


class FwImage(ttk.Frame):
    def __init__(self, master, name, scale_factor=1.0, default_image="resources/gears_400.jpg"):
        super().__init__(master)
        self.scale_factor = scale_factor

        self.lbl_image = ttk.Label(self)
        self.lbl_image.pack()

        image = Image.open(default_image)
        image = image.resize((int(image.width * self.scale_factor), int(image.height * self.scale_factor)))
        imagetk = ImageTk.PhotoImage(image)
        self.lbl_image.configure(image=imagetk)
        self.lbl_image.image = imagetk


    def set_scale_factor(self, scale_factor):
        self.scale_factor = scale_factor


    def get(self):
        pass


    def set(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_tmp = Image.fromarray(image)
        image_tmp = image_tmp.resize((int(image_tmp.width * self.scale_factor), int(image_tmp.height * self.scale_factor)))
        imagetk = ImageTk.PhotoImage(image=image_tmp)
        self.lbl_image.configure(image=imagetk)
        self.lbl_image.image = imagetk


class Info(ttk.Label):
    def __init__(self, master, tooltip_master, title, text):
        self.image_info = ImageTk.PhotoImage(Image.open("./resources/icons/info_16.png"))
        super().__init__(master, image=self.image_info)
        self.image = self.image_info
        self.tooltip_master = tooltip_master
        self.title = title
        self.text = text
        self.popup = None

        self.bind("<Enter>", lambda event: self.popup_open())
        self.bind("<Leave>", lambda event: self.popup_destroy_timer())


    def popup_destroy_timer(self, ms=1000):
        self.popup.after(ms, self.popup_destroy)


    def popup_destroy(self):
        self.popup.destroy()
        self.popup.update()
        self.popup = None


    def popup_open(self):
        if not bool(self.popup):
            self.popup = tk.Toplevel(self.tooltip_master, width=500)
            self.popup.title(self.title)

            lbl_title = ttk.Label(self.popup, text=self.title, font=('Mistral 18 bold'))
            lbl_text = ttk.Label(self.popup, text=self.text)

            lbl_title.pack()
            lbl_text.pack()

            self.popup.bind("<Button-1>", lambda event: self.popup_destroy())
            self.popup.bind("<Leave>", lambda event: self.popup_destroy_timer())

            self.popup.mainloop()
