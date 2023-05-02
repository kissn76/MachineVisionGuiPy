import cv2
from pathlib import Path
from enums import *
import settinggui as sg
import displaygui as dg
import commandmodel as cm


command_counter = 0     # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs


class Command():
    def __init__(self, command, setting_master, display_master):
        global command_counter
        self.command_name = f"{command}.{command_counter}"
        command_counter += 1

        self.command_model = cm.CommandModel(self.command_name)

        # setting widget
        self.frm_setting_main = sg.SettingGui(setting_master, self.command_model)

        # display widget
        self.frm_display_main = dg.DisplayGui(display_master, self.command_model)

        self.run = None

        self.set()


    def set(self):
        if self.command_name.startswith("opencv_imread"):
            def run_command(images):
                self.frm_setting_main.get()

                filename = self.command_model.parameters["setting"]["filename"]
                flags = self.command_model.parameters["setting"]["flags"]
                output = self.command_model.parameters["output"]["output"]

                try:
                    if Path(filename).is_file():
                        image = cv2.imread(filename, flags)
                        images.update({output: image})
                        return True
                except:
                    pass

                return False

            self.run = run_command

        elif self.command_name.startswith("opencv_threshold"):
            def run_command(images):
                self.frm_setting_main.get()

                src = self.command_model.parameters["input"]["src"]
                dst = self.command_model.parameters["output"]["dst"]
                thresh = self.command_model.parameters["setting"]["thresh"]
                maxval = self.command_model.parameters["setting"]["maxval"]
                type = self.command_model.parameters["setting"]["type"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        _, image = cv2.threshold(images[src], thresh=thresh, maxval=maxval, type=type)
                        images.update({dst: image})
                        return True
                except:
                    pass

                return False

            self.run = run_command

        elif self.command_name.startswith("opencv_resize"):
            def run_command(images):
                self.frm_setting_main.get()

                src = self.command_model.parameters["input"]["src"]
                dst = self.command_model.parameters["output"]["dst"]
                dsize_w = self.command_model.parameters["setting"]["dsize_w"]
                dsize_h = self.command_model.parameters["setting"]["dsize_h"]
                fx = self.command_model.parameters["setting"]["fx"]
                fy = self.command_model.parameters["setting"]["fy"]
                interpolation = self.command_model.parameters["setting"]["interpolation"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        image = cv2.resize(images[src], dsize=(dsize_w, dsize_h), fx=fx, fy=fy, interpolation=interpolation)
                        images.update({dst: image})
                        return True
                except:
                    pass

                return False

            self.run = run_command

        elif self.command_name.startswith("tk_display"):
            def run_command(images):
                src = self.command_model.parameters["input"]["src"]
                display_obj = self.frm_display_main.widget_list["display"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        display_obj.set(images[src])
                        return True
                except:
                    pass

                return False

            self.run = run_command
