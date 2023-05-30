import cv2
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import command as com
import widgets as wg


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
        self.icon_size = 16
        self.image_move = ImageTk.PhotoImage(Image.open(f"./resources/icons/move_{self.icon_size}.png"))
        self.image_close = ImageTk.PhotoImage(Image.open(f"./resources/icons/close_{self.icon_size}.png"))
        self.image_info = ImageTk.PhotoImage(Image.open(f"./resources/icons/info_{self.icon_size}.png"))
        self.image_settings = ImageTk.PhotoImage(Image.open(f"./resources/icons/settings_{self.icon_size}.png"))
        self.image_delete = ImageTk.PhotoImage(Image.open(f"./resources/icons/delete_{self.icon_size}.png"))

        self.system_language = "hu"
        self.backup_language = "en"

        self.lines = {}

        self.can_main_width = 800
        self.can_main_height = 800
        self.can_main_region_width = 4000
        self.can_main_region_height = 4000

        self.available_commands = ["opencv_videocapture", "opencv_imread", "opencv_threshold", "opencv_gaussianblur", "opencv_resize", "opencv_canny", "tk_display"]
        self.image_list = {}
        self.run_contimous = False

        self.frm_config = ttk.Frame(self)
        self.frm_popup_id = None

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

        self.can_main = tk.Canvas(self.frm_image, bg='blue', scrollregion=(0, 0, self.can_main_region_width, self.can_main_region_height))
        hbar=ttk.Scrollbar(self.frm_image, orient=tk.HORIZONTAL)
        hbar.grid(row=1, column=0, sticky="e, w")
        hbar.config(command=self.can_main.xview)
        vbar=ttk.Scrollbar(self.frm_image, orient=tk.VERTICAL)
        vbar.grid(row=0, column=1, sticky="n, s")
        vbar.config(command=self.can_main.yview)
        self.can_main.config(width=self.can_main_width, height=self.can_main_height)
        self.can_main.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.can_main.grid(row=0, column=0, sticky="n, s, w, e")

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

            for command_name in used_command_list.keys():
                self.connect_commands(command_name)


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
            model_properties = command_obj.command_model.properties
            model = {"input": model_input, "output": model_output, "properties": model_properties}
            setting.update({command_name: {"model": model}})

        # position of canvas elements
        for id in self.can_main.find_all():
            try:
                setting[self.can_main.gettags(id)[0]].update({"coords": self.can_main.coords(id)})
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


    def continous_run_start(self):
        self.run_contimous = True
        self.btn_run_continous.configure(state="disabled")
        self.next_image()


    def continous_run_stop(self):
        self.run_contimous = False
        self.btn_run_continous.configure(state="enabled")


    # DRAG & DROP metódusok
    def dnd_select_object(self, event):
        self.can_main.bind('<Motion>', self.dnd_move_object)
        self.can_main.bind('<ButtonRelease-1>', self.dnd_deselect_object)

        x, y = event.x, event.y
        x = self.can_main.canvasx(x)
        y = self.can_main.canvasy(y)
        self.can_main.addtag_withtag('selected', tk.CURRENT)

        tags = self.can_main.gettags('selected')
        if len(tags) > 0:
            tag = tags[0]
            command_name = tag[0:tag.rfind('.')]
            item_type_tag = tag[tag.rfind('.') + 1:]
            if item_type_tag == "settings":
                setting_widgets_hide()
                setting_widget_show(command_name)
            elif item_type_tag == "delete":
                self.used_command_delete(command_name)


    def dnd_move_object(self, event):
        tags = self.can_main.gettags('selected')
        if len(tags) > 0:
            tag = tags[0]
            command_name_tag = tag[0:tag.rfind('.')]
            item_type_tag = tag[tag.rfind('.') + 1:]
            if item_type_tag == "move":
                mouse_x, mouse_y = event.x, event.y
                self.display_move(command_name_tag, mouse_x, mouse_y)


    def dnd_deselect_object(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')
    # DRAG & DROP metódusok END


    # connect commands with line
    def connect_commands(self, command_name):
        if not command_name in used_command_list.keys():
            return

        command_x0, command_y0, command_x1, command_y1 = self.can_main.bbox(command_name)

        for output_name in used_command_list[command_name].command_model.output.values():
            children = self.find_child_commands(output_name)
            for child in children:
                line_name = f"{output_name}-{child}"
                child_x0, child_y0, child_x1, child_y1 = self.can_main.bbox(child)
                if line_name in self.lines.keys():
                    self.can_main.coords(self.lines[line_name], command_x0, command_y1, child_x0, child_y0)
                else:
                    line = self.can_main.create_line(command_x0, command_y1, child_x0, child_y0, fill="green", width=2)
                    self.lines.update({line_name: line})

        for input_name in used_command_list[command_name].command_model.input.values():
            if bool(input_name):
                input_command = input_name[:input_name.rfind('.')]
                line_name = f"{input_name}-{command_name}"
                parent_x0, parent_y0, parent_x1, parent_y1 = self.can_main.bbox(input_command)
                if line_name in self.lines.keys():
                    self.can_main.coords(self.lines[line_name], command_x0, command_y0, parent_x0, parent_y1)
                else:
                    line = self.can_main.create_line(command_x0, command_y0, parent_x0, parent_y1, fill="green", width=2)
                    self.lines.update({line_name: line})


    def available_command_row_add(self, command):
        text_json = None
        label_text = None
        command_description = None
        with open("lang/commands_en.json", "r") as fp:
            text_json = json.load(fp)
        try:
            label_text = text_json[command]["name"][self.system_language]
            command_description = text_json[command]["description"][self.system_language]
        except:
            try:
                label_text = text_json[command]["name"][self.backup_language]
                command_description = text_json[command]["description"][self.backup_language]
            except:
                label_text = command
        frm_row = ttk.Frame(self.frm_available_commands)
        lbl_command = ttk.Label(frm_row, text=label_text, cursor= "hand2")
        lbl_info = wg.Info(frm_row, self, label_text, command_description)
        lbl_info.pack(side=tk.LEFT)
        lbl_command.pack(side=tk.LEFT)
        lbl_command.bind("<Double-Button-1>", lambda event: self.used_command_add(command))
        frm_row.pack(fill=tk.X, expand=True)


    def used_command_add(self, command, setting=None):
        x = 100
        y = 100
        if bool(setting):   # ha dict-ből töltünk be meglévő adatokat, tipikusan mentés visszatöltésekor
            model_setting = setting["model"]
            x, y = setting["coords"]
            command_obj = com.Command(command, self.frm_used_command_setting, self.can_main, setting=model_setting)
        else:   # új létrehozása
            command_obj = com.Command(command, self.frm_used_command_setting, self.can_main)

        # hozzáadás a végrehajtási listához
        used_command_list.update({command_obj.command_name: command_obj})

        self.display_create(command_obj.command_name, x, y)


    def used_command_delete(self, command_name):
        print(f"delete: {command_name}")


    def display_create(self, command_name, x=100, y=100):
        command_obj = used_command_list[command_name]
        id_move = self.can_main.create_image(x, y, image=self.image_move, anchor="nw")
        self.can_main.addtag_withtag(f"{command_obj.command_name}.move", id_move)

        id_setting = self.can_main.create_image(x, y, image=self.image_settings, anchor="nw")
        self.can_main.addtag_withtag(f"{command_obj.command_name}.settings", id_setting)

        id_delete = self.can_main.create_image(x, y, image=self.image_delete, anchor="nw")
        self.can_main.addtag_withtag(f"{command_obj.command_name}.delete", id_delete)

        frm_command = command_obj.frm_display_main
        id_frm = self.can_main.create_window(x, y, window=frm_command, anchor="nw")
        self.can_main.addtag_withtag(command_obj.command_name, id_frm)    # a canvas elem tag-ként megkapja a command_name-et, hogy egyedileg meghívható legyen később

        frm_command.update()

        id_background = self.can_main.create_rectangle(x, y, x, y, fill='red', outline='red')
        self.can_main.addtag_withtag(f"{command_obj.command_name}.background", id_background)
        self.can_main.tag_lower(id_background, id_move)

        self.display_move(command_name, x, y)


    def display_move(self, command_name, x, y):
        canvas_x = self.can_main.canvasx(x)
        canvas_y = self.can_main.canvasy(y)
        if x > self.can_main_width:
            self.can_main.xview_scroll(1, 'units')
        if x < 1:
            self.can_main.xview_scroll(-1, 'units')
        if y > self.can_main_height:
            self.can_main.yview_scroll(1, 'units')
        if y < 1:
            self.can_main.yview_scroll(-1, 'units')
        if canvas_x < int(self.icon_size / 2):
            canvas_x = int(self.icon_size / 2)
        if canvas_x > self.can_main_region_width:
            canvas_x = self.can_main_region_width - int(self.icon_size / 2)
        if canvas_y < int(self.icon_size / 2):
            canvas_y = int(self.icon_size / 2)
        if canvas_y > self.can_main_region_height:
            canvas_y = self.can_main_region_height - int(self.icon_size / 2)
        self.can_main.coords(f"{command_name}.move", canvas_x - int(self.icon_size / 2), canvas_y - int(self.icon_size / 2))

        box = self.can_main.bbox(f"{command_name}.move")
        if bool(box):
            move_x0, move_y0, move_x1, move_y1 = box
            self.can_main.coords(command_name, move_x1, move_y0)
            frm_command = used_command_list[command_name].frm_display_main
            frm_width = frm_command.winfo_reqwidth()
            frm_height = frm_command.winfo_reqheight()
            self.can_main.coords(f"{command_name}.settings", move_x0, move_y1)
            self.can_main.coords(f"{command_name}.delete", move_x0, move_y1 + self.icon_size)
            self.can_main.coords(f"{command_name}.background", move_x0, move_y0, move_x1, move_y1 + self.icon_size * 2)

            self.connect_commands(command_name)


    # megkeres minden parancsot, amelyik inputként használja az outputot
    def find_child_commands(self, output_name):
        child_commands = []
        for command_object in used_command_list.values():
            if output_name in command_object.command_model.input.values():
                child_commands.append(command_object.command_name)

        return child_commands


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
                if parent_command_object.command_name in checked[command_name]:
                    print("Az inputja ugyanaz, mint az outputja:", command_name)
                    return False
                else:
                    checked[command_name].append(parent_command_object.command_name)
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
        # Input parancsok megkeresése, végrehejtása.
        # Az outputjaikat használó parancsok kigyűjtése.
        command_queue = []
        for command_name, command_object in used_command_list.items():
            if not bool(command_object.command_model.input):
                for output in command_object.command_model.output.values():
                    command_queue.extend(self.find_child_commands(output))
                command_object.update()
                command_object.run(self.image_list)
        # 2. Ha ennek a parancsnak egyéb inputja is van, ami még nem futott le, akkor várakozási sorba marad.
        # Ha minden inputja megvan, végrehajtjuk.
        # 3. A 2. pont iterálása, amíg minden parancs le nem futott.
        while len(command_queue) > 0:
            for command_name in command_queue:
                command_object = used_command_list[command_name]
                command_object_inputs = command_object.command_model.input.values()
                command_object_outputs = command_object.command_model.output.values()

                for output in command_object_outputs:
                    command_queue.extend(self.find_child_commands(output))

                if all(input in self.image_list.keys() for input in command_object_inputs): # ha a parancs összes inputja benne van a már létező parancskimenetek listájában
                    command_object.update()
                    ret = command_object.run(self.image_list)
                    if ret:
                        command_queue.remove(command_name)

        self.preview_set()

        if self.run_contimous:
            self.after(100, self.next_image)
