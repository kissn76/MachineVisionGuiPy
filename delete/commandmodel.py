class CommandModel():
    def init(self):
        if self.command_name.startswith("tk_display"):
            input_list = {"src": None}
