from tkinter import ttk


class SettingWidget(ttk.Frame):
    def __init__(self, master, command_name):
        super().__init__(master)
        self.command_name = command_name
        self.widget_elements = {}


    def set(self, input, output, properties):
        self.widget_elements.update({"input": input})
        self.widget_elements.update({"output": output})
        self.widget_elements.update({"properties": properties})

        ttk.Label(self, text=self.command_name).pack()
        for widget in self.widget_elements["properties"].values():
            if bool(widget):
                widget.pack()
