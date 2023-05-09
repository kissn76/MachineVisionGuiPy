class Command():
    def init(self):
        if self.command_model.command_name.startswith("tk_display"):
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
