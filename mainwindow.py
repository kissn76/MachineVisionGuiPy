import cv2
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import commandmodel as cm
import command as com
import maincanvas as mc
import widgets as wg
import project
import settings


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.projects = {}
        self.project_directory = "projects"
        self.project_actual = None

        self.setting = settings.Settings()
        self.can_main_width = self.setting.can_main_width
        self.can_main_height = self.setting.can_main_height
        self.can_main_region_width = self.setting.can_main_region_width
        self.can_main_region_height = self.setting.can_main_region_height
        self.projects_opened = self.setting.projects_opened
        self.system_language = self.setting.system_language

        self.available_commands = ["opencv_videocapture", "opencv_imread", "opencv_threshold", "opencv_gaussianblur", "opencv_resize", "opencv_canny", "tk_display"]
        self.run_contimous = False

        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New project", command=self.project_add)
        filemenu.add_command(label="Open project", command=self.project_open)
        filemenu.add_command(label="Save project", command=self.project_save)
        filemenu.add_command(label="Save project as...", command=self.project_save_as)
        filemenu.add_command(label="Close project", command=self.project_close)
        filemenu.add_separator()
        filemenu.add_command(label="Settings", command=self.setting_set)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.config(menu=menubar)

        self.frm_config = ttk.Frame(self)
        self.frm_popup_id = None

        frm_button = ttk.Frame(self.frm_config)
        # ttk.Button(frm_button, text="Save", command=self.project_save).grid(row=0, column=0)
        # ttk.Button(frm_button, text="Run once", command=self.once_run).grid(row=0, column=1)
        # self.btn_run_continous = ttk.Button(frm_button, text="Run continous", command=self.continous_run_start)
        # self.btn_run_continous.grid(row=0, column=2)
        # self.lbl_counter = ttk.Label(frm_button, text=self.process_counter)
        # self.lbl_counter.grid(row=0, column=3)
        # ttk.Button(frm_button, text="Stop", command=self.continous_run_stop).grid(row=0, column=4)

        self.frm_available_commands = ttk.LabelFrame(self.frm_config, text="Available commands")
        self.frm_used_command_setting = ttk.LabelFrame(self.frm_config, text="Command setting")
        self.frm_used_command_queue = ttk.LabelFrame(self.frm_config, text="Command queue")

        self.frm_preview = ttk.LabelFrame(self.frm_config, text="Preview")
        self.lbl_preview_name = ttk.Label(self.frm_preview)
        self.lbl_preview = ttk.Label(self.frm_preview)

        frm_button.grid(row=0, column=0)
        self.frm_available_commands.grid(row=1, column=0)
        self.frm_used_command_setting.grid(row=2, column=0)
        self.frm_used_command_queue.grid(row=3, column=0)
        self.frm_preview.grid(row=4, column=0)

        self.lbl_preview_name.pack()
        self.lbl_preview.pack()

        self.frm_image = ttk.Frame(self)
        self.notebook = ttk.Notebook(self.frm_image)
        self.notebook.grid(row=0, column=0, sticky="n, s, w, e")

        self.frm_config.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_image.grid(row=0, column=1, sticky="n, s, w, e")

        self.frm_image.rowconfigure(0, weight=1)
        self.frm_image.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        self.notebook.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)

        # elérhető parancsok gui frame feltöltése
        for available_command in self.available_commands:
            def add(available_command):
                text_json = None
                label_text = None
                command_description = None
                with open("lang/commands_en.json", "r") as fp:
                    text_json = json.load(fp)
                try:
                    label_text = text_json[available_command]["name"][self.system_language]
                    command_description = text_json[available_command]["description"][self.system_language]
                except:
                    label_text = available_command
                frm_row = ttk.Frame(self.frm_available_commands)
                lbl_command = ttk.Label(frm_row, text=label_text, cursor= "hand2")
                lbl_info = wg.Info(frm_row, self, label_text, command_description)
                lbl_info.pack(side=tk.LEFT)
                lbl_command.pack(side=tk.LEFT)
                lbl_command.bind("<Double-Button-1>", lambda event: self.projects[self.project_actual].used_command_add(available_command))
                frm_row.pack(fill=tk.X, expand=True)

            add(available_command)

        # self.preview_set()

        # előzőleg elmentett munka betöltése
        # self.project_load()

        for proj in self.projects_opened:
            self.project_add(proj["filepath"])


    def preview_set(self):
        image = None
        if not bool(self.can_main.preview_command):
            image = "./resources/gears_400.jpg"
            if Path(image).is_file():
                image = cv2.imread(image)
        else:
            try:
                image = self.image_list[self.can_main.preview_command]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except:
                image = "./resources/gears_400.jpg"
                if Path(image).is_file():
                    image = cv2.imread(image)

        width = 240
        height = width * (image.shape[0] / image.shape[1])
        image = cv2.resize(image, dsize=(int(width), int(height)))

        imagetk = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.lbl_preview.configure(image=imagetk)
        self.lbl_preview.image = imagetk

        if not bool(self.can_main.preview_command):
            name = "None"
        else:
            name = self.can_main.preview_command
        self.lbl_preview_name.configure(text=name)


    def tab_changed(self, *args):
        tab_name = self.notebook.select()
        try:
            tab_text = self.notebook.tab(tab_name, "text")
            self.project_actual = tab_text
        except:
            self.project_actual = None


    def setting_set(self):
        self.setting.setting_set(self)


    def project_open(self):
        filepath = filedialog.askopenfilename(initialdir=self.project_directory, filetypes=[("Json files", "*.json")])
        self.project_add(filepath)


    def project_close(self):
        self.projects.pop(self.project_actual)
        self.project_actual = None
        self.notebook.forget(self.notebook.select())


    def project_save(self):
        proj_obj = self.projects[self.project_actual]
        if bool(proj_obj.filepath):
            proj_obj.project_save()
        else:
            new_filepath = filedialog.asksaveasfilename(initialdir=self.project_directory, title="Please select a file name for saving:", filetypes=[("Json files", "*.json")])
            if bool(new_filepath):
                proj_obj.filepath = new_filepath
                proj_obj.project_save()


    def project_save_as(self):
        proj_obj = self.projects[self.project_actual]
        new_filepath = filedialog.asksaveasfilename(initialdir=self.project_directory, title="Please select a file name for saving:", filetypes=[("Json files", "*.json")])
        if bool(new_filepath):
            proj_obj.filepath = new_filepath
            proj_obj.uuid_generate()
            proj_obj.project_save()
            self.notebook.tab(self.notebook.select(), text=proj_obj.project_uuid)


    def project_add(self, filepath=None):
        frm_can_main = ttk.Frame(self.notebook)
        proj_obj = project.Project(master=frm_can_main, filepath=filepath)
        can_main = proj_obj.can_main

        ok = False

        if not proj_obj.project_uuid in self.projects.keys():
            ok = True
        else:
            answer = messagebox.askokcancel("Question", "This project has already opened in another tab. Do you want to open it as new project (Ok), or Cancel?")
            if bool(answer):
                proj_obj.uuid_generate()
                proj_obj.filepath = None
                # új fájlnév létrehozása
                proj_obj.filepath = filedialog.asksaveasfilename(initialdir=self.project_directory, title="Please select a file name for saving:", filetypes=[("Json files", "*.json")])
                proj_obj.project_save()
                ok = True
            else:
                ok = False

        if bool(ok):
            can_main.grid(row=0, column=0, sticky="n, s, w, e")
            self.notebook.add(frm_can_main, text=proj_obj.project_uuid)
            self.projects.update({proj_obj.project_uuid: proj_obj})
