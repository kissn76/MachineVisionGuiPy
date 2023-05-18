import cv2
from pathlib import Path
from tkinter import ttk
import commandmodel as cm
import settingwidget as sw
import displaywidget as dw
import widgets as wg
from enums import *


class OpencvThreshold():
    def __init__(self, command_model, setting_master, display_master):
        self.command_model = command_model
        # DEFAULT VALUES
        command_model_input = {"src": None}
        command_model_output = {"dst": f"{self.command_model.command_name}.dst"}
        command_model_properties = {
            "thresh": 150,
            "maxval": 255,
            "type": cv2.THRESH_BINARY
            }

        if not bool(self.command_model.input):
            self.command_model.set_input(command_model_input)

        if not bool(self.command_model.output):
            self.command_model.set_output(command_model_output)

        if not bool(self.command_model.properties):
            self.command_model.set_properties(command_model_properties)

        self.setting_widget = sw.SettingWidget(setting_master, self.command_model.command_name)
        setting_widget_input = {}
        setting_widget_output = {}
        setting_widget_properties = {
            "thresh": wg.FwScale(self.setting_widget, "Threshold", 0, 255, self.command_model.properties["thresh"]),
            "maxval": wg.FwScale(self.setting_widget, "Maximum value", 0, 255, self.command_model.properties["maxval"]),
            "type": wg.FwCombobox(self.setting_widget, "Type", ENUM_THRESHOLD_TYPES, self.command_model.properties["type"])
            }

        self.setting_widget.set(setting_widget_input, setting_widget_output, setting_widget_properties)

        self.display_widget = dw.DisplayWidget(display_master, self.command_model)
        display_widget_input = {}
        display_widget_output = {}
        display_widget_properties = {}

        self.display_widget.set(display_widget_input, display_widget_output, display_widget_properties)


    def setting_widget_get(self):
        return self.setting_widget


    def display_widget_get(self):
        return self.display_widget


    def run(self, images):
        # átvinni a controllerbe!!!
        # self.copy_widget2model()

        src = self.command_model.input["src"]
        thresh = self.command_model.properties["thresh"]
        maxval = self.command_model.properties["maxval"]
        type = self.command_model.properties["type"]
        dst = self.command_model.output["dst"]

        try:
            if bool(src) and len(images[src]) > 0:
                _, image = cv2.threshold(images[src], thresh=thresh, maxval=maxval, type=type)
                images.update({dst: image})
                return True
        except:
            pass

        return False


# class OpencvGaussianblur(cm.CommandModel):
#     def __init__(self, command_name, setting_master, display_master, setting=None):
#         super().__init__(command_name, setting_master, display_master)
#         self.input = {"src": None}
#         self.output = {"dst": f"{self.command_name}.dst"}
#         self.setting = {
#                 "ksize_w": 3,
#                 "ksize_h": 3,
#                 "sigmaX": 0.0,
#                 "sigmaY": 0.0,
#                 "borderType": cv2.BORDER_DEFAULT
#                 }

#         if bool(setting):
#             self.set(setting)


#     def setting_widget_get(self):
#         input = {}
#         output = {}
#         setting = {
#             "ksize_w": wg.FwScale(self.setting_widget, "Kernel size width", 1, 255, self.setting["ksize_w"], resolution=2, value_type=int),
#             "ksize_h": wg.FwScale(self.setting_widget, "Kernel size height", 1, 255, self.setting["ksize_h"], resolution=2, value_type=int),
#             "sigmaX": wg.FwScale(self.setting_widget, "Sigma x", 0, 1, self.setting["sigmaX"], resolution=0.1),
#             "sigmaY": wg.FwScale(self.setting_widget, "Sigma y", 0, 1, self.setting["sigmaY"], resolution=0.1),
#             "borderType": wg.FwCombobox(self.setting_widget, "Interpolation", ENUM_BORDERTYPES, self.setting["borderType"])
#             }

#         self.setting_widget_set(input, output, setting)

#         return self.setting_widget


#     def run(self, images):
#         self.copy_widget2model()

#         src = self.input["src"]
#         ksize_w = self.setting["ksize_w"]
#         ksize_h = self.setting["ksize_h"]
#         sigmaX = self.setting["sigmaX"]
#         sigmaY = self.setting["sigmaY"]
#         borderType = self.setting["borderType"]
#         dst = self.output["dst"]

