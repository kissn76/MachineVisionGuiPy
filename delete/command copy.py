class Command():
    def init(self):
        if self.command_model.command_name.startswith("opencv_resize"):
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

        elif self.command_model.command_name.startswith("opencv_canny"):
            def run_command(images):
                self.frm_setting_main.get()

                src = self.command_model.parameters["input"]["src"]
                dst = self.command_model.parameters["output"]["dst"]
                threshold1 = self.command_model.parameters["setting"]["threshold1"]
                threshold2 = self.command_model.parameters["setting"]["threshold2"]
                apertureSize = self.command_model.parameters["setting"]["apertureSize"]
                L2gradient = self.command_model.parameters["setting"]["L2gradient"]

                try:
                    if bool(src) and len(images[src]) > 0:
                        image = cv2.Canny(images[src], threshold1=threshold1, threshold2=threshold2, apertureSize=apertureSize, L2gradient=L2gradient)
                        images.update({dst: image})
                        return True
                except:
                    pass

                return False

            self.run = run_command

        elif self.command_model.command_name.startswith("tk_display"):
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
