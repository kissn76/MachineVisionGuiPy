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
                "filename": None,
                "flags": None
                }

        elif self.command_name.startswith("opencv_threshold"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "thresh": None,
                "maxval": None,
                "type": None
                }

        elif self.command_name.startswith("opencv_resize"):
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "dsize_w": None,
                "dsize_h": None,
                "fx": None,
                "fy": None,
                "interpolation": None
                }

        elif self.command_name.startswith("tk_display"):
            input_list = {"src": None}

        self.parameters.update({"input": input_list})
        self.parameters.update({"output": output_list})
        self.parameters.update({"setting": setting_list})
