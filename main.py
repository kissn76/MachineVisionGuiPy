from PIL import Image, ImageTk
import cv2
from numpy import size

import numpy as np
from opencvgui import *
import tkinter as tk


command_counter = 0         # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
command_list = []           # végrehajtási sor. A végrehajtandó parancsokat tartalmazza
command_object_list = {}    # a végrehajtandó parancsok object-jeit tartalmazza
image_list = {}             # a parancsok outputjaként létrehozott image-eket tartalmazza
image_show = None

available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize"]


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.command_row_list = {}  # CommandRow objektumokat (végrehajtandó parancsok) tartalmazza
        self.image_row_list = {}

        self.title("Machine Vision GUI")
        self.geometry("1280x700")
        # self.attributes("-fullscreen", True)
        # self.attributes("-zoomed", True)

        self.frm_image = tk.Frame(self)
        self.frm_image_list = tk.Frame(self.frm_image)
        self.lbl_image = ttk.Label(self.frm_image)
        self.frm_image_list.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_image.grid(row=0, column=1, sticky="n, s, w, e")

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

        # elérhető parancsok gui frame feltöltése
        for a in available_commands:
            self.add_available_command_row(a)

        self.next_image()

        self.mainloop()


    def add_available_command_row(self, command):
        frm_row = tk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda event: self.add_command_row(command))
        frm_row.pack()


    def add_command_row(self, command):
        global command_counter
        command_name = f"{command}.{command_counter}"
        command_counter += 1

        # hozzáadás a gui-hoz
        frm_row = tk.Frame(self.frm_commands)
        lbl_command = ttk.Label(frm_row, text=command_name, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Button-1>", lambda event: self.show_command_setting_form(command_name))

        self.command_row_list.update({command_name: frm_row})

        # hozzáadás a végrehajtási listához
        command_list.append(command_name)

        if command_name.startswith("opencv_imread"):
            command_object_list[command_name] = ImreadGui(self.frm_setting, command_name)
        elif command_name.startswith("opencv_threshold"):
            command_object_list[command_name] = ThresholdGui(self.frm_setting, command_name)
        elif command_name.startswith("opencv_resize"):
            command_object_list[command_name] = ResizeGui(self.frm_setting, command_name)

        command_object_list[command_name].set_src_list(image_list)
        self.set_command_row_list_frame()


    def show_command_setting_form(self, command):
        # az összes beállítás eltüntetése
        for obj in command_object_list.values():
            obj.pack_forget()

        # a szükséges (amelyikre kattintottunk) beállítás megjelenítése
        command_object_list[command].pack()
        command_object_list[command].set_src_list(image_list)


    def set_command_row_list_frame(self):
        for obj in self.command_row_list.values():
            obj.pack_forget()

        for str in command_list:
            self.command_row_list[str].pack()


    def set_image_list_frame(self):
        for image_name in image_list.keys():
            if not image_name in self.image_row_list.keys():
                frm_row = tk.Frame(self.frm_image_list)
                lbl_command = ttk.Label(frm_row, text=image_name, cursor= "hand2")
                lbl_command.pack()
                lbl_command.bind("<Button-1>", lambda event: self.set_image_show(image_name))
                frm_row.pack()

                self.image_row_list.update({image_name: frm_row})


    def set_image_show(self, image_name):
        global image_show
        image_show = image_name


    def next_image(self):
        image_list.clear()

        for command in command_list:
            command_object_list[command].run_process(image_list)

        self.set_image_list_frame()

        try:
            image = None
            if image_show is None:
                image = list(image_list.values())[-1]
            else:
                image = image_list[image_show]

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im)
            self.lbl_image.configure(image=imgtk)
            self.lbl_image.image = imgtk
        except:
            pass
        self.after(100, self.next_image)


def main():
    # commandParameters.update({"opencv_imread.1": {"dst": "opencv_imread.1.dst", "filename": "/home/nn/Képek/ocv.jpg", "flags": cv2.IMREAD_GRAYSCALE}})
    # commandParameters.update({"opencv_threshold.1": {"src": "opencv_imread.1.dst", "dst": "opencv_threshold.1.dst", "threshold": 100, "maxval": 255, "type": cv2.THRESH_BINARY}})
    # commandParameters.update({"opencv_resize.1": {"imshow": True, "src": "opencv_threshold.1.dst", "dst": "opencv_resize.1.dst", "dsize": (0, 0), "fx": 0.4, "fy": 0.4, "interpolation": cv2.INTER_AREA}})

    Mainwindow()


if __name__ == '__main__':
    main()
