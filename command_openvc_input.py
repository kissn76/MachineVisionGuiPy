import cv2
from pathlib import Path
from tkinter import ttk
import basecommand as bc
import widgets as wg
from enums import *


class OpencvImread(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        info_label = "Filename"
        info_description = "Name of file to be loaded."
        self.command_model_input = {}
        self.command_model_output = {"output": f"{self.command_model.command_name}.out"}
        self.command_model_properties = {
            "filename": "./resources/example/ocv_1.jpg",
            "flags": cv2.IMREAD_UNCHANGED
            }

        self.set_model()

        self.setting_widget_input = {}
        self.setting_widget_output = {}
        self.setting_widget_properties = {
            "filename": wg.FwEntry(self.setting_widget, "Filename", self.command_model.properties["filename"], state=None, info_label=info_label, info_description=info_description),
            "flags": wg.FwCombobox(self.setting_widget, "Flags", ENUM_IMREAD_MODES, self.command_model.properties["flags"])
            }

        self.set_setting_widget()


    def run(self, images):
        filename = self.command_model.properties["filename"]
        flags = self.command_model.properties["flags"]
        output = self.command_model.output["output"]

        try:
            if Path(filename).is_file():
                image = cv2.imread(filename, flags)
                images.update({output: image})
                return True
        except:
            pass

        return False


class OpencvVideoCapture(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        self.videocapture = None
        self.command_model_input = {}
        self.command_model_output = {"output": f"{self.command_model.command_name}.out"}
        self.command_model_properties = {
                "index": 0,
                "apiPreference": cv2.CAP_ANY
                }

        self.set_model()

        self.setting_widget_input = {}
        self.setting_widget_output = {}
        self.setting_widget_properties = {
            "index": wg.FwEntry(self.setting_widget, "Index", self.command_model.properties["index"], state=None)
            }

        self.set_setting_widget()

        ttk.Button(self.setting_widget, text="Connect", command=self.camera_connect).pack()
        ttk.Button(self.setting_widget, text="Disconnect", command=self.camera_disconnect).pack()


    def camera_connect(self):
        index = self.command_model.properties["index"]
        apiPreference = self.command_model.properties["apiPreference"]

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
        index = self.command_model.properties["index"]
        output = self.command_model.output["output"]

        if bool(self.videocapture) and self.videocapture.isOpened():
            try:
                ret, frame = self.videocapture.read()
                if not ret:
                    print("Error - VideoCapture - Can't receive frame")
                images.update({output: frame})
                return True
            except:
                pass
        else:
            print("VideoCapture", index, "is not opened")

        return False
