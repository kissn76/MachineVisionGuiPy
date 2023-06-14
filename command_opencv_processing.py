import cv2
import basecommand as bc
import widgets as wg
from enums import *


class OpencvThreshold(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        # DEFAULT VALUES
        self.command_model_input = {"src": None}
        self.command_model_output = {"dst": f"{self.command_model.command_name}.dst"}
        self.command_model_properties = {
            "thresh": 150,
            "maxval": 255,
            "type": cv2.THRESH_BINARY
            }

        self.set_model()

        self.setting_widget_properties = {
            "thresh": wg.FwScale(self.setting_widget, "Threshold", 0, 255, self.command_model.properties["thresh"]),
            "maxval": wg.FwScale(self.setting_widget, "Maximum value", 0, 255, self.command_model.properties["maxval"]),
            "type": wg.FwCombobox(self.setting_widget, "Type", ENUM_THRESHOLD_TYPES, self.command_model.properties["type"])
            }

        self.set_setting_widget()


    def run(self, images):
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


class OpencvGaussianblur(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        # DEFAULT VALUES
        self.command_model_input = {
                                    "src": None,
                                    }
        self.command_model_output = {
                                    "dst": f"{self.command_model.command_name}.dst",
                                    }
        self.command_model_properties = {
                "ksize_w": 3,
                "ksize_h": 3,
                "sigmaX": 0.0,
                "sigmaY": 0.0,
                "borderType": cv2.BORDER_DEFAULT
                }

        self.set_model()

        self.setting_widget_input = {}
        self.setting_widget_output = {}
        self.setting_widget_properties = {
            "ksize_w": wg.FwScale(self.setting_widget, "Kernel size width", 1, 255, self.command_model.properties["ksize_w"], resolution=2, value_type=int),
            "ksize_h": wg.FwScale(self.setting_widget, "Kernel size height", 1, 255, self.command_model.properties["ksize_h"], resolution=2, value_type=int),
            "sigmaX": wg.FwScale(self.setting_widget, "Sigma x", 0, 1, self.command_model.properties["sigmaX"], resolution=0.1),
            "sigmaY": wg.FwScale(self.setting_widget, "Sigma y", 0, 1, self.command_model.properties["sigmaY"], resolution=0.1),
            "borderType": wg.FwCombobox(self.setting_widget, "Interpolation", ENUM_BORDERTYPES, self.command_model.properties["borderType"])
            }

        self.set_setting_widget()


    def run(self, images):
        src = self.command_model.input["src"]
        ksize_w = self.command_model.properties["ksize_w"]
        ksize_h = self.command_model.properties["ksize_h"]
        sigmaX = self.command_model.properties["sigmaX"]
        sigmaY = self.command_model.properties["sigmaY"]
        borderType = self.command_model.properties["borderType"]
        dst = self.command_model.output["dst"]

        try:
            if bool(src) and len(images[src]) > 0:
                image = cv2.GaussianBlur(images[src], ksize=(ksize_w, ksize_h), sigmaX=sigmaX, sigmaY=sigmaY, borderType=borderType)
                images.update({dst: image})
                return True
        except:
            pass

        return False


class OpencvCanny(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        # DEFAULT VALUES
        self.command_model_input = {"src": None}
        self.command_model_output = {"dst": f"{self.command_model.command_name}.dst"}
        self.command_model_properties = {
            "threshold1": 100,
            "threshold2": 200,
            "apertureSize": 3,
            "L2gradient": False
            }

        self.set_model()

        self.setting_widget_input = {}
        self.setting_widget_output = {}
        self.setting_widget_properties = {
            "threshold1": wg.FwScale(self.setting_widget, "Threshold 1", 0, 255, self.command_model.properties["threshold1"]),
            "threshold2": wg.FwScale(self.setting_widget, "Threshold 2", 0, 255, self.command_model.properties["threshold2"]),
            "apertureSize": wg.FwScale(self.setting_widget, "Aperture size", 3, 7, self.command_model.properties["apertureSize"], value_type=int),
            "L2gradient": wg.FwCheckbutton(self.setting_widget, "L2 gradient", "L2gradient", self.command_model.properties["L2gradient"])
            }

        self.set_setting_widget()


    def run(self, images):
        src = self.command_model.input["src"]
        dst = self.command_model.output["dst"]
        threshold1 = self.command_model.properties["threshold1"]
        threshold2 = self.command_model.properties["threshold2"]
        apertureSize = self.command_model.properties["apertureSize"]
        L2gradient = self.command_model.properties["L2gradient"]

        try:
            if bool(src) and len(images[src]) > 0:
                image = cv2.Canny(images[src], threshold1=threshold1, threshold2=threshold2, apertureSize=apertureSize, L2gradient=L2gradient)
                images.update({dst: image})
                return True
        except:
            pass

        return False


class OpencvResize(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        # DEFAULT VALUES
        self.command_model_input = {"src": None}
        self.command_model_output = {"dst": f"{self.command_model.command_name}.dst"}
        self.command_model_properties = {
            "dsize_w": 0,
            "dsize_h": 0,
            "fx": 0.3,
            "fy": 0.3,
            "interpolation": cv2.INTER_NEAREST
            }

        self.set_model()

        self.setting_widget_input = {}
        self.setting_widget_output = {}
        self.setting_widget_properties = {
            "dsize_w": wg.FwScale(self.setting_widget, "Width", 0, 255, self.command_model.properties["dsize_w"], value_type=int),
            "dsize_h": wg.FwScale(self.setting_widget, "Height", 0, 255, self.command_model.properties["dsize_h"], value_type=int),
            "fx": wg.FwScale(self.setting_widget, "Factor x", 0, 1, self.command_model.properties["fx"], resolution=0.1),
            "fy": wg.FwScale(self.setting_widget, "Factor y", 0, 1, self.command_model.properties["fy"], resolution=0.1),
            "interpolation": wg.FwCombobox(self.setting_widget, "Interpolation", ENUM_INTERPOLATION_FLAGS, self.command_model.properties["interpolation"])
            }

        self.set_setting_widget()


    def run(self, images):
        src = self.command_model.input["src"]
        dst = self.command_model.output["dst"]
        dsize_w = self.command_model.properties["dsize_w"]
        dsize_h = self.command_model.properties["dsize_h"]
        fx = self.command_model.properties["fx"]
        fy = self.command_model.properties["fy"]
        interpolation = self.command_model.properties["interpolation"]

        try:
            if bool(src) and len(images[src]) > 0:
                image = cv2.resize(images[src], dsize=(dsize_w, dsize_h), fx=fx, fy=fy, interpolation=interpolation)
                images.update({dst: image})
                return True
        except:
            pass

        return False
