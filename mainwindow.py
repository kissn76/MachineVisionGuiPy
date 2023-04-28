import tkinter as tk
from tkinter import ttk
import commandframework as fw


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.images = {}

        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize", "tk_display"]
        self.image_list = {}

        self.frm_config = ttk.Frame(self)
        # ttk.Button(self.frm_config, text="Save setting", command=self.settings_save).grid(row=0, column=0)
        self.frm_available_commands = ttk.LabelFrame(self.frm_config, text="Available commands")
        self.frm_used_command_setting = ttk.LabelFrame(self.frm_config, text="Command setting")

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
        # setting = self.load_setting()
        # if bool(setting):
        #     self.used_command_list = list(setting.keys())

        # max_counter = 0
        # for command in self.used_command_list:
        #     counter = int(command[command.rfind(".") + 1:]) + 1
        #     if counter > max_counter:
        #         max_counter = counter
        # self.command_counter = max_counter
        # TODO
        # előző canvas elemek betöltése

        self.next_image()
        self.mainloop()


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


    def available_command_row_add(self, command):
        frm_row = ttk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda event: self.used_command_add(command))
        frm_row.pack()


    def used_command_add(self, command):
        command_obj = fw.Command(command)
        command_obj.get_setting_widget(self.frm_used_command_setting).pack()

        # hozzáadás a végrehajtási listához
        # setting = self.setting_get()
        frm_command = command_obj.get_display_widget(self.can_main)

        self.can_main.create_window(100, 100, window=frm_command, anchor="nw")
        command_obj.show_setting_widget()


    def next_image(self):
        for command_name, command_object in fw.used_command_list.items():
            # print(command_name, command_object.print_values())
            command_object.run(self.image_list)

        # print(self.image_list.keys())

        self.after(100, self.next_image)
