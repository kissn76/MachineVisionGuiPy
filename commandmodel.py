from enums import *


class CommandModel():
    def __init__(self, command_name):
        self.command_name = command_name
        self.parameters = {}

        self.init()


    def init(self):
        input_list = {}
        output_list = {}
        setting_list = {}

        if self.command_name.startswith("opencv_imread"):
            output_list = {"output": f"{self.command_name}.out"}
            setting_list = {
                "filename": "./resources/example/ocv_1.jpg",
                "flags": cv2.IMREAD_UNCHANGED
                }

        elif self.command_name.startswith("opencv_threshold"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "thresh": 150,
                "maxval": 255,
                "type": cv2.THRESH_BINARY
                }

        elif self.command_name.startswith("opencv_gaussianblur"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "ksize_w": 3,
                "ksize_h": 3,
                "sigmaX": 0.0,
                "sigmaY": 0.0,
                "borderType": cv2.BORDER_DEFAULT
                }

        elif self.command_name.startswith("opencv_resize"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "dsize_w": 0,
                "dsize_h": 0,
                "fx": 0.3,
                "fy": 0.3,
                "interpolation": cv2.INTER_NEAREST
                }

        elif self.command_name.startswith("opencv_canny"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "threshold1": 100,
                "threshold2": 200,
                "apertureSize": 3,
                "L2gradient": False
                }

        elif self.command_name.startswith("tk_display"):
            input_list = {"src": None}

        self.parameters.update({"input": input_list})
        self.parameters.update({"output": output_list})
        self.parameters.update({"setting": setting_list})


    def set(self, setting):
        for key in self.parameters["input"].keys():
            self.parameters["input"][key] = setting["input"][key]

        for key in self.parameters["output"].keys():
            self.parameters["output"][key] = setting["output"][key]

        for key in self.parameters["setting"].keys():
            self.parameters["setting"][key] = setting["setting"][key]
