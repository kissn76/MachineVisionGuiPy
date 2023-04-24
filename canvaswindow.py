import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from opencvgui import *


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize"]
        self.command_counter = 0            # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
        self.used_command_list = []         # végrehajtási sor. A végrehajtandó parancsokat tartalmazza
        self.used_command_setting_list = {}  # a végrehajtandó parancsok object-jeit tartalmazza

        self.frm_config = tk.Frame(self)
        self.frm_available_commands = tk.Frame(self.frm_config)
        self.frm_used_command_setting = tk.Frame(self.frm_config)

        # ttk.Button(self.frm_available_commands, text="Reload GUI", command=self.reload_gui).pack()
        # ttk.Button(self.frm_available_commands, text="Save setting", command=self.save_settings).pack()
        ttk.Label(self.frm_available_commands, text="Available commands").pack()
        ttk.Label(self.frm_used_command_setting, text="Command setting").pack()

        self.frm_available_commands.grid(row=0, column=0)
        self.frm_used_command_setting.grid(row=1, column=0)

        self.frm_image = tk.Frame(self)
        self.can_main = tk.Canvas(self.frm_image, bg="blue", height=800, width=1200)
        self.can_main.pack()
        self.can_main.bind('<1>', self.select_object)
        self.selected = None

        self.frm_config.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_image.grid(row=0, column=1, sticky="n, s, w, e")

        # elérhető parancsok gui frame feltöltése
        for available_command in self.available_commands:
            self.add_available_command_row(available_command)

        self.canvas_elements = []

        self.mainloop()


    def select_object(self, event):
        self.can_main.bind('<Motion>', self.move_object)
        self.can_main.bind('<ButtonRelease-1>', self.deselect_object)
        # self.can_main.addtag_withtag('selected', tk.CURRENT)

        x, y = event.x, event.y
        self.can_main.addtag_closest('selected', x, y)


    def move_object(self, event):
        x, y = event.x, event.y
        self.can_main.coords('selected', x, y)


    def deselect_object(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')


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
        setting = self.get_setting()
        self.used_command_list.append(command_name)
        self.add_used_command_setting(command_name, setting)

        # hozzáadás a gui-hoz
        frm_row = tk.Frame(self.can_main)
        lbl_command = tk.Label(frm_row, text=command_name)
        btn_delete = ttk.Button(frm_row, text="t", width=1, command=lambda: self.del_command_row(command_name))
        frm_output = tk.Frame(frm_row)
        lbl_command.grid(row=0, column=0)
        btn_delete.grid(row=0, column=1)
        frm_output.grid(row=1, column=0)
        lbl_command.bind("<Button-1>", lambda event: self.show_command_setting_form(command_name))

        output_list = self.used_command_setting_list[command_name].get_output()
        for output in output_list:
            lbl_out = tk.Label(frm_output, text=output)
            lbl_out.pack()
            self.make_draggable(lbl_out)

        w = self.can_main.create_window(100, 100, window=frm_row, anchor="nw")
        self.canvas_elements.append(w)


    def make_draggable(self, widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        print(x, y)


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


    def del_command_row(self, command):
        print("Delete:", command)
        # self.used_command_list.remove(command)


    def show_command_setting_form(self, command):
        for child in self.frm_used_command_setting.pack_slaves():
            child.pack_forget()

        # a szükséges (amelyikre kattintottunk) beállítás megjelenítése
        self.used_command_setting_list[command].pack()


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