from PIL import Image, ImageTk
import cv2
from numpy import size
from tkinter import LEFT, TOP, X, FLAT, RAISED, N, S, E, W
from tkinter import Tk, Frame, Menu, Button, PhotoImage, Label

import numpy as np


class Mainwindow():

    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.menubar = None
        self.toolbar = None

        self.init_ui()

        self.root.mainloop()

    def init_ui(self):
        self.root.title("Toolbar")
        self.init_menubar()
        self.root.config(menu=self.menubar)

        self.init_toolbar()
        self.toolbar.grid(row=0, column=0, sticky=(E, W))

        self.mainbar = Frame(self.root, bd=6, relief=RAISED)
        self.mainbar.grid(row=1, column=0, sticky=(N, S, E, W))
        namelbl = Label(self.mainbar, text="Name")
        namelbl.grid(row=0, column=0)

        # self.pack()

    def init_menubar(self):
        self.menubar = Menu(self.root)
        self.fileMenu = Menu(self.root, tearoff=0)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

    def init_toolbar(self):
        self.toolbar = Frame(self.root, bd=6, relief=RAISED)

        icon_exit = ImageTk.PhotoImage(Image.open("resources/icons/exit.png"))
        btn_exit = Button(self.toolbar, image=icon_exit, width=64, height=64, command=self.onExit)
        btn_exit.image = icon_exit
        btn_exit.grid(row=0, column=0)

        btn_exit_2 = Button(self.toolbar, image=icon_exit, width=64, height=64, command=self.onExit)
        btn_exit_2.image = icon_exit
        btn_exit_2.grid(row=0, column=1)

    def onExit(self):
        self.root.quit()


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

    app = Mainwindow()


if __name__ == '__main__':
    main()
