import cv2
from pathlib import Path
from tkinter import ttk
import commandmodel as cm
import widgets as wg
from enums import *


class OpencvThreshold(cm.CommandModel):
    def __init__(self, command_name, setting_master, display_master, setting=None):
        super().__init__(command_name, setting_master, display_master)
        self.input = {"src": None}
        self.output = {"dst": f"{self.command_name}.dst"}
        self.setting = {
                "thresh": 150,
                "maxval": 255,
                "type": cv2.THRESH_BINARY
                }

        if bool(setting):
            self.set(setting)


    def setting_widget_get(self):
        input = {}
        output = {}
        setting = {
            "thresh": wg.FwScale(self.setting_widget, "Threshold", 0, 255, self.setting["thresh"]),
            "maxval": wg.FwScale(self.setting_widget, "Maximum value", 0, 255, self.setting["maxval"]),
            "type": wg.FwCombobox(self.setting_widget, "Type", ENUM_THRESHOLD_TYPES, self.setting["type"])
            }

        self.setting_widget_set(input, output, setting)

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


class OpencvGaussianblur(cm.CommandModel):
    def __init__(self, command_name, setting_master, display_master, setting=None):
        super().__init__(command_name, setting_master, display_master)
        self.input = {"src": None}
        self.output = {"dst": f"{self.command_name}.dst"}
        self.setting = {
                "ksize_w": 3,
                "ksize_h": 3,
                "sigmaX": 0.0,
                "sigmaY": 0.0,
                "borderType": cv2.BORDER_DEFAULT
                }

        if bool(setting):
            self.set(setting)


    def setting_widget_get(self):
        input = {}
        output = {}
        setting = {
            "ksize_w": wg.FwScale(self.setting_widget, "Kernel size width", 1, 255, self.setting["ksize_w"], resolution=2, value_type=int),
            "ksize_h": wg.FwScale(self.setting_widget, "Kernel size height", 1, 255, self.setting["ksize_h"], resolution=2, value_type=int),
            "sigmaX": wg.FwScale(self.setting_widget, "Sigma x", 0, 1, self.setting["sigmaX"], resolution=0.1),
            "sigmaY": wg.FwScale(self.setting_widget, "Sigma y", 0, 1, self.setting["sigmaY"], resolution=0.1),
            "borderType": wg.FwCombobox(self.setting_widget, "Interpolation", ENUM_BORDERTYPES, self.setting["borderType"])
            }

        self.setting_widget_set(input, output, setting)

        return self.setting_widget


    def run(self, images):
        self.copy_widget2model()

        src = self.input["src"]
        ksize_w = self.setting["ksize_w"]
        ksize_h = self.setting["ksize_h"]
        sigmaX = self.setting["sigmaX"]
        sigmaY = self.setting["sigmaY"]
        borderType = self.setting["borderType"]
        dst = self.output["dst"]

        try:
            if bool(src) and len(images[src]) > 0:
                image = cv2.GaussianBlur(images[src], ksize=(ksize_w, ksize_h), sigmaX=sigmaX, sigmaY=sigmaY, borderType=borderType)
                images.update({dst: image})
        except:
            pass
