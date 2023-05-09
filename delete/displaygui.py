class DisplayGui(ttk.Frame):
    def init(self):
        if self.command_model.command_name.startswith("tk_display"):
            self.widget_list.update({"display": wg.FwImage(self, "Image")})