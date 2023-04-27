import cv2
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import widgets as wg
from enums import *


command_counter = 0


class Command():
    def __init__(self, command):
        global command_counter

        self.command_name = f"{command}.{command_counter}"
        command_counter += 1
        self.setting_widget_list = {}
        self.display_widget_list = {}
        self.run = None

        self.frm_main_setting = None
        self.frm_main_display = None


    def get_setting_widget(self, master):
        self.frm_main_setting = ttk.Frame(master)
        self.widget_list_set()

        ttk.Label(self.frm_main_setting, text=self.command_name).pack()
        for widget in self.setting_widget_list.values():
            widget.pack()

        return self.frm_main_setting


    def get_display_widget(self, master):
        self.frm_main_display = ttk.Frame(master)
        frm_input = tk.Frame(self.frm_main_display)
        lbl_command_name = ttk.Label(self.frm_main_display, text=self.command_name)
        # btn_delete = ttk.Button(self.frm_main_display, text="t", width=1, command=lambda: self.used_command_del(command_name))
        frm_output = tk.Frame(self.frm_main_display)

        frm_input.pack()
        lbl_command_name.pack()
        # btn_delete.grid(row=1, column=1)
        frm_output.pack()

        return self.frm_main_display


    def widget_list_set(self):
        if self.command_name.startswith("opencv_imread"):
            self.setting_widget_list.update({"filename": wg.FwEntry(self.frm_main_setting, "Filename", "./resources/example/ocv_1.jpg", state=None)})
            self.setting_widget_list.update({"flags": wg.FwCombobox(self.frm_main_setting, "Flags", ENUM_IMREAD_MODES, tuple(ENUM_IMREAD_MODES.values()).index(cv2.IMREAD_UNCHANGED))})
            self.setting_widget_list.update({"output": wg.FwEntry(self.frm_main_setting, "Output", f"{self.command_name}.out")})

            def run_command(images):
                filename = self.setting_widget_list["filename"].get()
                flags = self.setting_widget_list["flags"].get()
                output = self.setting_widget_list["output"].get()

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
            self.setting_widget_list.update({"src": wg.FwEntry(self.frm_main_setting, "Source", None)})
            self.setting_widget_list.update({"dst": wg.FwEntry(self.frm_main_setting, "Destination", f"{self.command_name}.dst")})
            self.setting_widget_list.update({"thresh": wg.FwScale(self.frm_main_setting, "Threshold", 0, 255, 150)})
            self.setting_widget_list.update({"maxval": wg.FwScale(self.frm_main_setting, "Maximum value", 0, 255, 255)})
            self.setting_widget_list.update({"type": wg.FwCombobox(self.frm_main_setting, "Type", ENUM_THRESHOLD_TYPES, tuple(ENUM_THRESHOLD_TYPES.values()).index(cv2.THRESH_BINARY))})

            def run_command(images):
                src = self.setting_widget_list["src"].get()
                dst = self.setting_widget_list["dst"].get()
                thresh = self.setting_widget_list["thresh"].get()
                maxval = self.setting_widget_list["maxval"].get()
                type = self.setting_widget_list["type"].get()

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
            self.setting_widget_list.update({"src": wg.FwEntry(self.frm_main_setting, "Source", None)})
            self.setting_widget_list.update({"dst": wg.FwEntry(self.frm_main_setting, "Destination", f"{self.command_name}.dst")})
            self.setting_widget_list.update({"dsize_w": wg.FwScale(self.frm_main_setting, "Width", 0, 255, 0)})
            self.setting_widget_list.update({"dsize_h": wg.FwScale(self.frm_main_setting, "Height", 0, 255, 0)})
            self.setting_widget_list.update({"fx": wg.FwScale(self.frm_main_setting, "Factor x", 0, 1, 0.3, resolution=0.1)})
            self.setting_widget_list.update({"fy": wg.FwScale(self.frm_main_setting, "Factor y", 0, 1, 0.3, resolution=0.1)})
            self.setting_widget_list.update({"interpolation": wg.FwCombobox(self.frm_main_setting, "Interpolation", ENUM_INTERPOLATION_FLAGS, tuple(ENUM_INTERPOLATION_FLAGS.values()).index(cv2.INTER_NEAREST))})

            def run_command(images):
                src = self.setting_widget_list["src"].get()
                dst = self.setting_widget_list["dst"].get()
                dsize_w = self.setting_widget_list["dsize_w"].get()
                dsize_h = self.setting_widget_list["dsize_h"].get()
                fx = self.setting_widget_list["fx"].get()
                fy = self.setting_widget_list["fy"].get()
                interpolation = self.setting_widget_list["interpolation"].get()

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
            self.setting_widget_list.update({"src": wg.FwEntry(self.frm_main_setting, "Source", None)})
            self.setting_widget_list.update({"display": wg.FwImage(self.frm_main_setting, "Image")})

            def run_command(images):
                display_obj = self.setting_widget_list["display"]

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
        for key, widget in self.setting_widget_list.items():
            values.update({key: widget.get()})

        return values


    def print_values(self):
        print(self.get_values())
