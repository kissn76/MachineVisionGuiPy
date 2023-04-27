from PIL import Image, ImageTk
import cv2
from numpy import size
import tkinter as tk
import json

from opencvgui import *


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize"]
        self.command_counter = 0            # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
        self.used_command_list = []         # végrehajtási sor. A végrehajtandó parancsokat tartalmazza
        self.used_command_setting_list = {}  # a végrehajtandó parancsok object-jeit tartalmazza
        self.used_command_list_row = {}     # CommandRow objektumokat (végrehajtandó parancsok) tartalmazza
        self.image_list = {}                # a parancsok outputjaként létrehozott image-eket tartalmazza
        self.image_show = None


        self.title("Machine Vision GUI")
        self.geometry("1280x700")
        # self.attributes("-fullscreen", True)
        # self.attributes("-zoomed", True)

        self.frm_config = tk.Frame(self)
        self.frm_available_commands = tk.Frame(self.frm_config)
        self.frm_used_command_list = tk.Frame(self.frm_config)
        self.frm_used_command_setting = tk.Frame(self.frm_config)

        ttk.Button(self.frm_available_commands, text="Reload GUI", command=self.reload_gui).pack()
        ttk.Button(self.frm_available_commands, text="Save setting", command=self.save_settings).pack()
        ttk.Label(self.frm_available_commands, text="Available commands").pack()
        ttk.Label(self.frm_used_command_list, text="Used commands").pack()
        ttk.Label(self.frm_used_command_setting, text="Command setting").pack()

        self.frm_available_commands.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_used_command_list.grid(row=0, column=1)
        self.frm_used_command_setting.grid(row=1, column=1)

        self.frm_image = tk.Frame(self)
        self.frm_image_list = tk.Frame(self.frm_image)
        self.lbl_image = ttk.Label(self.frm_image)
        self.frm_image_list.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_image.grid(row=0, column=1, sticky="n, s, w, e")

        self.frm_config.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_image.grid(row=0, column=1, sticky="n, s, w, e")

        # elérhető parancsok gui frame feltöltése
        for available_command in self.available_commands:
            self.add_available_command_row(available_command)

        # előzőleg elmentett munka betöltése
        setting = self.load_setting()
        if bool(setting):
            self.used_command_list = list(setting.keys())

        max_counter = 0
        for command in self.used_command_list:
            counter = int(command[command.rfind(".") + 1:]) + 1
            if counter > max_counter:
                max_counter = counter
        self.command_counter = max_counter

        self.reload_ui(setting)

        self.next_image()

        self.mainloop()


    def add_available_command_row(self, command):
        frm_row = tk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda event: self.add_used_command(command))
        frm_row.pack()


    def add_used_command(self, command):
        command_name = f"{command}.{self.command_counter}"
        self.command_counter += 1

        # hozzáadás a végrehajtási listához
        self.used_command_list.append(command_name)

        setting = self.get_setting()
        self.reload_ui(setting)


    def reload_gui(self):
        setting = self.get_setting()
        self.reload_ui(setting)


    def reload_ui(self, setting):
        self.reload_frm_used_command_setting(setting)
        self.reload_frm_used_command_list()
        self.reload_frm_image_list()


    def reload_frm_used_command_list(self):
        for child in self.frm_used_command_list.pack_slaves():
            child.pack_forget()
            child.destroy()

        self.used_command_list_row.clear()

        for command in self.used_command_list:
            self.add_used_command_list_row(command)


    def reload_frm_used_command_setting(self, setting):
        for child in self.frm_used_command_setting.pack_slaves():
            child.pack_forget()
            child.destroy()

        self.used_command_setting_list.clear()

        for command in self.used_command_list:
            self.add_used_command_setting(command, setting)


    def add_used_command_list_row(self, command):
        # hozzáadás a gui-hoz
        frm_row = tk.Frame(self.frm_used_command_list, bg="red")
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2", background="green")
        btn_delete = ttk.Button(frm_row, text="t", width=1, command=lambda: self.del_command_row(command))
        btn_move_up = ttk.Button(frm_row, text="u", width=1, command=lambda: self.move_up_command_row(command))
        btn_move_down = ttk.Button(frm_row, text="d", width=1, command=lambda: self.move_down_command_row(command))
        lbl_command.grid(row=0, column=0)
        btn_delete.grid(row=0, column=1)
        btn_move_up.grid(row=0, column=2)
        btn_move_down.grid(row=0, column=3)
        lbl_command.bind("<Button-1>", lambda event: self.show_command_setting_form(command))
        frm_row.pack()


    def add_used_command_setting(self, command, setting):
        if command.startswith("opencv_imread"):
            self.used_command_setting_list[command] = ImreadGui(self.frm_used_command_setting, command)
        elif command.startswith("opencv_threshold"):
            self.used_command_setting_list[command] = ThresholdGui(self.frm_used_command_setting, command)
        elif command.startswith("opencv_resize"):
            self.used_command_setting_list[command] = ResizeGui(self.frm_used_command_setting, command)

        try:
            self.used_command_setting_list[command].set_setting(setting[command])
        except:
            pass


    def reload_frm_image_list(self):
        for child in self.frm_image_list.pack_slaves():
            child.pack_forget()
            child.destroy()

        for image_name in self.image_list.keys():
            self.add_image_list_row(image_name)

        self.image_list.clear()
        self.image_show = None


    def add_image_list_row(self, image_name):
        frm_row = tk.Frame(self.frm_image_list)
        lbl_command = ttk.Label(frm_row, text=image_name, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Button-1>", lambda event: self.set_image_show(image_name))
        frm_row.pack()


    def del_command_row(self, command):
        self.used_command_list.remove(command)
        setting = self.get_setting()
        self.reload_ui(setting)


    def move_up_command_row(self, command):
        command_index = self.used_command_list.index(command)
        self.used_command_list.insert(command_index - 1, self.used_command_list.pop(command_index))
        setting = self.get_setting()
        self.reload_ui(setting)


    def move_down_command_row(self, command):
        command_index = self.used_command_list.index(command)
        self.used_command_list.insert(command_index + 1, self.used_command_list.pop(command_index))
        setting = self.get_setting()
        self.reload_ui(setting)


    def show_command_setting_form(self, command):
        for child in self.frm_used_command_setting.pack_slaves():
            child.pack_forget()

        # a szükséges (amelyikre kattintottunk) beállítás megjelenítése
        self.used_command_setting_list[command].pack()
        self.used_command_setting_list[command].set_src_list(self.image_list)
        self.reload_frm_image_list()


    def set_image_show(self, image_name):
        self.image_show = image_name


    def next_image(self):
        self.image_list.clear()

        for command in self.used_command_list:
            try:
                self.used_command_setting_list[command].run_process(self.image_list)
            except:
                pass

        # self.set_image_list_frame()

        try:
            image = None
            if self.image_show is None:
                image = list(self.image_list.values())[-1]
            else:
                image = self.image_list[self.image_show]

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im)
            self.lbl_image.configure(image=imgtk)
            self.lbl_image.image = imgtk
        except:
            pass
        self.after(100, self.next_image)


    def load_setting(self):
        try:
            with open("setting.json", "r") as fp:
                setting = json.load(fp)
        except:
            setting = {}

        return setting


    def get_setting(self):
        setting = {}
        for command in self.used_command_list:
            try:
                command_setting = self.used_command_setting_list[command].get_setting()
                setting.update({command: command_setting})
            except:
                pass
        return setting


    def save_settings(self):
        setting = self.get_setting()
        with open("setting.json", "w") as fp:
            json.dump(setting, fp)