#         try:
#             if bool(src) and len(images[src]) > 0:
#                 image = cv2.GaussianBlur(images[src], ksize=(ksize_w, ksize_h), sigmaX=sigmaX, sigmaY=sigmaY, borderType=borderType)
#                 images.update({dst: image})
#                 return True
#         except:
#             pass

#         return False


# class OpencvCanny(cm.CommandModel):
#     def __init__(self, command_name, setting_master, display_master, setting=None):
#         super().__init__(command_name, setting_master, display_master)
#         self.input = {"src": None}
#         self.output = {"dst": f"{self.command_name}.dst"}
#         self.setting = {
#                 "threshold1": 100,
#                 "threshold2": 200,
#                 "apertureSize": 3,
#                 "L2gradient": False
#                 }

#         if bool(setting):
#             self.set(setting)


#     def setting_widget_get(self):
#         input = {}
#         output = {}
#         setting = {
#             "threshold1": wg.FwScale(self.setting_widget, "Threshold 1", 0, 255, self.setting["threshold1"]),
#             "threshold2": wg.FwScale(self.setting_widget, "Threshold 2", 0, 255, self.setting["threshold2"]),
#             "apertureSize": wg.FwScale(self.setting_widget, "Aperture size", 0, 255, self.setting["apertureSize"], value_type=int),
#             "L2gradient": wg.FwCheckbutton(self.setting_widget, "L2 gradient", "L2gradient", self.setting["L2gradient"])
#             }

#         self.setting_widget_set(input, output, setting)

#         return self.setting_widget


#     def run(self, images):
#         self.copy_widget2model()

#         src = self.input["src"]
#         dst = self.output["dst"]
#         threshold1 = self.setting["threshold1"]
#         threshold2 = self.setting["threshold2"]
#         apertureSize = self.setting["apertureSize"]
#         L2gradient = self.setting["L2gradient"]

#         try:
#             if bool(src) and len(images[src]) > 0:
#                 image = cv2.Canny(images[src], threshold1=threshold1, threshold2=threshold2, apertureSize=apertureSize, L2gradient=L2gradient)
#                 images.update({dst: image})
#                 return True
#         except:
#             pass

#         return False


# class OpencvResize(cm.CommandModel):
#     def __init__(self, command_name, setting_master, display_master, setting=None):
#         super().__init__(command_name, setting_master, display_master)
#         self.input = {"src": None}
#         self.output = {"dst": f"{self.command_name}.dst"}
#         self.setting = {
#                 "dsize_w": 0,
#                 "dsize_h": 0,
#                 "fx": 0.3,
#                 "fy": 0.3,
#                 "interpolation": cv2.INTER_NEAREST
#                 }

#         if bool(setting):
#             self.set(setting)


#     def setting_widget_get(self):
#         input = {}
#         output = {}
#         setting = {
#             "dsize_w": wg.FwScale(self.setting_widget, "Width", 0, 255, self.setting["dsize_w"], value_type=int),
#             "dsize_h": wg.FwScale(self.setting_widget, "Height", 0, 255, self.setting["dsize_h"], value_type=int),
#             "fx": wg.FwScale(self.setting_widget, "Factor x", 0, 1, self.setting["fx"], resolution=0.1),
#             "fy": wg.FwScale(self.setting_widget, "Factor y", 0, 1, self.setting["fy"], resolution=0.1),
#             "interpolation": wg.FwCombobox(self.setting_widget, "Interpolation", ENUM_INTERPOLATION_FLAGS, self.setting["interpolation"])
#             }

#         self.setting_widget_set(input, output, setting)

#         return self.setting_widget


#     def run(self, images):
#         self.copy_widget2model()

#         src = self.input["src"]
#         dst = self.output["dst"]
#         dsize_w = self.setting["dsize_w"]
#         dsize_h = self.setting["dsize_h"]
#         fx = self.setting["fx"]
#         fy = self.setting["fy"]
#         interpolation = self.setting["interpolation"]

#         try:
#             if bool(src) and len(images[src]) > 0:
#                 image = cv2.resize(images[src], dsize=(dsize_w, dsize_h), fx=fx, fy=fy, interpolation=interpolation)
#                 images.update({dst: image})
#                 return True
#         except:
#             pass

#         return False
