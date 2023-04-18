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
            elif command.startswith("opencv_resize"):
                commandGuiList[command] = ResizeGui(self.frm_methodes, parmeters)

            commandGuiList[command].pack()


    def nextImage(self):
        images["original"] = cv2.imread('/home/nn/Képek/ocv.jpg')
        images["original_rgb"] = cv2.cvtColor(images["original"], cv2.COLOR_BGR2RGB)
        images["original_gray"] = cv2.cvtColor(images["original_rgb"], cv2.COLOR_RGB2GRAY)

        for command in commandList:
            commandGuiList[command].getValues()

            if command.startswith("opencv_threshold"):
                try:
                    commandParameters[command]["threshold"] = commandGuiList[command].threshold_value
                    commandParameters[command]["maxval"] = commandGuiList[command].max_value
                    commandParameters[command]["type"] = commandGuiList[command].type
                    _, image = cv2.threshold(images["original_gray"], commandParameters[command]["threshold"], commandParameters[command]["maxval"], commandParameters[command]["type"])
                    images["original_gray"] = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                except:
                    pass
            elif command.startswith("opencv_resize"):
                try:
                    commandParameters[command]["dsize"] = commandGuiList[command].dsize
                    commandParameters[command]["fx"] = commandGuiList[command].fx
                    commandParameters[command]["fy"] = commandGuiList[command].fy
                    commandParameters[command]["interpolation"] = commandGuiList[command].interpolation
                    images["original_gray"] = cv2.resize(images["original_gray"], dsize=commandParameters[command]["dsize"], fx=commandParameters[command]["fx"], fy=commandParameters[command]["fy"], interpolation=commandParameters[command]["interpolation"])
                except:
                    pass


        im = Image.fromarray(images["original_gray"])
        imgtk = ImageTk.PhotoImage(image=im)
        self.lbl_image.configure(image=imgtk)
        self.lbl_image.image = imgtk
        self.after(100, self.nextImage)

    def onExit(self):
        self.quit()


def main():
    commandList.append("opencv_threshold.1")
    commandParameters.update({"opencv_threshold.1": {"threshold": 100, "maxval": 255, "type": cv2.THRESH_BINARY}})
    commandList.append("opencv_resize.1")
    commandParameters.update({"opencv_resize.1": {"dsize": (0, 0), "fx": 0.4, "fy": 0.4, "interpolation": cv2.INTER_AREA}})
    Mainwindow()


if __name__ == '__main__':
    main()
