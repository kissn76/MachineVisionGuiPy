from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
from opencvgui import *
import tkinter as tk


commandCounter = 0
commandList = []
commandGuiList = {}
images = {}
imagesShow = []


class AvailableCommandRow(tk.Frame):
    def __init__(self, master, command):
        super().__init__(master)

        lbl_command = ttk.Label(self, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda e: self.addRow(command))

    def addRow(self, command):
        global commandCounter
        commandList.append(f"{command}.{commandCounter}")
        commandCounter += 1


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

        self.commandRows = {}

        # self.attributes("-fullscreen", True)
        # self.attributes("-zoomed", True)

        self.frm_image = tk.Frame(self)
        self.lbl_image = ttk.Label(self.frm_image)
        self.lbl_image.pack()

        self.frm_config = tk.Frame(self)
        self.frm_available_commands = tk.Frame(self.frm_config)
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

        availableCommands = ["opencv_imread", "opencv_threshold", "opencv_resize"]
        for a in availableCommands:
            AvailableCommandRow(self.frm_available_commands, a).pack()

        self.nextImage()

        self.mainloop()


    def nextImage(self):
        for command in commandGuiList.keys():
            if command not in commandList:
                commandGuiList.pop(command)
                self.commandRows[command].pack_forget()
                self.commandRows[command].destroy()
                self.commandRows.pop(command)

        for command in commandList:
            if command not in commandGuiList:
                if command.startswith("opencv_imread"):
                    commandGuiList[command] = ImreadGui(self.frm_setting, command)
                elif command.startswith("opencv_threshold"):
                    commandGuiList[command] = ThresholdGui(self.frm_setting, command)
                elif command.startswith("opencv_resize"):
                    commandGuiList[command] = ResizeGui(self.frm_setting, command)

                self.commandRows.update({command: CommandRow(self.frm_commands, command)})
                self.commandRows[command].pack()

            commandGuiList[command].runProcess(images)

        try:
            # TODO
            # Összefűzni a képeket az imagesShow listből
            im = Image.fromarray(list(images.values())[-1])
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
    # commandParameters.update({"opencv_imread.1": {"dst": "opencv_imread.1.dst", "filename": "/home/nn/Képek/ocv.jpg", "flags": cv2.IMREAD_GRAYSCALE}})
    # commandParameters.update({"opencv_threshold.1": {"src": "opencv_imread.1.dst", "dst": "opencv_threshold.1.dst", "threshold": 100, "maxval": 255, "type": cv2.THRESH_BINARY}})
    # commandParameters.update({"opencv_resize.1": {"imshow": True, "src": "opencv_threshold.1.dst", "dst": "opencv_resize.1.dst", "dsize": (0, 0), "fx": 0.4, "fy": 0.4, "interpolation": cv2.INTER_AREA}})

    # global commandList
    # commandList = list(commandParameters.keys())
    Mainwindow()


if __name__ == '__main__':
    main()
