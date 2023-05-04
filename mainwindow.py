import tkinter as tk
from tkinter import ttk
import json
import command as com


used_command_list = {}  # a végrehajtandó parancsok object-jeit tartalmazza

# DEBUG
process_counter = 0     # élesben nem kell
# DEBUG END


def setting_widgets_hide():
    for command_obj in used_command_list.values():
        command_obj.frm_setting_main.pack_forget()


def setting_widget_show(command_name):
    used_command_list[command_name].frm_setting_main.pack()


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_gaussianblur", "opencv_resize", "opencv_canny", "tk_display"]
        self.image_list = {}
        self.run_contimous = False

        self.frm_config = ttk.Frame(self)
        self.frm_available_commands = ttk.LabelFrame(self.frm_config, text="Available commands")
        self.frm_used_command_setting = ttk.LabelFrame(self.frm_config, text="Command setting")

        frm_button = ttk.Frame(self.frm_config)
        ttk.Button(frm_button, text="Save", command=self.setting_save).grid(row=0, column=0)
        ttk.Button(frm_button, text="Run once", command=self.next_image).grid(row=0, column=1)
        ttk.Button(frm_button, text="Run continous", command=self.continous_run_start).grid(row=0, column=2)
        ttk.Button(frm_button, text="Stop", command=self.continous_run_stop).grid(row=0, column=3)

        frm_button.grid(row=0, column=0)
        self.frm_available_commands.grid(row=1, column=0)
        self.frm_used_command_setting.grid(row=2, column=0)

        self.frm_image = ttk.Frame(self)
        self.can_main = tk.Canvas(self.frm_image, bg="blue", height=800, width=1200)
        self.can_main.pack()
        self.can_main.bind('<Button-1>', self.dnd_select_object)

        self.frm_config.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_image.grid(row=0, column=1, sticky="n, s, w, e")

        # elérhető parancsok gui frame feltöltése
        for available_command in self.available_commands:
            self.available_command_row_add(available_command)

        # előzőleg elmentett munka betöltése
        setting = self.setting_load()
        if bool(setting):
            for command_name, command_setting in setting.items():
                self.used_command_add(command_name, command_setting)

        self.mainloop()


    def setting_save(self):
        setting = {}
        # model setting
        for command_name, command_obj in used_command_list.items():
            setting.update({command_name: {"model": command_obj.command_model.parameters}})

        # position of canvas elements
        for id in self.can_main.find_all():
            setting[self.can_main.gettags(id)[0]].update({"coords": self.can_main.coords(id)})

        with open("setting.json", "w") as fp:
            json.dump(setting, fp, indent=4)


    def setting_load(self):
        try:
            with open("setting.json", "r") as fp:
                setting = json.load(fp)
        except:
            setting = {}

        return setting


    def continous_run_start(self):
        self.run_contimous = True
        self.next_image()


    def continous_run_stop(self):
        self.run_contimous = False


    # DRAG & DROP metódusok
    def dnd_select_object(self, event):
        self.can_main.bind('<Motion>', self.dnd_move_object)
        self.can_main.bind('<ButtonRelease-1>', self.dnd_deselect_object)

        x, y = event.x, event.y
        self.can_main.addtag_closest('selected', x, y)


    def dnd_move_object(self, event):
        x, y = event.x, event.y
        self.can_main.coords('selected', x, y)


    def dnd_deselect_object(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')
    # DRAG & DROP metódusok END


    def available_command_row_add(self, command):
        frm_row = ttk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda event: self.used_command_add(command))
        frm_row.pack()


    def used_command_add(self, command, setting=None):
        coords = None
        if bool(setting):   # ha dict-ből töltünk be meglévő adatokat, tipikusan mentés visszatöltésekor
            model_setting = setting["model"]
            coords = setting["coords"]
            command_obj = com.Command(command, self.frm_used_command_setting, self.can_main, setting=model_setting)
        else:   # új létrehozása
            command_obj = com.Command(command, self.frm_used_command_setting, self.can_main)

        # hozzáadás a végrehajtási listához
        used_command_list.update({command_obj.command_model.command_name: command_obj})

        # display hozzáadás a canvas-hoz
        frm_command = command_obj.frm_display_main
        id = self.can_main.create_window(100, 100, window=frm_command, anchor="nw")
        self.can_main.addtag_withtag(command_obj.command_model.command_name, id)    # a canvas elem tag-ként megkapja a command_name-et, hogy egyedileg meghívható legyen később
        # ha betöltött elem, akkor mozgatás a mentett pozícióba a canvas-on
        if bool(setting):
            self.can_main.moveto(id, coords[0], coords[1])


    def used_command_list_reorder(self):
        pass


    def next_image(self):
        # DEBUG
        # global process_counter
        # print(process_counter, "run process")
        # process_counter += 1
        # DEBUG END

        self.image_list.clear()
        for command_object in used_command_list.values():
            command_object.run(self.image_list)

        if self.run_contimous:
            self.after(100, self.next_image)
