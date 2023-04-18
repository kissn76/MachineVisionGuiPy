from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
from opencvgui import *
import tkinter as tk


commandList = []
commandParameters = {}
commandGuiList = {}
images = {}


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.frm_image = tk.Frame(self)
        self.lbl_image = tk.Label(self.frm_image)
        self.lbl_image.pack()

        self.frm_methodes = tk.Frame(self)
        # self.ocvresize = ResizeGui(self.frm_methodes)
        # self.ocvresize.pack()

        # btn_next = tk.Button(self, text="Next", command=self.nextImage)

        self.frm_image.grid(row=0, column=0)
        self.frm_methodes.grid(row=0, column=1)
        # btn_next.pack()

        self.setUI()
        self.nextImage()

        self.mainloop()


    def setUI(self):
        for command in commandList:
            parmeters = {}
            try:
                parmeters = commandParameters[command]
            except:
                pass

            if command.startswith("opencv_threshold"):
                commandGuiList[command] = ThresholdGui(self.frm_methodes, parmeters)

            commandGuiList[command].pack()


    def nextImage(self):
        images["original"] = cv2.imread('/home/nn/Képek/ocv.jpg')
        images["original_rgb"] = cv2.cvtColor(images["original"], cv2.COLOR_BGR2RGB)
        images["original_gray"] = cv2.cvtColor(images["original_rgb"], cv2.COLOR_RGB2GRAY)

        # self.ocvresize.getValues()

        for command in commandList:
            if command.startswith("opencv_threshold"):
                commandGuiList[command].getValues()
                _, images["threshold"] = cv2.threshold(images["original_gray"], commandGuiList[command].threshold_value, commandGuiList[command].max_value, commandGuiList[command].type)
                images["threshold_rgb"] = cv2.cvtColor(images["threshold"], cv2.COLOR_GRAY2RGB)

        # try:
        #     img = cv2.resize(images["threshold_rgb"], dsize=self.ocvresize.dsize, fx=self.ocvresize.fx, fy=self.ocvresize.fy, interpolation=self.ocvresize.interpolation)
        # except:
        #     pass


        im = Image.fromarray(images["threshold_rgb"])
        imgtk = ImageTk.PhotoImage(image=im)
        self.lbl_image.configure(image=imgtk)
        self.lbl_image.image = imgtk
        # self.update()
        self.after(100, self.nextImage)

    def onExit(self):
        self.quit()


def main():
    commandList.append("opencv_threshold.1")
    commandParameters.update({"opencv_threshold.1": {"threshold": 10, "maxval": 250, "type": cv2.THRESH_TOZERO}})
    Mainwindow()


if __name__ == '__main__':
    main()
