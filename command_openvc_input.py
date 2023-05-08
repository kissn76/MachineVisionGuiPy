import cv2
from pathlib import Path
from tkinter import ttk
import commandmodel as cm
import widgets as wg
from enums import *


class OpencvImread(cm.CommandModel):
    def __init__(self, command_name, setting = None):
        super().__init__(command_name)
        self.input = {}
        self.output = {"output": f"{self.command_name}.out"}
        self.setting = {
            "filename": "./resources/example/ocv_1.jpg",
            "flags": cv2.IMREAD_UNCHANGED
            }

        if bool(setting):
            self.set(setting)


    def setting_widget_get(self, master):
        self.setting_widget = ttk.Frame(master)
        input = {}
        output = {}
        setting = {
            "filename": wg.FwEntry(self.setting_widget, "Filename", self.setting["filename"], state=None),
            "flags": wg.FwCombobox(self.setting_widget, "Flags", ENUM_IMREAD_MODES, self.setting["flags"])
            }

        self.setting_widget_elements.update({"input": input})
        self.setting_widget_elements.update({"output": output})
        self.setting_widget_elements.update({"setting": setting})

        ttk.Label(self.setting_widget, text=self.command_name).pack()
        for widget in self.setting_widget_elements["setting"].values():
            if bool(widget):
                widget.pack()

        return self.setting_widget


    def run(self, images):
        self.copy_widget2model()

        filename = self.setting["filename"]
        flags = self.setting["flags"]
        output = self.output["output"]

        try:
            if Path(filename).is_file():
                image = cv2.imread(filename, flags)
                images.update({output: image})
        except:
            pass


class OpencvVideoCapture(cm.CommandModel):
    def __init__(self, command_name, setting = None):
        super().__init__(command_name)
        self.videocapture = None
        self.input = {}
        self.output = {"output": f"{self.command_name}.out"}
        self.setting = {
                "index": 0,
                "apiPreference": cv2.CAP_ANY
                }

        if bool(setting):
            self.set(setting)


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
        ttk.Button(self.setting_widget, text="Connect", command=self.camera_connect).pack()
        ttk.Button(self.setting_widget, text="Disconnect", command=self.camera_disconnect).pack()

        return self.setting_widget


    def camera_connect(self):
        self.copy_widget2model()

        index = self.setting["index"]
        apiPreference = self.setting["apiPreference"]

        if not bool(self.videocapture):
            input = None
            if not index is None:
                input = int(index)

            if not input is None:
                print("VideoCapture setting:", input)
                self.videocapture = cv2.VideoCapture(input, apiPreference)
                if self.videocapture.isOpened():
                    print("VideoCapture", input, "is opened")
                else:
                    print("Error - VideoCapture - Can't open")
                    self.camera_disconnect()
            else:
                print("Error - VideoCapture - Unknown input device")
        else:
            print("VideoCapture has already opened")


    def camera_disconnect(self):
        try:
            self.videocapture.release()
            self.videocapture = None
            print("VideoCapture released")
        except:
            pass


    def run(self, images):
        self.copy_widget2model()

        index = self.setting["index"]
        output = self.output["output"]

        if bool(self.videocapture) and self.videocapture.isOpened():
            try:
                ret, frame = self.videocapture.read()
                if not ret:
                    print("Error - VideoCapture - Can't receive frame")
                images.update({output: frame})
            except:
                pass
        else:
            print("VideoCapture", index, "is not opened")
