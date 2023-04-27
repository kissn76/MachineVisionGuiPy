import tkinter as tk
from tkinter import ttk
import commandframework as fw


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.images = {}

        # command = "opencv_imread"
        # # command = "opencv_resize"
        # # command = "opencv_threshold"
        # self.obj = fw.CommandGui(self, command)
        # self.obj.pack()






        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize", "tk_display"]
        self.command_counter = 0        # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
        self.used_command_list = {}     # a végrehajtandó parancsok object-jeit tartalmazza
        self.image_list = {}

        self.output_clipboard = None
        self.canvas_input_elements = {}

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

        # self.next_image()
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
        # hozzáadás a gui-hoz
        frm_row = tk.Frame(self.can_main)
        frm_input = tk.Frame(frm_row)
        frm_command = tk.Frame(frm_row)
        # btn_delete = ttk.Button(frm_row, text="t", width=1, command=lambda: self.used_command_del(command_name))
        frm_output = tk.Frame(frm_row)

        frm_input.grid(row=0, column=0)
        frm_command.grid(row=1, column=0)
        # btn_delete.grid(row=1, column=1)
        frm_output.grid(row=2, column=0)

        # hozzáadás a végrehajtási listához
        # setting = self.setting_get()

        frm_command_filling = fw.CommandGui(frm_command, command)
        frm_command_filling.pack()

        self.used_command_list.update({frm_command_filling.command_name: frm_command_filling})

        # frm_command_filling.bind("<Button-1>", lambda event: self.used_command_setting_form_show(command_name))

        # bemenetek kirajzolása
        # try:
        #     input_list = self.used_command_list[command_name].get_input()
        #     for input_key, input_value in input_list.items():
        #         if input_value is None:
        #             input_value = "None"
        #         lbl_in = tk.Label(frm_input, text=f"{input_key}: {input_value}")
        #         lbl_in.pack()
        #         lbl_in.bind("<Double-Button-1>", lambda event: self.paste_input(command_name, input_key))
        #         self.canvas_input_elements.update({f"{command_name}.{input_key}": lbl_in})
        # except:
        #     pass

        # kimenetek kirajzolása
        # try:
        #     output_list = self.used_command_list[command_name].get_output()
        #     for output_key, output_value in output_list.items():
        #         lbl_out = tk.Label(frm_output, text=f"{output_key}: {output_value}")
        #         lbl_out.pack()
        #         lbl_out.bind("<Double-Button-1>", lambda event: self.copy_output(output_value))
        # except:
        #     pass

        self.can_main.create_window(100, 100, window=frm_row, anchor="nw")







    # def next_image(self):
    #     # self.obj.print_values()
    #     self.obj.run(self.images)

    #     print(list(self.images.keys()))

    #     self.after(100, self.next_image)
