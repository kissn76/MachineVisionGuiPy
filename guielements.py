import tkinter as tk
from tkinter import ttk


class FwCombobox(ttk.Frame):
    def __init__(self, master, name, values, default_index, state="readonly"):
        super().__init__(master)

        self.lbl_name = ttk.Label(self, text=name)

        self.var_widget = tk.StringVar()
        self.widget = ttk.Combobox(self, textvariable=self.var_widget, state=state)
        self.widget.config(values=values)
        self.set(default_index)

        self.lbl_name.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)


    def get(self):
        return self.var_widget.get()


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
        return self.var_widget.set(value)