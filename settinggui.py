import tkinter as tk
from tkinter import ttk
import widgets as wg
from enums import *


class SettingGui(ttk.Frame):
    def __init__(self, master, command_model):
        super().__init__(master=master)
        self.command_model = command_model
        self.command_name = self.command_model.command_name
        self.widget_list = {}

        self.set()


    def set(self):
        input_list = {}
        output_list = {}
        setting_list = {}

        if self.command_name.startswith("opencv_imread"):
            # output_list = {"output": wg.FwEntry(self, "Output", f"{self.command_name}.out")}
            setting_list = {
                "filename": wg.FwEntry(self, "Filename", "./resources/example/ocv_1.jpg", state=None),
                "flags": wg.FwCombobox(self, "Flags", ENUM_IMREAD_MODES, tuple(ENUM_IMREAD_MODES.values()).index(cv2.IMREAD_UNCHANGED))
                }

        elif self.command_name.startswith("opencv_threshold"):
            # input_list = {"src": wg.FwEntry(self, "Source", None)}
            # output_list = {"dst": wg.FwEntry(self, "Destination", f"{self.command_name}.dst")}
            setting_list = {
                "thresh": wg.FwScale(self, "Threshold", 0, 255, 150),
                "maxval": wg.FwScale(self, "Maximum value", 0, 255, 255),
                "type": wg.FwCombobox(self, "Type", ENUM_THRESHOLD_TYPES, tuple(ENUM_THRESHOLD_TYPES.values()).index(cv2.THRESH_BINARY))
                }

        elif self.command_name.startswith("opencv_resize"):
            # input_list = {"src": wg.FwEntry(self, "Source", None)}
            # output_list = {"dst": wg.FwEntry(self, "Destination", f"{self.command_name}.dst")}
            setting_list = {
                "dsize_w": wg.FwScale(self, "Width", 0, 255, 0),
                "dsize_h": wg.FwScale(self, "Height", 0, 255, 0),
                "fx": wg.FwScale(self, "Factor x", 0, 1, 0.3, resolution=0.1),
                "fy": wg.FwScale(self, "Factor y", 0, 1, 0.3, resolution=0.1),
                "interpolation": wg.FwCombobox(self, "Interpolation", ENUM_INTERPOLATION_FLAGS, tuple(ENUM_INTERPOLATION_FLAGS.values()).index(cv2.INTER_NEAREST))
                }

        self.widget_list.update({"input": input_list})
        self.widget_list.update({"output": output_list})
        self.widget_list.update({"setting": setting_list})

        ttk.Label(self, text=self.command_name).pack()
        for widget in self.widget_list["setting"].values():
            if bool(widget):
                widget.pack()


    def get(self):
        for main_key in self.command_model.parameters.keys():
            for key in self.command_model.parameters[main_key].keys():
                try:
                    self.command_model.parameters[main_key][key] = self.widget_list[main_key][key].get()
                except:
                    pass
