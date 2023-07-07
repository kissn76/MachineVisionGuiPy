import json
from tkinter import ttk
import commandcontainer as cc
import command as com
import maincanvas as mc


class Project():
    def __init__(self, master, filepath=None):
        self.can_main_width = 1000
        self.can_main_height = 800
        self.can_main_region_width = 4000
        self.can_main_region_height = 4000
        self.command_container = cc.CommandContainer()
        self.command_queue = []
        self.image_list = {}
        self.filepath = filepath
        self.can_main = mc.MainCanvas(master, command_container=self.command_container, bg='blue', can_main_width=self.can_main_width, can_main_height=self.can_main_height, can_main_region_width=self.can_main_region_width, can_main_region_height=self.can_main_region_height)
        self.frm_used_command_setting = ttk.LabelFrame(master, text="Command setting")

        if bool(self.filepath):
            self.project_load(self.filepath)


    def project_load(self, project_name):
        project = {}
        try:
            with open(project_name, "r") as fp:
                project = json.load(fp)
        except:
            pass

        if bool(project):
            # reset project, delete canvas elements
            self.can_main.delete("all")
            self.command_container.clear()
            # for widget in self.frm_used_command_setting.winfo_children():
            #     widget.pack_forget()
            # cm.command_counter = 0

            for command_name, command_setting in project.items():
                self.used_command_add(command_name, command_setting)

            for command_name in self.command_container.keys():
                self.can_main.io_widgets_connect(command_name)


    def project_save(self):
        project = {}
        # model setting
        for command_name, command_obj in self.command_container.items():
            model_input = command_obj.command_model.input
            model_output = command_obj.command_model.output
            model_properties = command_obj.command_model.properties
            model = {"input": model_input, "output": model_output, "properties": model_properties}
            project.update({command_name: {"model": model}})

        # position of canvas elements
        for id in self.can_main.find_all():
            tag = self.can_main.gettags(id)
            if bool(tag):
                tag = tag[0]
                command_name = tag[:tag.rfind('.')]
                widget_func = tag[tag.rfind('.') + 1:]
                if widget_func == "move":
                    try:
                        project[command_name].update({"coords": self.can_main.coords(id)})
                    except:
                        pass

        with open(self.filepath, "w") as fp:
            json.dump(project, fp, indent=4)


    def used_command_add(self, command, setting=None):
        # self.continous_run_stop()
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



    # def once_run(self):
    #     self.sort_commands()
    #     self.continous_run_stop()
    #     self.next_image()


    # def continous_run_start(self):
    #     self.sort_commands()
    #     self.run_contimous = True
    #     self.btn_run_continous.configure(state="disabled")
    #     self.next_image()


    # def continous_run_stop(self):
    #     self.run_contimous = False
    #     self.btn_run_continous.configure(state="enabled")


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
        # self.process_counter += 1
        # self.lbl_counter.configure(text=self.process_counter)

        self.image_list.clear()

        if bool(self.command_queue):
            for command in self.command_queue:
                try:
                    command_obj = self.command_container.get_object(command)
                except KeyError: # Futás közben törölve lett az objektum
                    # self.continous_run_stop()
                    return False
                command_obj.update()
                command_obj.run(self.image_list)
        else:
            # self.continous_run_stop()
            return False

        # self.preview_set()

        # if self.run_contimous:
        #     self.after(100, self.next_image)
