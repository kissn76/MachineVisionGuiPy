from enums import *
import command_openvc_input as coi


command_counter = 0     # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs


class Command():
    def __init__(self, command, setting_master, display_master, setting=None):
        global command_counter
        if command.startswith("opencv_videocapture_index"):
            self.command_model = coi.OpencvVideoCapture(f"{command}.{command_counter}")
        command_counter += 1

        # setting widget
        self.frm_setting_main = self.command_model.setting_widget_get(setting_master)

        # display widget
        self.frm_display_main = self.command_model.display_widget_get(display_master)

        self.run = self.command_model.run
