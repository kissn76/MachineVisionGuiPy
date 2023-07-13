command_counter = 0     # a parancs nevéhez egy counter, hogy ne legyen két egyforma nevű parancs


class CommandModel():
    def __init__(self, command, setting=None):
        self.command_name = None
        self.input = {}
        self.output = {}
        self.properties = {}

        global command_counter
        if bool(setting):
            # counter beállítása a mentett maximális utáni értékre
            counter = int(command[command.rindex(".") + 1:]) + 1
            if counter > command_counter:
                command_counter = counter

            self.set(setting)
        else:
            command = f"{command}.{command_counter}"
            command_counter += 1

        self.command_name = command


    def __repr__(self):
         return {"input": self.input, "output": self.output, "properties": self.properties}.__repr__()


    def __str__(self):
         return {"input": self.input, "output": self.output, "properties": self.properties}.__str__()


    def __dict__(self):
         return {"input": self.input, "output": self.output, "properties": self.properties}


    def set(self, setting):
        self.set_input(setting["input"])
        self.set_output(setting["output"])
        self.set_properties(setting["properties"])


    def set_input(self, input):
        self.input.clear()
        for key in input.keys():
            self.input.update({key: input[key]})


    def set_output(self, output):
        self.output.clear()
        for key in output.keys():
            self.output.update({key: output[key]})


    def set_properties(self, properties):
        self.properties.clear()
        for key in properties.keys():
            self.properties.update({key: properties[key]})


    def set_propertie_value(self, propertie_key, new_value):
        self.properties[propertie_key] = new_value
