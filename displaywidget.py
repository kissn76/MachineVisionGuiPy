from tkinter import ttk


class DisplayWidget(ttk.Frame):
    def __init__(self, master, command_model):
        super().__init__(master)
        self.command_model = command_model
        self.command_name = self.command_model.command_name
        self.widget_elements = {}


    def set(self, input, output, properties):
        self.widget_elements.update({"input": input})
        self.widget_elements.update({"output": output})
        self.widget_elements.update({"properties": properties})

        frm_display_input = ttk.Frame(self)
        lbl_command_name = ttk.Label(self, text=self.command_name)
        frm_display_command = ttk.Frame(self)
        frm_display_output = ttk.Frame(self)

        frm_display_input.pack()
        lbl_command_name.pack()
        frm_display_command.pack()
        frm_display_output.pack()

        for widget in self.widget_elements["properties"].values():
            widget.pack()
