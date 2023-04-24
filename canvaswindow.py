import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize"]
        self.photoimage = None

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
        # self.can_main.bind('<Shift-1>', self.make_circle)
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

        self.can_main.addtag_withtag('selected', tk.CURRENT)


    def move_object(self, event):
        x, y = event.x, event.y
        self.can_main.coords('selected', x, y)


    def deselect_object(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')
        # self.can_main.bind('<Shift-1>', self.make_circle)


    def add_available_command_row(self, command):
        frm_row = tk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda event: self.add_used_command(command))
        frm_row.pack()


    def add_used_command(self, command):
        # photoimage = ImageTk.PhotoImage(Image.open("resources/example/ocv_1.jpg").reduce(4), size=(200, 200))
        # mainimage = self.can_main.create_image(1100, 50, anchor="ne", image=photoimage)
        # self.canvas_elements.append(photoimage)
        # self.canvas_elements.append(mainimage)

        # hozzáadás a gui-hoz
        frm_row = tk.Frame(self.can_main, bg="red")
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2", background="green")
        # btn_delete = ttk.Button(frm_row, text="t", width=1, command=lambda: self.del_command_row(command))
        # btn_move_up = ttk.Button(frm_row, text="u", width=1, command=lambda: self.move_up_command_row(command))
        # btn_move_down = ttk.Button(frm_row, text="d", width=1, command=lambda: self.move_down_command_row(command))
        lbl_command.grid(row=0, column=0)
        # btn_delete.grid(row=0, column=1)
        # btn_move_up.grid(row=0, column=2)
        # btn_move_down.grid(row=0, column=3)
        # lbl_command.bind("<Button-1>", lambda event: self.show_command_setting_form(command))
        # frm_row.pack(side=tk.S)
        self.can_main.create_window(100, 100, window=frm_row, height=100, anchor=tk.CENTER)

        self.canvas_elements.append(frm_row)