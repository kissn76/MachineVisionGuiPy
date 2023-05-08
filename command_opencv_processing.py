import cv2
from pathlib import Path
from tkinter import ttk
import commandmodel as cm
import widgets as wg
from enums import *


class OpencvThreshold(cm.CommandModel):
    def __init__(self, command_name, setting = None):
        super().__init__(command_name)
        self.input = {"src": None}
        self.output = {"dst": f"{self.command_name}.dst"}
        self.setting = {
                "thresh": 150,
                "maxval": 255,
                "type": cv2.THRESH_BINARY
                }

        if bool(setting):
            self.set(setting)


    def setting_widget_get(self, master):
        self.setting_widget = ttk.Frame(master)
        input = {}
        output = {}
        setting = {
            "thresh": wg.FwScale(self.setting_widget, "Threshold", 0, 255, self.setting["thresh"]),
            "maxval": wg.FwScale(self.setting_widget, "Maximum value", 0, 255, self.setting["maxval"]),
            "type": wg.FwCombobox(self.setting_widget, "Type", ENUM_THRESHOLD_TYPES, self.setting["type"])
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

        src = self.input["src"]
        thresh = self.setting["thresh"]
        maxval = self.setting["maxval"]
        type = self.setting["type"]
        dst = self.output["dst"]

        try:
            if bool(src) and len(images[src]) > 0:
                _, image = cv2.threshold(images[src], thresh=thresh, maxval=maxval, type=type)
                images.update({dst: image})
        except:
            pass