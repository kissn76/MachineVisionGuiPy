class SettingGui(ttk.Frame):
    def init(self):
        if self.command_model.command_name.startswith("opencv_resize"):
            # input_list = {"src": wg.FwEntry(self, "Source", None)}
            # output_list = {"dst": wg.FwEntry(self, "Destination", f"{self.command_model.command_name}.dst")}
            setting_list = {
                "dsize_w": wg.FwScale(self, "Width", 0, 255, self.command_model.parameters["setting"]["dsize_w"], value_type=int),
                "dsize_h": wg.FwScale(self, "Height", 0, 255, self.command_model.parameters["setting"]["dsize_h"], value_type=int),
                "fx": wg.FwScale(self, "Factor x", 0, 1, self.command_model.parameters["setting"]["fx"], resolution=0.1),
                "fy": wg.FwScale(self, "Factor y", 0, 1, self.command_model.parameters["setting"]["fy"], resolution=0.1),
                "interpolation": wg.FwCombobox(self, "Interpolation", ENUM_INTERPOLATION_FLAGS, self.command_model.parameters["setting"]["interpolation"])
                }

        elif self.command_model.command_name.startswith("opencv_canny"):
            setting_list = {
                "threshold1": wg.FwScale(self, "Threshold 1", 0, 255, self.command_model.parameters["setting"]["threshold1"]),
                "threshold2": wg.FwScale(self, "Threshold 2", 0, 255, self.command_model.parameters["setting"]["threshold2"]),
                "apertureSize": wg.FwScale(self, "Aperture size", 0, 255, self.command_model.parameters["setting"]["apertureSize"], value_type=int),
                "L2gradient": wg.FwCheckbutton(self, "L2 gradient", "L2gradient", self.command_model.parameters["setting"]["L2gradient"])
                }
