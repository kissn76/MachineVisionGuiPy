import cv2
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import commandcontainer as cc
import command as com
import maincanvas as mc
import widgets as wg


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.system_language = "hu"
        self.backup_language = "en"

        self.can_main_width = 1000
        self.can_main_height = 800
        self.can_main_region_width = 4000
        self.can_main_region_height = 4000

        self.available_commands = ["opencv_videocapture", "opencv_imread", "opencv_threshold", "opencv_gaussianblur", "opencv_resize", "opencv_canny", "tk_display"]
        self.image_list = {}
        self.run_contimous = False
        self.process_counter = 0

        self.command_container = cc.CommandContainer()
        self.command_queue = []

        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=())
        filemenu.add_command(label="Open", command=())
        filemenu.add_command(label="Save", command=())
        filemenu.add_command(label="Save as...", command=())
        filemenu.add_command(label="Close", command=())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=())
        menubar.add_cascade(label="File", menu=filemenu)

        self.config(menu=menubar)

        self.frm_config = ttk.Frame(self)
        self.frm_popup_id = None

        frm_button = ttk.Frame(self.frm_config)
        ttk.Button(frm_button, text="Save", command=self.setting_save).grid(row=0, column=0)
        ttk.Button(frm_button, text="Run once", command=self.once_run).grid(row=0, column=1)
        self.btn_run_continous = ttk.Button(frm_button, text="Run continous", command=self.continous_run_start)
        self.btn_run_continous.grid(row=0, column=2)
        self.lbl_counter = ttk.Label(frm_button, text=self.process_counter)
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

        self.frm_image = ttk.Frame(self)

        self.can_main = mc.MainCanvas(self.frm_image, command_container=self.command_container, bg='blue', can_main_width=self.can_main_width, can_main_height=self.can_main_height, can_main_region_width=self.can_main_region_width, can_main_region_height=self.can_main_region_height)

        self.can_main.grid(row=0, column=0, sticky="n, s, w, e")

        self.frm_config.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_image.grid(row=0, column=1, sticky="n, s, w, e")

        self.frm_image.rowconfigure(0, weight=1)
        self.frm_image.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

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
                    try:
                        label_text = text_json[available_command]["name"][self.backup_language]
                        command_description = text_json[available_command]["description"][self.backup_language]
                    except:
                        label_text = available_command
                frm_row = ttk.Frame(self.frm_available_commands)
                lbl_command = ttk.Label(frm_row, text=label_text, cursor= "hand2")
                lbl_info = wg.Info(frm_row, self, label_text, command_description)
                lbl_info.pack(side=tk.LEFT)
                lbl_command.pack(side=tk.LEFT)
                lbl_command.bind("<Double-Button-1>", lambda event: self.used_command_add(available_command))
                frm_row.pack(fill=tk.X, expand=True)

            add(available_command)

        self.preview_set()

        # előzőleg elmentett munka betöltése
        setting = self.setting_load()
        if bool(setting):
            for command_name, command_setting in setting.items():
                self.used_command_add(command_name, command_setting)

            for command_name in self.command_container.keys():
                self.can_main.io_widgets_connect(command_name)


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


    def setting_save(self):
        setting = {}
        # model setting
        for command_name, command_obj in self.command_container.items():
            model_input = command_obj.command_model.input
            model_output = command_obj.command_model.output
            model_properties = command_obj.command_model.properties
            model = {"input": model_input, "output": model_output, "properties": model_properties}
            setting.update({command_name: {"model": model}})

        # position of canvas elements
        for id in self.can_main.find_all():
            tag = self.can_main.gettags(id)
            if bool(tag):
                tag = tag[0]
                command_name = tag[:tag.rfind('.')]
                widget_func = tag[tag.rfind('.') + 1:]
                if widget_func == "move":
                    try:
                        setting[command_name].update({"coords": self.can_main.coords(id)})
                    except:
                        pass

        with open("setting.json", "w") as fp:
            json.dump(setting, fp, indent=4)


    def setting_load(self):
        try:
            with open("setting.json", "r") as fp:
                setting = json.load(fp)
        except:
            setting = {}

        return setting


    def once_run(self):
        self.sort_commands()
        self.continous_run_stop()
        self.next_image()


    def continous_run_start(self):
        self.sort_commands()
        self.run_contimous = True
        self.btn_run_continous.configure(state="disabled")
        self.next_image()


    def continous_run_stop(self):
        self.run_contimous = False
        self.btn_run_continous.configure(state="enabled")


    def used_command_add(self, command, setting=None):
        self.continous_run_stop()
        x = 100
        y = 100
        if bool(setting):   # ha dict-ből töltünk be meglévő adatokat, tipikusan mentés visszatöltésekor
            model_setting = setting["model"]
            x, y = setting["coords"]
            command_obj = com.Command(command, self.frm_used_command_setting, self.can_main, setting=model_setting)
        else:   # új létrehozása
            command_obj = com.Command(command, self.frm_used_command_setting, self.can_main)

        # hozzáadás a végrehajtási listához
        self.command_container.append(command_obj.command_name, command_obj)

        self.can_main.widget_create(command_obj.command_name, x, y)


    def sort_commands(self):
        self.can_main.canvas_disable()
        ok = True
        image_list = {}
        command_queue = []
        ##
        # Parancsok lefuttatása helyes sorrendben
        ##
        def find_parent_output(checked, command_name, input_name):
            # megkeressük, hogy az input_name melyik parancs outputja
            parent_command_object = self.command_container.get_object(input_name[0:input_name.rfind('.')])
            if bool(parent_command_object):
                if parent_command_object.command_name in checked[command_name]:
                    print("Az inputja ugyanaz, mint az outputja:", command_name)
                    return False
                else:
                    checked[command_name].append(parent_command_object.command_name)
                    for parent_command_input in parent_command_object.command_model.input.values():
                        ret = find_parent_output(checked, command_name, parent_command_input)
                        if not ret:
                            return False
            return True

        # 0. Hibák felderítése
        # 0.1 Megkeresünk minden olyan parancsot, amelyiknek nincs bemenete, de kéne, hogy legyen.
        for command_name_1, command_object_1 in self.command_container.items():
            if None in command_object_1.command_model.input.values():
                print("Error - command has empty input:", command_name_1, "-", command_object_1.command_model.input)
                ok = False
        # 0.2 Megkeresünk minden olyan parancsot, amelyiknek az inputja a saját outputja, akár más parancsokon keresztűl is.
        if ok:
            checked = {}
            for command_name_2, command_object_2 in self.command_container.items():
                for command_input_2 in command_object_2.command_model.input.values():
                    checked.clear()
                    checked.update({command_name_2: [command_name_2]})
                    ret = find_parent_output(checked, command_name_2, command_input_2)
                    if not ret:
                        ok = False
        if ok:
            #
            # 1. Input parancsok megkeresése, végrehejtása
            # Input parancsok megkeresése, végrehejtása.
            # Az outputjaikat használó parancsok kigyűjtése.
            command_queue_tmp = []
            for command_name_3, command_object_3 in self.command_container.items():
                if not bool(command_object_3.command_model.input):
                    for output_3 in command_object_3.command_model.output.values():
                        inputs_3 = self.command_container.find_input_keys(output_3)
                        for input_3 in inputs_3:
                            command_queue_tmp.append(input_3[:input_3.rfind('.')])
                            if not command_name_3 in command_queue:
                                command_queue.append(command_name_3)
                    command_object_3.update()
                    command_object_3.run(image_list)

            # 2. Ha ennek a parancsnak egyéb inputja is van, ami még nem futott le, akkor várakozási sorba marad.
            # Ha minden inputja megvan, végrehajtjuk.
            # 3. A 2. pont iterálása, amíg minden parancs le nem futott.
            while len(command_queue_tmp) > 0:
                for command_name_4 in command_queue_tmp:
                    command_object_4 = self.command_container.get_object(command_name_4)
                    command_object_4_inputs = command_object_4.command_model.input.values()
                    command_object_4_outputs = command_object_4.command_model.output.values()

                    for output_4 in command_object_4_outputs:
                        inputs_4 = None
                        inputs_4 = self.command_container.find_input_keys(output_4)
                        for input_4 in inputs_4:
                            cn_4 = input_4[:input_4.rfind('.')]
                            if not cn_4 in command_queue_tmp:
                                command_queue_tmp.append(cn_4)

                    if all(input_4_1 in image_list.keys() for input_4_1 in command_object_4_inputs): # ha a parancs összes inputja benne van a már létező parancskimenetek listájában
                        command_object_4.update()
                        ret = command_object_4.run(image_list)
                        if ret:
                            command_queue_tmp.remove(command_name_4)
                            if not command_name_4 in command_queue:
                                command_queue.append(command_name_4)

            self.command_queue = command_queue
        else:
            self.command_queue.clear()

        self.can_main.canvas_enable()
        return ok


    def next_image(self):
        self.process_counter += 1
        self.lbl_counter.configure(text=self.process_counter)

        self.image_list.clear()

        if bool(self.command_queue):
            for command in self.command_queue:
                try:
                    command_obj = self.command_container.get_object(command)
                except KeyError: # Futás közben törölve lett az objektum
                    self.continous_run_stop()
                    return False
                command_obj.update()
                command_obj.run(self.image_list)
        else:
            self.continous_run_stop()
            return False

        self.preview_set()

        if self.run_contimous:
            self.after(100, self.next_image)
