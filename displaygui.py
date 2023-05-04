import tkinter as tk
from tkinter import ttk
import widgets as wg
from enums import *
import mainwindow as mw


input_elements = {}
clipboard_io = None


class DisplayGui(ttk.Frame):
    def __init__(self, master, command_model):
        super().__init__(master=master)
        self.command_model = command_model
        self.widget_list = {}

        self.set()


    def set(self):
        if self.command_model.command_name.startswith("tk_display"):
            self.widget_list.update({"display": wg.FwImage(self, "Image")})

        frm_display_input = ttk.Frame(self)
        lbl_command_name = ttk.Label(self, text=self.command_model.command_name)
        frm_display_command = ttk.Frame(self)
        frm_display_output = ttk.Frame(self)

        frm_display_input.pack()
        lbl_command_name.pack()
        frm_display_command.pack()
        frm_display_output.pack()

        lbl_command_name.bind("<Button-1>", lambda event: self.show_setting_widget(self.command_model.command_name))

        for widget in self.widget_list.values():
            widget.pack()

        # bemenetek kirajzolása
        try:
            for input_key, input_value_name in self.command_model.parameters["input"].items():
                input_value = None
                if input_value_name is None:
                    input_value = "None"
                else:
                    input_value = input_value_name
                lbl_in = ttk.Label(frm_display_input, text=f"{input_key}: {input_value}")
                lbl_in.pack()
                lbl_in.bind("<Double-Button-1>", lambda event: self.paste_input(input_key))
                input_elements.update({f"{self.command_model.command_name}.{input_key}": lbl_in})
        except:
            pass

        # kimenetek kirajzolása
        try:
            for output_key, output_value_name in self.command_model.parameters["output"].items():
                output_value = None
                if output_value_name is None:
                    output_value = "None"
                else:
                    output_value = output_value_name
                lbl_out = ttk.Label(frm_display_output, text=f"{output_key}: {output_value}")
                lbl_out.pack()
                lbl_out.bind("<Double-Button-1>", lambda event: self.copy_output(output_value))
        except:
            pass


    def show_setting_widget(self, command_name):
        mw.setting_widgets_hide()
        mw.setting_widget_show(command_name)


    def copy_output(self, output_name):
        global clipboard_io
        clipboard_io = output_name


    def paste_input(self, input_key):
        if not bool(clipboard_io):
            print("Empty clipboard")
        else:
            self.command_model.parameters["input"][input_key] = clipboard_io
            print(input_elements.keys())
            input_elements[f"{self.command_model.command_name}.{input_key}"].config(text=f"{input_key}: {clipboard_io}")

        # TODO
        # kiszűrni a saját kimenetet, ne legyen a saját kimenet, a saját bemenet
