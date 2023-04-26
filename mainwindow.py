import tkinter as tk
from tkinter import ttk
import commandframework as fw


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # command = "opencv_imread"
        command = "opencv_resize"
        # command = "opencv_threshold"
        self.obj = fw.CommandGui(self, command)
        self.obj.pack()

        self.next_image()
        self.mainloop()


    def next_image(self):
        self.obj.print_values()

        self.after(100, self.next_image)
