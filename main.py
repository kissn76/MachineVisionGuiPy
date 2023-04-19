from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
from opencvgui import *
import tkinter as tk


commandList = []
commandParameters = {}
commandGuiList = {}
usedCommands = {}
images = {}
imagesShow = []


class CommandRow(tk.Frame):
    def __init__(self, master, command):
        super().__init__(master)

        lbl_command = ttk.Label(self, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Button-1>", lambda e: self.setRow(command))

    def setRow(self, command):
        for c in commandList:
            commandGuiList[c].pack_forget()

        commandGuiList[command].pack()


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # self.attributes("-fullscreen", True)
        # self.attributes("-zoomed", True)

        self.frm_image = tk.Frame(self)
        self.lbl_image = ttk.Label(self.frm_image)
        self.lbl_image.pack()

        self.frm_config = tk.Frame(self)
        self.frm_available_commands = tk.Frame(self.frm_config, bg="green")
        self.frm_commands = tk.Frame(self.frm_config)
        self.frm_setting = tk.Frame(self.frm_config)

        ttk.Label(self.frm_available_commands, text="Available commands").pack()
        ttk.Label(self.frm_commands, text="Used commands").pack()
        ttk.Label(self.frm_setting, text="Command setting").pack()

        self.frm_available_commands.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_commands.grid(row=0, column=1)
        self.frm_setting.grid(row=1, column=1)

        self.frm_config.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_image.grid(row=0, column=1, sticky="n, s, w, e")

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

            if command.startswith("opencv_imread"):
                commandGuiList[command] = ImreadGui(self.frm_setting, parmeters)
            elif command.startswith("opencv_threshold"):
                commandGuiList[command] = ThresholdGui(self.frm_setting, parmeters)
            elif command.startswith("opencv_resize"):
                commandGuiList[command] = ResizeGui(self.frm_setting, parmeters)

            # commandGuiList[command].pack()

            CommandRow(self.frm_commands, command).pack()


    def nextImage(self):
        for command in commandList:
            if command.startswith("opencv_imread"):
                images[commandParameters[command]["dst"]] = commandGuiList[command].runProcess()
            else:
                images[commandParameters[command]["dst"]] = commandGuiList[command].runProcess(src=images[commandParameters[command]["src"]])

            try:
                if commandParameters[command]["imshow"]:
                    imagesShow.append(images[commandParameters[command]["dst"]].copy())
            except:
                pass

        try:
            # TODO
            # Összefűzni a képeket az imagesShow listből
            im = Image.fromarray(imagesShow[0])
            imgtk = ImageTk.PhotoImage(image=im)
            self.lbl_image.configure(image=imgtk)
            self.lbl_image.image = imgtk
            imagesShow.clear()
        except:
            pass
        self.after(100, self.nextImage)

    def onExit(self):
        self.quit()


def main():
    commandParameters.update({"opencv_imread.1": {"dst": "opencv_imread.1.dst", "filename": "/home/nn/Képek/ocv.jpg", "flags": cv2.IMREAD_GRAYSCALE}})
    commandParameters.update({"opencv_threshold.1": {"src": "opencv_imread.1.dst", "dst": "opencv_threshold.1.dst", "threshold": 100, "maxval": 255, "type": cv2.THRESH_BINARY}})
    commandParameters.update({"opencv_resize.1": {"imshow": True, "src": "opencv_threshold.1.dst", "dst": "opencv_resize.1.dst", "dsize": (0, 0), "fx": 0.4, "fy": 0.4, "interpolation": cv2.INTER_AREA}})

    global commandList
    commandList = list(commandParameters.keys())
    Mainwindow()


if __name__ == '__main__':
    main()
