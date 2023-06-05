class CommandContainer(dict):
    def __init__(self):
        pass


    def append(self, command_name, command_object):
        self.update({command_name: command_object})


    def get_object(self, command_name):
        return self[command_name]


    # megkeresi minden parancs input kulcsát, amelyik értékként tartalmazza az outputot
    # tömbként adja vissza a canvas tag neveket
    def find_input_keys(self, output_name):
        input_commands = []
        for command_object in self.values():
            keys = [k for k, v in command_object.command_model.input.items() if v == output_name]
            if bool(keys):
                for key in keys:
                    input_commands.append(f"{command_object.command_name}.{key}")

        return input_commands


    def setting_widgets_hide(self):
        for command_obj in self.values():
            command_obj.frm_setting_main.pack_forget()


    def setting_widget_show(self, command_name):
        self.setting_widgets_hide()
        self.get_object(command_name).frm_setting_main.pack()