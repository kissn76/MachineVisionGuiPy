from tkinter import ttk
import widgets as wg
from enums import *
import mainwindow as mw


input_elements = {}
output_elements = {}
clipboard_io = None


class CommandModel():
    def __init__(self, command_name):
        self.command_name = command_name
        self.setting_widget = None
        self.setting_widget_elements = {}
        self.display_widget = None
        self.display_widget_elements = {}
        self.input = {}
        self.output = {}
        self.setting = {}


    def display_widget_get(self, master):
        self.display_widget = ttk.Frame(master)

        frm_display_input = ttk.Frame(self.display_widget)
        lbl_command_name = ttk.Label(self.display_widget, text=self.command_name)
        frm_display_command = ttk.Frame(self.display_widget)
        frm_display_output = ttk.Frame(self.display_widget)

        frm_display_input.pack()
        lbl_command_name.pack()
        frm_display_command.pack()
        frm_display_output.pack()

        lbl_command_name.bind("<Button-1>", lambda event: self.show_setting_widget(self.command_name))

        for widget in self.display_widget_elements.values():
            widget.pack()

        # bemenetek kirajzolása
        try:
            for input_key, input_value_name in self.input.items():
                input_value = None
                if input_value_name is None:
                    input_value = "None"
                else:
                    input_value = input_value_name
                lbl_in = ttk.Label(frm_display_input, text=f"{input_key}: {input_value}")
                lbl_in.pack()
                lbl_in.bind("<Double-Button-1>", lambda event: self.paste_input(input_key))
                input_elements.update({f"{self.command_name}.{input_key}": lbl_in})
        except:
            pass

        # kimenetek kirajzolása
        try:
            for output_key, output_value_name in self.output.items():
                output_value = None
                if output_value_name is None:
                    output_value = "None"
                else:
                    output_value = output_value_name
                lbl_out = ttk.Label(frm_display_output, text=f"{output_key}: {output_value}")
                lbl_out.pack()
                lbl_out.bind("<Double-Button-1>", lambda event: self.copy_output(output_value))
                lbl_out.bind("<Button-1>", lambda event: self.preview_set(output_value))
                output_elements.update({f"{self.command_name}.{output_value}": lbl_out})
        except:
            pass

        return self.display_widget


    def show_setting_widget(self, command_name):
        mw.setting_widgets_hide()
        mw.setting_widget_show(command_name)


    def preview_set(self, output_name):
        mw.preview_command = output_name


    def copy_output(self, output_name):
        global clipboard_io
        clipboard_io = output_name

        for lbl_name, lbl_out in output_elements.items():
            if lbl_name == f"{self.command_name}.{output_name}":
                lbl_out.configure(background="red")
            else:
                lbl_out.configure(background="#d9d9d9")


    def paste_input(self, input_key):
        if not bool(clipboard_io):
            print("Empty clipboard")
        else:
            self.input[input_key] = clipboard_io
            input_elements[f"{self.command_name}.{input_key}"].config(text=f"{input_key}: {clipboard_io}")

        # TODO
        # kiszűrni a saját kimenetet, ne legyen a saját kimenet, a saját bemenet


    # def setting_widget_get(self, master):
    #     self.setting_widget = ttk.Frame(master)
    #     ttk.Label(self.setting_widget, text=self.command_name).pack()
    #     for widget in self.setting_widget_elements["setting"].values():
    #         if bool(widget):
    #             widget.pack()


    def get(self):
        for key in self.input.keys():
            try:
                self.input[key] = self.setting_widget_elements[key].get()
            except:
                pass


    def set(self, setting):
        for key in self.input.keys():
            self.input[key] = setting["input"][key]

        for key in self.output.keys():
            self.output[key] = setting["output"][key]

        for key in self.setting.keys():
            self.setting[key] = setting["setting"][key]



class OpencvVideoCapture(CommandModel):
    def __init__(self, command_name):
        super().__init__(command_name)
        self.input = {"videocapture": None}
        self.output = {"output": f"{self.command_name}.out"}
        self.setting = {
                "index": 0,
                "apiPreference": cv2.CAP_ANY
                }


    def setting_widget_get(self, master):
        self.setting_widget = ttk.Frame(master)
        input = {}
        output = {}
        setting = {
            "index": wg.FwEntry(self.setting_widget, "Index", self.setting["index"], state=None)
            }

        self.setting_widget_elements.update({"input": input})
        self.setting_widget_elements.update({"output": output})
        self.setting_widget_elements.update({"setting": setting})

        ttk.Label(self.setting_widget, text=self.command_name).pack()
        for widget in self.setting_widget_elements["setting"].values():
            if bool(widget):
                widget.pack()

        # super().setting_widget_get(master)

        return self.setting_widget

    def run(self, images):
        self.get()

        videocapture = self.input["videocapture"]
        index = self.setting["index"]
        apiPreference = self.setting["apiPreference"]
        output = self.output["output"]

        if not bool(videocapture):
            input = None
            if not index is None:
                input = int(index)

            if not input is None:
                print("VideoCapture setting:", input)
                self.input["videocapture"] = cv2.VideoCapture(input, apiPreference)
                videocapture = self.input["videocapture"]
                if videocapture.isOpened():
                    print("VideoCapture", input, "is opened")
                else:
                    print("Error - VideoCapture - Can't open")
                    self.input["videocapture"].release()
                    self.input["videocapture"] = None
                    videocapture = None
            else:
                print("Error - VideoCapture - Unknown input device")

        if bool(videocapture) and videocapture.isOpened():
            try:
                ret, frame = videocapture.read()
                if not ret:
                    print("Error - VideoCapture - Can't receive frame")
                images.update({output: frame})
            except:
                pass