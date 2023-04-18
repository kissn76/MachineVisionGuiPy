from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
from opencvgui import *
import tkinter as tk


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.frm_image = tk.Frame(self)
        self.lbl_image = tk.Label(self.frm_image)
        self.lbl_image.pack()

        self.frm_methodes = tk.Frame(self)
        self.ocvresize = ResizeGui(self.frm_methodes)
        self.ocvth = ThresholdGui(self.frm_methodes)
        self.ocvresize.pack()
        self.ocvth.pack()

        # btn_next = tk.Button(self, text="Next", command=self.nextImage)

        self.frm_image.grid(row=0, column=0)
        self.frm_methodes.grid(row=0, column=1)
        # btn_next.pack()

        self.nextImage()

        self.mainloop()

    def nextImage(self):
        self.ocvresize.getValues()
        self.ocvth.getValues()
        img = cv2.imread('/home/nn/Képek/ocv.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            img = cv2.resize(img, dsize=self.ocvresize.dsize, fx=self.ocvresize.fx, fy=self.ocvresize.fy, interpolation=self.ocvresize.interpolation)
        except:
            pass

        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, img = cv2.threshold(img, self.ocvth.threshold_value, self.ocvth.max_value, self.ocvth.type)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        self.lbl_image.configure(image=imgtk)
        self.lbl_image.image = imgtk
        # self.update()
        self.after(100, self.nextImage)

    def onExit(self):
        self.quit()


def main():
    Mainwindow()


if __name__ == '__main__':
    main()
