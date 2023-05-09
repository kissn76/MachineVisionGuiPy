class CommandModel():
    def init(self):

        if self.command_name.startswith("opencv_resize"):
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
