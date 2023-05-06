import tkinter as tk
from tkinter import ttk
import widgets as wg
from enums import *


class SettingGui(ttk.Frame):
    def __init__(self, master, command_model):
        super().__init__(master=master)
        self.command_model = command_model
        self.widget_list = {}

        self.init()


    def init(self):
        input_list = {}
        output_list = {}
        setting_list = {}

        if self.command_model.command_name.startswith("opencv_videocapture_index"):
            # output_list = {"output": wg.FwEntry(self, "Output", f"{self.command_model.command_name}.out")}
            setting_list = {
                "index": wg.FwEntry(self, "Index", self.command_model.parameters["setting"]["index"], state=None)
                }

        elif self.command_model.command_name.startswith("opencv_imread"):
            # output_list = {"output": wg.FwEntry(self, "Output", f"{self.command_model.command_name}.out")}
            setting_list = {
                "filename": wg.FwEntry(self, "Filename", self.command_model.parameters["setting"]["filename"], state=None),
                "flags": wg.FwCombobox(self, "Flags", ENUM_IMREAD_MODES, self.command_model.parameters["setting"]["flags"])
                }

        elif self.command_model.command_name.startswith("opencv_threshold"):
            # input_list = {"src": wg.FwEntry(self, "Source", None)}
            # output_list = {"dst": wg.FwEntry(self, "Destination", f"{self.command_model.command_name}.dst")}
            setting_list = {
                "thresh": wg.FwScale(self, "Threshold", 0, 255, self.command_model.parameters["setting"]["thresh"]),
                "maxval": wg.FwScale(self, "Maximum value", 0, 255, self.command_model.parameters["setting"]["maxval"]),
                "type": wg.FwCombobox(self, "Type", ENUM_THRESHOLD_TYPES, self.command_model.parameters["setting"]["type"])
                }

        elif self.command_model.command_name.startswith("opencv_gaussianblur"):
            setting_list = {
                "ksize_w": wg.FwScale(self, "Kernel size width", 0, 255, self.command_model.parameters["setting"]["ksize_w"], value_type=int),
                "ksize_h": wg.FwScale(self, "Kernel size height", 0, 255, self.command_model.parameters["setting"]["ksize_h"], value_type=int),
                "sigmaX": wg.FwScale(self, "Sigma x", 0, 1, self.command_model.parameters["setting"]["sigmaX"], resolution=0.1),
                "sigmaY": wg.FwScale(self, "Sigma y", 0, 1, self.command_model.parameters["setting"]["sigmaY"], resolution=0.1),
                "borderType": wg.FwCombobox(self, "Interpolation", ENUM_BORDERTYPES, self.command_model.parameters["setting"]["borderType"])
                }

        elif self.command_model.command_name.startswith("opencv_resize"):
            # input_list = {"src": wg.FwEntry(self, "Source", None)}
            # output_list = {"dst": wg.FwEntry(self, "Destination", f"{self.command_model.command_name}.dst")}
            setting_list = {
                "dsize_w": wg.FwScale(self, "Width", 0, 255, self.command_model.parameters["setting"]["dsize_w"], value_type=int),
                "dsize_h": wg.FwScale(self, "Height", 0, 255, self.command_model.parameters["setting"]["dsize_h"], value_type=int),
                "fx": wg.FwScale(self, "Factor x", 0, 1, self.command_model.parameters["setting"]["fx"], resolution=0.1),
                "fy": wg.FwScale(self, "Factor y", 0, 1, self.command_model.parameters["setting"]["fy"], resolution=0.1),
                "interpolation": wg.FwCombobox(self, "Interpolation", ENUM_INTERPOLATION_FLAGS, self.command_model.parameters["setting"]["interpolation"])
                }

        elif self.command_model.command_name.startswith("opencv_canny"):
            setting_list = {
                "threshold1": wg.FwScale(self, "Threshold 1", 0, 255, self.command_model.parameters["setting"]["threshold1"]),
                "threshold2": wg.FwScale(self, "Threshold 2", 0, 255, self.command_model.parameters["setting"]["threshold2"]),
                "apertureSize": wg.FwScale(self, "Aperture size", 0, 255, self.command_model.parameters["setting"]["apertureSize"], value_type=int),
                "L2gradient": wg.FwCheckbutton(self, "L2 gradient", "L2gradient", self.command_model.parameters["setting"]["L2gradient"])
                }

        self.widget_list.update({"input": input_list})
        self.widget_list.update({"output": output_list})
        self.widget_list.update({"setting": setting_list})

        ttk.Label(self, text=self.command_model.command_name).pack()
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
