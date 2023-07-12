import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class Settings():
    def __init__(self, filepath = "setting.json"):
        self.filepath = filepath
        self.can_main_width = 1000
        self.can_main_height = 800
        self.can_main_region_width = 4000
        self.can_main_region_height = 4000
        self.projects_opened = []
        self.backup_language = "en"
        self.system_language = self.backup_language
        self.setting_load()


    def setting_set(self, master):

        def send():
            self.can_main_width = self.ent_can_width.get()
            top.destroy()
            self.setting_save()

        top = tk.Toplevel(master)
        top.wm_attributes("-topmost", True)
        top.lift()
        top.grab_set()

        self.lbl_can_width = tk.Label(top, text="Canvas width")
        self.ent_can_width = ttk.Entry(top)
        self.ent_can_width.insert(0, self.can_main_width)

        self.btn_submit = tk.Button(top, text="Submit", command=send)

        self.lbl_can_width.grid(row=0, column=0)
        self.ent_can_width.grid(row=0, column=1)
        self.btn_submit.grid(row=1, column=0, columnspan=2)


    def setting_save(self):
        setting = {}
        setting.update({"system_language": self.system_language})

        canvas = {}
        canvas.update({"main_width": self.can_main_width})
        canvas.update({"main_height": self.can_main_height})
        canvas.update({"region_width": self.can_main_region_width})
        canvas.update({"region_height": self.can_main_region_height})
        setting.update({"canvas": canvas})

        projects = []
        for proj_name in self.projects_opened:
            proj = {}
            proj.update({"filepath": proj_name})
            projects.append(proj)
        setting.update({"projects": projects})

        with open(self.filepath, "w") as fp:
            json.dump(setting, fp, indent=4)


    def setting_load(self):
        setting = {}
        try:
            with open(self.filepath, "r") as fp:
                setting = json.load(fp)
        except:
            pass

        try:
            self.system_language = setting["system_language"]
        except:
            pass

        try:
            self.can_main_width = setting["canvas"]["main_width"]
        except:
            pass

        try:
            self.can_main_height = setting["canvas"]["main_height"]
        except:
            pass

        try:
            self.can_main_region_width = setting["canvas"]["region_width"]
        except:
            pass

        try:
            self.can_main_region_height = setting["canvas"]["region_height"]
        except:
            pass

        try:
            self.projects_opened = setting["projects"]
        except:
            pass