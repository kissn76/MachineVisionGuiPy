import cv2
import tkinter as tk
from tkinter import ttk
import guielements as gui
from enums import *


command_counter = 0


class CommandGui(ttk.Frame):
    def __init__(self, master, command):
        super().__init__(master)
        global command_counter

        self.command = command
        self.command_name = f"{command}.{command_counter}"
        command_counter += 1
        self.widget_list = {}

        self.name = ttk.Label(self, text=command)
        self.widget_list_set()

        self.name.pack()
        for widget in self.widget_list.values():
            widget.pack()


    def widget_list_set(self):
        if self.command == "opencv_imread":
            self.widget_list.update({"filename": gui.FwEntry(self, "Filename", "resources/example/ocv_1.jpg", state=None)})
            self.widget_list.update({"flags": gui.FwCombobox(self, "Flags", tuple(ENUM_IMREAD_MODES.keys()), tuple(ENUM_IMREAD_MODES.values()).index(cv2.IMREAD_UNCHANGED))})
            self.widget_list.update({"output": gui.FwEntry(self, "Output", f"{self.command_name}.out")})

        elif self.command == "opencv_threshold":
            self.widget_list.update({"src": gui.FwEntry(self, "Source", None)})
            self.widget_list.update({"dst": gui.FwEntry(self, "Destination", f"{self.command_name}.dst")})
            self.widget_list.update({"thresh": gui.FwScale(self, "Threshold", 0, 255, 150)})
            self.widget_list.update({"maxval": gui.FwScale(self, "Maximum value", 0, 255, 255)})
            self.widget_list.update({"type": gui.FwCombobox(self, "Type", tuple(ENUM_THRESHOLD_TYPES.keys()), tuple(ENUM_THRESHOLD_TYPES.values()).index(cv2.THRESH_BINARY))})

        elif self.command == "opencv_resize":
            self.widget_list.update({"src": gui.FwEntry(self, "Source", None)})
            self.widget_list.update({"dst": gui.FwEntry(self, "Destination", f"{self.command_name}.dst")})
            self.widget_list.update({"dsize_w": gui.FwScale(self, "Width", 0, 255, 0)})
            self.widget_list.update({"dsize_h": gui.FwScale(self, "Height", 0, 255, 0)})
            self.widget_list.update({"fx": gui.FwScale(self, "Factor x", 0, 1, 0.3, resolution=0.1)})
            self.widget_list.update({"fy": gui.FwScale(self, "Factor y", 0, 1, 0.3, resolution=0.1)})
            self.widget_list.update({"interpolation": gui.FwCombobox(self, "Interpolation", tuple(ENUM_INTERPOLATION_FLAGS.keys()), tuple(ENUM_INTERPOLATION_FLAGS.values()).index(cv2.INTER_NEAREST))})


    def get_values(self):
        values = {}
        for key, widget in self.widget_list.items():
            values.update({key: widget.get()})

        return values


    def print_values(self):
        print(self.get_values())