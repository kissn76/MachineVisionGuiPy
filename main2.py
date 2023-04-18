from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
import tkinter as tk


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.menubar = None
        self.toolbar = None
        self.geometry("500x500")
        self.init_ui()
        self.mainloop()

    def init_ui(self):
        self.title("Toolbar")
        self.init_menubar()
        self.config(menu=self.menubar)

        self.init_toolbar()
        self.toolbar.grid(row=0, column=0, sticky=(tk.E, tk.W))

        self.mainbar = tk.Frame(self, bd=6, relief=tk.RAISED)
        self.mainbar.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        namelbl = tk.Label(self.mainbar, text="Name")
        namelbl.grid(row=0, column=0)

        # self.pack()

    def init_menubar(self):
        self.menubar = tk.Menu(self)
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

    def init_toolbar(self):
        self.toolbar = tk.Frame(self, bd=6, relief=tk.RAISED)

        icon_exit = ImageTk.PhotoImage(Image.open("resources/icons/exit.png"))
        btn_exit = tk.Button(self.toolbar, image=icon_exit, width=64, height=64, command=self.onExit)
        btn_exit.image = icon_exit
        btn_exit.grid(row=0, column=0)

        btn_exit_2 = tk.Button(self.toolbar, image=icon_exit, width=64, height=64, command=self.onExit)
        btn_exit_2.image = icon_exit
        btn_exit_2.grid(row=0, column=1)

    def onExit(self):
        self.quit()


def main():
    # # Load the image
    # img = cv2.imread('/home/nn/Képek/ocv.jpg')
    #
    # # Rearrange colors
    # blue, green, red = cv2.split(img)
    # img = cv2.merge((red, green, blue))
    # im = Image.fromarray(img)
    #
    # win = Tk()
    # # win.geometry("700x550")
    # imgtk = ImageTk.PhotoImage(image=im)
    # Label(win, image=imgtk).pack()
    # win.mainloop()

    Mainwindow()


if __name__ == '__main__':
    main()
