import cv2
import basecommand as bc
import widgets as wg
from enums import *


class TkDisplay(bc.BaseCommand):
    def __init__(self, command_model, setting_master, display_master):
        super().__init__(command_model, setting_master, display_master)
        # DEFAULT VALUES
        self.command_model_input = {"src": None}
        self.command_model_output = {}
        self.command_model_properties = {
            "factor": 0.2
            }

        self.set_model()

        self.setting_widget_properties = {
            "factor": wg.FwScale(self.setting_widget, "Size factor", 0, 1, self.command_model.properties["factor"], resolution=0.1)
            }

        self.set_setting_widget()

        self.display_widget_properties = {
            "image": wg.FwImage(self.display_widget, None, scale_factor=self.command_model.properties["factor"])
            }

        self.set_display_widget()


    def run(self, images):
        src = self.command_model.input["src"]
        factor = self.command_model.properties["factor"]

        try:
            if bool(src) and len(images[src]) > 0:
                self.display_widget_properties["image"].set_scale_factor(factor)
                image = images[src]
                self.display_widget_properties["image"].set(image)
                return True
        except:
            pass

        return False
