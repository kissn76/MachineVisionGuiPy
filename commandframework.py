import cv2
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import widgets as wg
from enums import *


command_counter = 0     # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
used_command_list = {}  # a végrehajtandó parancsok object-jeit tartalmazza
clipboard_io = None
input_elements = {}


class Command():
    def __init__(self, command):
        global command_counter

        self.command_name = f"{command}.{command_counter}"
        command_counter += 1
        self.setting_widget_list = {}
        self.display_widget_list = {}
        self.run = None

        self.frm_main_setting = None

        used_command_list.update({self.command_name: self})

        # display widget
        self.frm_display_main = None
        self.frm_display_input = None
        self.frm_display_command = None
        self.frm_display_output = None


    def get_setting_widget(self, master=None):
        if not bool(self.frm_main_setting):
            self.frm_main_setting = ttk.Frame(master)
            ttk.Label(self.frm_main_setting, text=self.command_name).pack()

            if not bool(self.setting_widget_list):
                self.setting_widget_list_set()

                for widget in self.setting_widget_list.values():
                    if bool(widget) and isinstance(widget, ttk.Frame):
                        widget.pack()

        return self.frm_main_setting


    def get_display_widget(self, master=None):
        if not bool(self.frm_display_main):
            self.frm_display_main = ttk.Frame(master)
            self.frm_display_input = ttk.Frame(self.frm_display_main)
            lbl_command_name = ttk.Label(self.frm_display_main, text=self.command_name)
            self.frm_display_command = ttk.Frame(self.frm_display_main)
            self.frm_display_output = ttk.Frame(self.frm_display_main)

            self.frm_display_input.pack()
            lbl_command_name.pack()
            self.frm_display_command.pack()
            self.frm_display_output.pack()

            lbl_command_name.bind("<Button-1>", lambda event: self.show_setting_widget())

            if not bool(self.display_widget_list):
                self.display_widget_list_set()

                for widget in self.display_widget_list.values():
                    if bool(widget) and isinstance(widget, ttk.Frame):
                        widget.pack()


            # bemenetek kirajzolása
            try:
                for input_key, input_value_obj in self.setting_widget_list["input"].items():
                    input_value = None
                    if input_value_obj is None:
                        input_value = "None"
                    else:
                        input_value = input_value_obj.get()
                    lbl_in = ttk.Label(self.frm_display_input, text=f"{input_key}: {input_value}")
                    lbl_in.pack()
                    lbl_in.bind("<Double-Button-1>", lambda event: self.paste_input(input_key))
                    input_elements.update({f"{self.command_name}.{input_key}": lbl_in})
            except:
                pass

            # kimenetek kirajzolása
            try:
                for output_key, output_value_obj in self.setting_widget_list["output"].items():
                    output_value = None
                    if output_value_obj is None:
                        output_value = "None"
                    else:
                        output_value = output_value_obj.get()
                    lbl_out = ttk.Label(self.frm_display_output, text=f"{output_key}: {output_value}")
                    lbl_out.pack()
                    lbl_out.bind("<Double-Button-1>", lambda event: self.copy_output(output_value))
            except:
                pass

        return self.frm_display_main


    def show_setting_widget(self):
        for command_obj in used_command_list.values():
            command_obj.frm_main_setting.pack_forget()

        self.frm_main_setting.pack()


    def copy_output(self, output_name):
        global clipboard_io
        clipboard_io = output_name


    def paste_input(self, input_key):
        if not bool(clipboard_io):
            print("Empty clipboard")
        else:
            self.setting_widget_list["input"][input_key].set(clipboard_io)
            input_elements[f"{self.command_name}.{input_key}"].config(text=f"{input_key}: {clipboard_io}")

        # TODO
        # kiszűrni a saját kimenetet, ne legyen a saját kimenet, a saját bemenet


    def display_widget_list_set(self):
        if self.command_name.startswith("tk_display"):
            self.display_widget_list.update({"display": wg.FwImage(self.frm_display_command, "Image")})

            def run_command(images):
                src = self.setting_widget_list["input"]["src"].get()
                display_obj = self.display_widget_list["display"]

                if bool(src) and len(images["src"]) > 0:
                    image = None
                    try:
                        display_obj.set(images["src"])
                        return True
                    except:
                        pass

                return False

            self.run = run_command


    def setting_widget_list_set(self):
        if self.command_name.startswith("opencv_imread"):
            input_list = None
            output_list = {"output": wg.FwEntry(self.frm_main_setting, "Output", f"{self.command_name}.out")}
            setting_list = {
                "filename": wg.FwEntry(self.frm_main_setting, "Filename", "./resources/example/ocv_1.jpg", state=None),
                "flags": wg.FwCombobox(self.frm_main_setting, "Flags", ENUM_IMREAD_MODES, tuple(ENUM_IMREAD_MODES.values()).index(cv2.IMREAD_UNCHANGED))
                }

            self.setting_widget_list.update({"input": input_list})
            self.setting_widget_list.update({"output": output_list})
            self.setting_widget_list.update({"setting": setting_list})

            def run_command(images):
                filename = self.setting_widget_list["setting"]["filename"].get()
                flags = self.setting_widget_list["setting"]["flags"].get()
                output = self.setting_widget_list["output"]["output"].get()

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
            input_list = {"src": wg.FwEntry(self.frm_main_setting, "Source", None)}
            output_list = {"dst": wg.FwEntry(self.frm_main_setting, "Destination", f"{self.command_name}.dst")}
            setting_list = {
                "thresh": wg.FwScale(self.frm_main_setting, "Threshold", 0, 255, 150),
                "maxval": wg.FwScale(self.frm_main_setting, "Maximum value", 0, 255, 255),
                "type": wg.FwCombobox(self.frm_main_setting, "Type", ENUM_THRESHOLD_TYPES, tuple(ENUM_THRESHOLD_TYPES.values()).index(cv2.THRESH_BINARY))
                }

            self.setting_widget_list.update({"input": input_list})
            self.setting_widget_list.update({"output": output_list})
            self.setting_widget_list.update({"setting": setting_list})

            def run_command(images):
                src = self.setting_widget_list["input"]["src"].get()
                dst = self.setting_widget_list["output"]["dst"].get()
                thresh = self.setting_widget_list["setting"]["thresh"].get()
                maxval = self.setting_widget_list["setting"]["maxval"].get()
                type = self.setting_widget_list["setting"]["type"].get()

                print("b", images.keys())

                try:
                    if bool(src) and len(images[src]) > 0:
                        image = None
                        try:
                            print("run")
                            _, image = cv2.threshold(images[src], thresh, maxval, type)
                            # image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                            print("a", images.keys())
                            images.update({dst: image})
                            return True
                        except:
                            pass
                except:
                    pass

                return False

            self.run = run_command

        elif self.command_name.startswith("opencv_resize"):
            input_list = {"src": wg.FwEntry(self.frm_main_setting, "Source", None)}
            output_list = {"dst": wg.FwEntry(self.frm_main_setting, "Destination", f"{self.command_name}.dst")}
            setting_list = {
                "dsize_w": wg.FwScale(self.frm_main_setting, "Width", 0, 255, 0),
                "dsize_h": wg.FwScale(self.frm_main_setting, "Height", 0, 255, 0),
                "fx": wg.FwScale(self.frm_main_setting, "Factor x", 0, 1, 0.3, resolution=0.1),
                "fy": wg.FwScale(self.frm_main_setting, "Factor y", 0, 1, 0.3, resolution=0.1),
                "interpolation": wg.FwCombobox(self.frm_main_setting, "Interpolation", ENUM_INTERPOLATION_FLAGS, tuple(ENUM_INTERPOLATION_FLAGS.values()).index(cv2.INTER_NEAREST))
                }

            self.setting_widget_list.update({"input": input_list})
            self.setting_widget_list.update({"output": output_list})
            self.setting_widget_list.update({"setting": setting_list})

            def run_command(images):
                src = self.setting_widget_list["input"]["src"].get()
                dst = self.setting_widget_list["output"]["dst"].get()
                dsize_w = self.setting_widget_list["setting"]["dsize_w"].get()
                dsize_h = self.setting_widget_list["setting"]["dsize_h"].get()
                fx = self.setting_widget_list["setting"]["fx"].get()
                fy = self.setting_widget_list["setting"]["fy"].get()
                interpolation = self.setting_widget_list["setting"]["interpolation"].get()

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
            input_list = {"src": wg.FwEntry(self.frm_main_setting, "Source", None)}
            output_list = None
            setting_list = None

            self.setting_widget_list.update({"input": input_list})
            self.setting_widget_list.update({"output": output_list})
            self.setting_widget_list.update({"setting": setting_list})

            def run_command(images):
                src = self.setting_widget_list["input"]["src"].get()
                display_obj = self.display_widget_list["display"]

                if bool(src) and len(images["src"]) > 0:
                    image = None
                    try:
                        display_obj.set(images["src"])
                        return True
                    except:
                        pass

                return False

            self.run = run_command


    def get_values(self):
        values = {}
        for main_key, widget_list in self.setting_widget_list.items():
            d = {}
            if not widget_list is None:
                for key, widget in widget_list.items():
                    value = widget.get()
                    d.update({key: value})
            else:
                d = None

            values.update({main_key: d})

        return values


    def print_values(self):
        print(self.get_values())
