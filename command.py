from enums import *
import command_openvc_input as coi
import command_opencv_processing as cop


command_counter = 0     # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs


class Command():
    def __init__(self, command, setting_master, display_master, setting=None):
        global command_counter
        if bool(setting):
            # counter beállítása a mentett maximális utáni értékre
            counter = int(command[command.rindex(".") + 1:]) + 1
            if counter > command_counter:
                command_counter = counter
        else:
            command = f"{command}.{command_counter}"
            command_counter += 1

        self.command_model = None

        if command.startswith("opencv_videocapture"):
            self.command_model = coi.OpencvVideoCapture(command, setting_master, display_master, setting)
        elif command.startswith("opencv_imread"):
            self.command_model = coi.OpencvImread(command, setting_master, display_master, setting)
        elif command.startswith("opencv_threshold"):
            self.command_model = cop.OpencvThreshold(command, setting_master, display_master, setting)
        elif command.startswith("opencv_gaussianblur"):
            self.command_model = cop.OpencvGaussianblur(command, setting_master, display_master, setting)
        elif command.startswith("opencv_resize"):
            self.command_model = cop.OpencvResize(command, setting_master, display_master, setting)
        elif command.startswith("opencv_canny"):
            self.command_model = cop.OpencvCanny(command, setting_master, display_master, setting)

        # setting widget
        self.frm_setting_main = self.command_model.setting_widget_get()

        # display widget
        self.frm_display_main = self.command_model.display_widget_get()

        self.run = self.command_model.run
