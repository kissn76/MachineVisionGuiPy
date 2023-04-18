from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
from ocvthreshold import OcvThreshold
import tkinter as tk


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.frm_image = tk.Frame(self)

        self.lbl_image = tk.Label(self.frm_image)

        self.ocvth = OcvThreshold(self)

        btn_next = tk.Button(self, text="Next", command=self.nextImage)

        self.frm_image.pack()
        self.lbl_image.pack()
        self.ocvth.pack()
        btn_next.pack()

        self.mainloop()

    def nextImage(self):
        self.ocvth.printvalues()
        img = cv2.imread('/home/nn/Képek/ocv.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        t, img = cv2.threshold(img, self.ocvth.threshold_value, self.ocvth.max_value, self.ocvth.type[0])
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        self.lbl_image.configure(image=imgtk)
        self.lbl_image.image = imgtk
        # self.update()

    def onExit(self):
        self.quit()


def main():
    Mainwindow()


if __name__ == '__main__':
    main()
