import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json

from opencvgui import *

# TODO
# a parancsok végrehajtási sorrendje a be és kimenetek láncolata alapján legyen
# az első egy input elem
# a második az, amelyiknek az input elem outputja az inputja :-)
# stb
#
# ennek a rendezése fusson le minden input beállítás után

class Mainwindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.available_commands = ["opencv_imread", "opencv_threshold", "opencv_resize", "tk_display"]
        self.command_counter = 0        # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs
        self.used_command_list = {}     # a végrehajtandó parancsok object-jeit tartalmazza
        self.image_list = {}

        self.output_clipboard = None
        self.canvas_input_elements = {}
        self.canvas_display_list = {}

        self.frm_config = tk.Frame(self)
        ttk.Button(self.frm_config, text="Save setting", command=self.settings_save).grid(row=0, column=0)
        self.frm_available_commands = tk.LabelFrame(self.frm_config, text="Available commands")
        self.frm_used_command_setting = tk.LabelFrame(self.frm_config, text="Command setting")

        self.frm_available_commands.grid(row=1, column=0)
        self.frm_used_command_setting.grid(row=2, column=0)

        self.frm_image = tk.Frame(self)
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


    def display_add(self, command_name):
        image = ImageTk.PhotoImage(Image.open("resources/gears_400.jpg"))
        ci = self.can_main.create_image(100, 100, image=image)

        self.canvas_display_list.update({command_name: {"object": ci, "src": None, "imagetk": image}})

        self.can_main.tag_bind(ci, "<Double-Button-1>", lambda event: self.display_paste_input(command_name))


    def display_refresh(self):
        for display_properties in self.canvas_display_list.values():
            try:
                image = self.image_list[display_properties["src"]]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                imagetk = ImageTk.PhotoImage(image=Image.fromarray(image))

                display_properties["imagetk"] = imagetk
                self.can_main.itemconfig(display_properties["object"], image=imagetk)
            except:
                pass


    def display_paste_input(self, display_name):
        if not bool(self.output_clipboard):
            print("Empty clipboard")
        else:
            self.canvas_display_list[display_name]["src"] = self.output_clipboard


    def available_command_row_add(self, command):
        frm_row = tk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=command, cursor= "hand2")
        lbl_command.pack()
        lbl_command.bind("<Double-Button-1>", lambda event: self.used_command_add(command))
        frm_row.pack()


    def used_command_add(self, command):
        command_name = f"{command}.{self.command_counter}"
        self.command_counter += 1

        # hozzáadás a végrehajtási listához
        setting = self.setting_get()
        if command_name.startswith("opencv_imread"):
            self.used_command_list[command_name] = ImreadGui(self.frm_used_command_setting, command_name)
        elif command_name.startswith("opencv_threshold"):
            self.used_command_list[command_name] = ThresholdGui(self.frm_used_command_setting, command_name)
        elif command_name.startswith("opencv_resize"):
            self.used_command_list[command_name] = ResizeGui(self.frm_used_command_setting, command_name)
        elif command_name.startswith("tk_display"):
            self.used_command_list[command_name] = TkDisplay(self.frm_used_command_setting, command_name)
            # self.display_add(command_name)

        try:
            self.used_command_list[command_name].set_setting(setting[command_name])
        except:
            pass

        # hozzáadás a gui-hoz
        frm_row = tk.Frame(self.can_main)
        frm_input = tk.Frame(frm_row)
        lbl_command = tk.Label(frm_row, text=command_name)
        btn_delete = ttk.Button(frm_row, text="t", width=1, command=lambda: self.used_command_del(command_name))
        frm_output = tk.Frame(frm_row)
        frm_input.grid(row=0, column=0)
        lbl_command.grid(row=1, column=0)
        btn_delete.grid(row=1, column=1)
        frm_output.grid(row=2, column=0)
        lbl_command.bind("<Button-1>", lambda event: self.used_command_setting_form_show(command_name))

        # bemenetek kirajzolása
        try:
            input_list = self.used_command_list[command_name].get_input()
            for input_key, input_value in input_list.items():
                if input_value is None:
                    input_value = "None"
                lbl_in = tk.Label(frm_input, text=f"{input_key}: {input_value}")
                lbl_in.pack()
                lbl_in.bind("<Double-Button-1>", lambda event: self.paste_input(command_name, input_key))
                self.canvas_input_elements.update({f"{command_name}.{input_key}": lbl_in})
        except:
            pass

        # kimenetek kirajzolása
        try:
            output_list = self.used_command_list[command_name].get_output()
            for output_key, output_value in output_list.items():
                lbl_out = tk.Label(frm_output, text=f"{output_key}: {output_value}")
                lbl_out.pack()
                lbl_out.bind("<Double-Button-1>", lambda event: self.copy_output(output_value))
        except:
            pass

        self.can_main.create_window(100, 100, window=frm_row, anchor="nw")


    def copy_output(self, output):
        self.output_clipboard = output


    def paste_input(self, command_name, input_key):
        if not bool(self.output_clipboard):
            print("Empty clipboard")
        else:
            self.used_command_list[command_name].input[input_key] = self.output_clipboard
            self.used_command_list[command_name].set_values()
            self.canvas_input_elements[f"{command_name}.{input_key}"].config(text=f"{input_key}: {self.output_clipboard}")

        # TODO
        # kiszűrni a saját kimenetet, ne legyen a saját kimenet, a saját bemenet


    def used_command_del(self, command):
        print("Delete:", command)
        # self.used_command_list.remove(command)


    def used_command_setting_form_show(self, command):
        for child in self.frm_used_command_setting.pack_slaves():
            child.pack_forget()

        # a szükséges (amelyikre kattintottunk) beállítás megjelenítése
        self.used_command_list[command].pack()


    def setting_load(self):
        try:
            with open("setting.json", "r") as fp:
                setting = json.load(fp)
        except:
            setting = {}

        return setting


    def setting_get(self):
        setting = {}
        for command_name, command_obj in self.used_command_list.items():
            try:
                setting.update({command_name: command_obj.get_setting()})
            except:
                pass
        return setting


    def settings_save(self):
        # TODO
        # canvas elemek mentése
        setting = self.setting_get()
        with open("setting.json", "w") as fp:
            json.dump(setting, fp)


    def next_image(self):
        for command_obj in self.used_command_list.values():
            try:
                command_obj.run_process(self.image_list)
            except:
                pass

        self.display_refresh()

        self.after(100, self.next_image)
