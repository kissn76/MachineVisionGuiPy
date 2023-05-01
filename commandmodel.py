import cv2
from pathlib import Path



class CommandModel():
    def __init__(self, command_name):
        self.command_name = command_name
        self.parameters = {}
        self.run = None

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

            def run_command(images):
                filename = self.parameters["setting"]["filename"]
                flags = self.parameters["setting"]["flags"]
                output = self.parameters["output"]["output"]

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
            input_list = {"src": None}
            output_list = {"dst": f"{self.command_name}.dst"}
            setting_list = {
                "thresh": None,
                "maxval": None,
                "type": None
                }

            def run_command(images):
                src = self.parameters["input"]["src"]
                dst = self.parameters["output"]["dst"]
                thresh = self.parameters["setting"]["thresh"]
                maxval = self.parameters["setting"]["maxval"]
                type = self.parameters["setting"]["type"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        _, image = cv2.threshold(images[src], thresh, maxval, type)
                        images.update({dst: image})
                        return True
                except:
                    pass

                return False

            self.run = run_command

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

            def run_command(images):
                src = self.parameters["input"]["src"]
                dst = self.parameters["output"]["dst"]
                dsize_w = self.parameters["setting"]["dsize_w"]
                dsize_h = self.parameters["setting"]["dsize_h"]
                fx = self.parameters["setting"]["fx"]
                fy = self.parameters["setting"]["fy"]
                interpolation = self.parameters["setting"]["interpolation"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        image = cv2.resize(src, dsize=(dsize_w, dsize_h), fx=fx, fy=fy, interpolation=interpolation)
                        images.update({dst: image})
                        return True
                except:
                    pass

                return False

            self.run = run_command

        elif self.command_name.startswith("tk_display"):
            def run_command(images):
                src = self.setting_widget_list["input"]["src"].get()
                display_obj = self.display_widget_list["display"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        display_obj.set(images[src])
                        return True
                except:
                    pass

                return False

            self.run = run_command

        self.parameters.update({"input": input_list})
        self.parameters.update({"output": output_list})
        self.parameters.update({"setting": setting_list})
