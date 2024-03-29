import commandmodel as cm
import command_openvc_input as coi
import command_opencv_processing as cop
import command_tk as ctk


class Command():
    def __init__(self, command, setting_master, display_master, setting=None):
        self.command_model = cm.CommandModel(command, setting)
        self.command_name = self.command_model.command_name
        self.command_object = None
        self.frm_setting_main = None
        self.run = None

        if self.command_name.startswith("opencv_videocapture"):
            self.command_object = coi.OpencvVideoCapture(self.command_model, setting_master, display_master)
        elif self.command_name.startswith("opencv_imread"):
            self.command_object = coi.OpencvImread(self.command_model, setting_master, display_master)
        elif self.command_name.startswith("opencv_threshold"):
            self.command_object = cop.OpencvThreshold(self.command_model, setting_master, display_master)
        elif self.command_name.startswith("opencv_gaussianblur"):
            self.command_object = cop.OpencvGaussianblur(self.command_model, setting_master, display_master)
        elif self.command_name.startswith("opencv_resize"):
            self.command_object = cop.OpencvResize(self.command_model, setting_master, display_master)
        elif self.command_name.startswith("opencv_canny"):
            self.command_object = cop.OpencvCanny(self.command_model, setting_master, display_master)
        elif self.command_name.startswith("tk_display"):
            self.command_object = ctk.TkDisplay(self.command_model, setting_master, display_master)

        if bool(self.command_object):
            self.frm_setting_main = self.command_object.setting_widget_get()
            self.run = self.command_object.run


    def __repr__(self):
        return {self.command_name: {"model": self.command_model}}.__repr__()


    def __str__(self):
        return {self.command_name: {"model": self.command_model}}.__str__()


    def to_dict(self):
        return {self.command_name: {"model": self.command_model.to_dict()}}


    def update(self):
        for key, widget in self.frm_setting_main.widget_elements["properties"].items():
            if bool(widget):
                newvalue = widget.get()
                self.command_model.set_propertie_value(key, newvalue)
