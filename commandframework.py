import cv2
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import widgets as wg
from enums import *


command_counter = 0


class CommandGui(ttk.Frame):
    def __init__(self, master, command):
        super().__init__(master)
        global command_counter

        self.command_name = f"{command}.{command_counter}"
        command_counter += 1
        self.widget_list = {}
        self.run = None

        self.name = ttk.Label(self, text=command)
        self.widget_list_set()

        self.name.pack()
        for widget in self.widget_list.values():
            widget.pack()


    def widget_list_set(self):
        if self.command_name.startswith("opencv_imread"):
            self.widget_list.update({"filename": wg.FwEntry(self, "Filename", "./resources/example/ocv_1.jpg", state=None)})
            self.widget_list.update({"flags": wg.FwCombobox(self, "Flags", ENUM_IMREAD_MODES, tuple(ENUM_IMREAD_MODES.values()).index(cv2.IMREAD_UNCHANGED))})
            self.widget_list.update({"output": wg.FwEntry(self, "Output", f"{self.command_name}.out")})

            def run_command(images):
                filename = self.widget_list["filename"].get()
                flags = self.widget_list["flags"].get()
                output = self.widget_list["output"].get()

                if Path(filename).is_file():
                    image = None
                    try:
                        image = cv2.imread(filename, flags)
                        images.update({output: image})
                        return True
                    except:
                        pass

                return False

            self.run = run_command

        elif self.command_name.startswith("opencv_threshold"):
            self.widget_list.update({"src": wg.FwEntry(self, "Source", None)})
            self.widget_list.update({"dst": wg.FwEntry(self, "Destination", f"{self.command_name}.dst")})
            self.widget_list.update({"thresh": wg.FwScale(self, "Threshold", 0, 255, 150)})
            self.widget_list.update({"maxval": wg.FwScale(self, "Maximum value", 0, 255, 255)})
            self.widget_list.update({"type": wg.FwCombobox(self, "Type", ENUM_THRESHOLD_TYPES, tuple(ENUM_THRESHOLD_TYPES.values()).index(cv2.THRESH_BINARY))})

            def run_command(images):
                src = self.widget_list["src"].get()
                dst = self.widget_list["dst"].get()
                thresh = self.widget_list["thresh"].get()
                maxval = self.widget_list["maxval"].get()
                type = self.widget_list["type"].get()

                if bool(src) and len(images["src"]) > 0:
                    image = None
                    try:
                        _, image = cv2.threshold(images["src"], thresh, maxval, type)
                        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                        images.update({dst: image})
                        return True
                    except:
                        pass

                return False

            self.run = run_command

        elif self.command_name.startswith("opencv_resize"):
            self.widget_list.update({"src": wg.FwEntry(self, "Source", None)})
            self.widget_list.update({"dst": wg.FwEntry(self, "Destination", f"{self.command_name}.dst")})
            self.widget_list.update({"dsize_w": wg.FwScale(self, "Width", 0, 255, 0)})
            self.widget_list.update({"dsize_h": wg.FwScale(self, "Height", 0, 255, 0)})
            self.widget_list.update({"fx": wg.FwScale(self, "Factor x", 0, 1, 0.3, resolution=0.1)})
            self.widget_list.update({"fy": wg.FwScale(self, "Factor y", 0, 1, 0.3, resolution=0.1)})
            self.widget_list.update({"interpolation": wg.FwCombobox(self, "Interpolation", ENUM_INTERPOLATION_FLAGS, tuple(ENUM_INTERPOLATION_FLAGS.values()).index(cv2.INTER_NEAREST))})

            def run_command(images):
                src = self.widget_list["src"].get()
                dst = self.widget_list["dst"].get()
                dsize_w = self.widget_list["dsize_w"].get()
                dsize_h = self.widget_list["dsize_h"].get()
                fx = self.widget_list["fx"].get()
                fy = self.widget_list["fy"].get()
                interpolation = self.widget_list["interpolation"].get()

                if bool(src) and len(images["src"]) > 0:
                    image = None
                    try:
                        image = cv2.resize(src, dsize=(dsize_w, dsize_h), fx=fx, fy=fy, interpolation=interpolation)
                        images.update({dst: image})
                        return True
                    except:
                        pass

                return False

            self.run = run_command

        elif self.command_name.startswith("tk_display"):
            self.widget_list.update({"src": wg.FwEntry(self, "Source", None)})
            self.widget_list.update({"display": wg.FwImage(self, "Image")})

            def run_command(images):
                display_obj = self.widget_list["display"]

                if bool(src) and len(images["src"]) > 0:
                    image = None
                    try:
                        image = cv2.resize(src, dsize=(dsize_w, dsize_h), fx=fx, fy=fy, interpolation=interpolation)
                        images.update({dst: image})
                        return True
                    except:
                        pass

                return False

            self.run = run_command

    def get_values(self):
        values = {}
        for key, widget in self.widget_list.items():
            values.update({key: widget.get()})

        return values


    def print_values(self):
        print(self.get_values())
