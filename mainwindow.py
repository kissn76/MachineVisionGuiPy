import cv2
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import command as com


used_command_list = {}  # a végrehajtandó parancsok object-jeit tartalmazza
preview_command = None

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

        self.available_commands = ["opencv_videocapture", "opencv_imread", "opencv_threshold", "opencv_gaussianblur", "opencv_resize", "opencv_canny", "tk_display"]
        self.image_list = {}
        self.run_contimous = False

        self.frm_config = ttk.Frame(self)

        frm_button = ttk.Frame(self.frm_config)
        ttk.Button(frm_button, text="Save", command=self.setting_save).grid(row=0, column=0)
        ttk.Button(frm_button, text="Run once", command=self.next_image).grid(row=0, column=1)
        self.btn_run_continous = ttk.Button(frm_button, text="Run continous", command=self.continous_run_start)
        self.btn_run_continous.grid(row=0, column=2)
        self.lbl_counter = ttk.Label(frm_button, text=process_counter)
        self.lbl_counter.grid(row=0, column=3)
        ttk.Button(frm_button, text="Stop", command=self.continous_run_stop).grid(row=0, column=4)

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
        self.preview_set()

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


    def preview_set(self):
        image = None
        if not bool(preview_command):
            image = "./resources/gears_400.jpg"
            if Path(image).is_file():
                image = cv2.imread(image)
        else:
            try:
                image = self.image_list[preview_command]
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

        if not bool(preview_command):
            name = "None"
        else:
            name = preview_command
        self.lbl_preview_name.configure(text=name)


    def setting_save(self):
        setting = {}
        # model setting
        for command_name, command_obj in used_command_list.items():
            model_input = command_obj.command_model.input
            model_output = command_obj.command_model.output
            model_setting = command_obj.command_model.setting
            model = {"input": model_input, "output": model_output, "setting": model_setting}
            setting.update({command_name: {"model": model}})

        # position of canvas elements
        for id in self.can_main.find_all():
            setting[self.can_main.gettags(id)[0]].update({"coords": self.can_main.coords(id)})

        print(setting)

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
        self.btn_run_continous.configure(state="disabled")
        self.next_image()


    def continous_run_stop(self):
        self.run_contimous = False
        self.btn_run_continous.configure(state="enabled")
        # global process_counter
        # process_counter = 0
        # self.lbl_counter.configure(text=process_counter)


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


    def next_image(self):
        # DEBUG
        global process_counter
        # print(process_counter, "run process")
        process_counter += 1
        self.lbl_counter.configure(text=process_counter)
        # DEBUG END

        self.image_list.clear()

        ##
        # Parancsok lefuttatása helyes sorrendben
        ##
        checked = {}
        def find_own_output(command_name, input_name):
            # megkeressük, hogy az input_name melyik parancs outputja
            parent_command_object = used_command_list[input_name[0:input_name.rfind('.')]]
            if bool(parent_command_object):
                if parent_command_object.command_model.command_name in checked[command_name]:
                    print("Az inputja ugyanaz, mint az outputja:", command_name)
                    return False
                else:
                    checked[command_name].append(parent_command_object.command_model.command_name)
                    for parent_command_input in parent_command_object.command_model.input.values():
                        ret = find_own_output(command_name, parent_command_input)
                        if not ret:
                            return False
            return True

        # 0. Hibák felderítése
        # 0.1 Megkeresünk minden olyan parancsot, amelyiknek nincs bemenete, de kéne, hogy legyen.
        for command_name, command_object in used_command_list.items():
            if None in command_object.command_model.input.values():
                print("Error - command has empty input:", command_name, "-", command_object.command_model.input)
                return False
        # 0.2 Megkeresünk minden olyan parancsot, amelyiknek az inputja a saját outputja, akár más parancsokon keresztűl is.
        for command_name, command_object in used_command_list.items():
            for command_input in command_object.command_model.input.values():
                checked.clear()
                checked.update({command_name: [command_name]})
                ret = find_own_output(command_name, command_input)
                if not ret:
                    return False
        #
        # 1. Input parancsok megkeresése, végrehejtása
        def find_child_commands(output_name):
            child_commands = []
            for command_object in used_command_list.values():
                if output_name in command_object.command_model.input.values():
                    child_commands.append(command_object.command_model.command_name)

            return child_commands


        # Input parancsok megkeresése, végrehejtása.
        # Az outputjaikat használó parancsok kigyűjtése.
        command_queue = []
        for command_name, command_object in used_command_list.items():
            if not bool(command_object.command_model.input):
                for output in command_object.command_model.output.values():
                    command_queue.extend(find_child_commands(output))
                command_object.command_model.run(self.image_list)
        # 2. Ha ennek a parancsnak egyéb inputja is van, ami még nem futott le, akkor várakozási sorba marad.
        # Ha minden inputja megvan, végrehajtjuk.
        # 3. A 2. pont iterálása, amíg minden parancs le nem futott.
        while len(command_queue) > 0:
            for command_name in command_queue:
                command_object = used_command_list[command_name]
                command_object_inputs = command_object.command_model.input.values()
                command_object_outputs = command_object.command_model.output.values()

                for output in command_object_outputs:
                    command_queue.extend(find_child_commands(output))

                if all(input in self.image_list.keys() for input in command_object_inputs): # ha a parancs összes inputja benne van a már létező parancskimenetek listájában
                    ret = command_object.command_model.run(self.image_list)
                    print(command_name)
                    if ret:
                        command_queue.remove(command_name)

        self.preview_set()

        if self.run_contimous:
            self.after(100, self.next_image)
