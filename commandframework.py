import cv2
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import widgets as wg
from enums import *
import settinggui as sg
import displaygui as dg
import commandmodel as cm


command_counter = 0     # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
used_command_list = {}  # a végrehajtandó parancsok object-jeit tartalmazza


class Command():
    def __init__(self, command, setting_master, display_master):
        global command_counter
        self.command_name = f"{command}.{command_counter}"

        self.command_model = cm.CommandModel(self.command_name)

        used_command_list.update({self.command_name: self})

        # setting widget
        self.frm_setting_main = sg.SettingGui(setting_master, self.command_model)

        # display widget
        self.frm_display_main = dg.DisplayGui(display_master, self.command_model)


    def get_values(self):
        values = {}
        for main_key, widget_list in self.frm_setting_main.widget_list.items():
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
