from enums import *


class CommandModel():
    def __init__(self, command_name):
        self.command_name = command_name
        self.parameters = {}

        self.set()


    def set(self):
        input_list = {}
        output_list = {}
        setting_list = {}

        if self.command_name.startswith("opencv_imread"):
            output_list = {"output": f"{self.command_name}.out"}
            setting_list = {
                "filename": "./resources/example/ocv_1.jpg",
                "flags": tuple(ENUM_IMREAD_MODES.values()).index(cv2.IMREAD_UNCHANGED)
                }

        elif self.command_name.startswith("opencv_threshold"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "thresh": 150,
                "maxval": 255,
                "type": tuple(ENUM_THRESHOLD_TYPES.values()).index(cv2.THRESH_BINARY)
                }

        elif self.command_name.startswith("opencv_resize"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "dsize_w": 0,
                "dsize_h": 0,
                "fx": 0.3,
                "fy": 0.3,
                "interpolation": tuple(ENUM_INTERPOLATION_FLAGS.values()).index(cv2.INTER_NEAREST)
                }

        elif self.command_name.startswith("tk_display"):
            input_list = {"src": None}

        self.parameters.update({"input": input_list})
        self.parameters.update({"output": output_list})
        self.parameters.update({"setting": setting_list})
