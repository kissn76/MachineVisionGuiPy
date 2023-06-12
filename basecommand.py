import settingwidget as sw
from tkinter import ttk


class BaseCommand():
    def __init__(self, command_model, setting_master, display_master):
        self.setting_master = setting_master
        self.display_master = display_master

        self.command_model = command_model
        self.command_model_input = {}
        self.command_model_output = {}
        self.command_model_properties = {}

        self.setting_widget = sw.SettingWidget(self.setting_master, self.command_model.command_name)
        self.setting_widget_input = {}
        self.setting_widget_output = {}
        self.setting_widget_properties = {}

        self.display_widget = ttk.Frame(self.display_master)
        self.display_widget_input = {}
        self.display_widget_output = {}
        self.display_widget_properties = {}


    def set_model(self):
        if not bool(self.command_model.input):
            self.command_model.set_input(self.command_model_input)

        if not bool(self.command_model.output):
            self.command_model.set_output(self.command_model_output)

        if not bool(self.command_model.properties):
            self.command_model.set_properties(self.command_model_properties)


    def set_setting_widget(self):
        self.setting_widget.set(self.setting_widget_input, self.setting_widget_output, self.setting_widget_properties)


    def set_display_widget(self):
        for widget in self.display_widget_properties.values():
            if bool(widget):
                widget.pack()



    def setting_widget_get(self):
        return self.setting_widget


    def display_widget_get(self):
        return self.display_widget
