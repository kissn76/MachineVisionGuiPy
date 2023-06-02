from tkinter import ttk
import mainwindow as mw
import vars


input_elements = {}
output_elements = {}
# clipboard_io = None


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

        # bemenetek kirajzolása
        # try:
        #     for input_key, input_value_name in self.command_model.input.items():
        #         input_value = None
        #         if input_value_name is None:
        #             input_value = "None"
        #         else:
        #             input_value = input_value_name
        #         lbl_in = ttk.Label(frm_display_input, text=f"{input_key}: {input_value}")
        #         lbl_in.pack()
        #         # lbl_in.bind("<Double-Button-1>", lambda event: self.paste_input(input_key))
        #         input_elements.update({f"{self.command_name}.{input_key}": lbl_in})
        # except:
        #     pass

        # kimenetek kirajzolása
        # try:
        #     for output_key, output_value_name in self.command_model.output.items():
        #         output_value = None
        #         if output_value_name is None:
        #             output_value = "None"
        #         else:
        #             output_value = output_value_name
        #         lbl_out = ttk.Label(frm_display_output, text=f"{output_key}: {output_value}")
        #         lbl_out.pack()
        #         lbl_out.bind("<Double-Button-1>", lambda event: self.copy_output(output_value))
        #         lbl_out.bind("<Button-1>", lambda event: self.preview_set(output_value))
        #         output_elements.update({f"{self.command_name}.{output_value}": lbl_out})
        # except:
        #     pass


    # def preview_set(self, output_name):
    #     mw.preview_command = output_name

    #     for lbl_name, lbl_out in output_elements.items():
    #         if lbl_name == f"{self.command_name}.{output_name}":
    #             lbl_out.configure(borderwidth=1, relief="solid")
    #         else:
    #             lbl_out.configure(borderwidth=0)


    # def copy_output(self, output_name):
    #     global clipboard_io
    #     clipboard_io = output_name

    #     for lbl_name, lbl_out in output_elements.items():
    #         if lbl_name == f"{self.command_name}.{output_name}":
    #             lbl_out.configure(background="red")
    #         else:
    #             lbl_out.configure(background="#d9d9d9")


    def paste_input(self, input_key):
        if not bool(mw.clipboard_io):
            print("Empty clipboard")
        else:
            if not mw.clipboard_io in self.command_model.output.values():
                # vonal törlése a gui-n, ha már volt beállított input
                if bool(self.command_model.input[input_key]):
                    line_name = f"{self.command_model.input[input_key]}-{self.command_name}"
                    vars.mainwindow.can_main.delete(vars.mainwindow.lines[line_name])
                    vars.mainwindow.lines.pop(line_name)

                self.command_model.input[input_key] = mw.clipboard_io
                print(self.command_model.input)
                # input_elements[f"{self.command_name}.{input_key}"].config(text=f"{input_key}: {mw.clipboard_io}")
                vars.mainwindow.connect_commands(self.command_name)
            else:
                print("Error: nem lehet a saját maga inputja!")
