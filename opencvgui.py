import cv2
import tkinter as tk
from tkinter import ttk
from pathlib import Path


ENUM_IMREAD_MODES = {
    "IMREAD_UNCHANGED": cv2.IMREAD_UNCHANGED,
    "IMREAD_GRAYSCALE": cv2.IMREAD_GRAYSCALE,
    "IMREAD_COLOR": cv2.IMREAD_COLOR,
    "IMREAD_ANYDEPTH": cv2.IMREAD_ANYDEPTH,
    "IMREAD_ANYCOLOR": cv2.IMREAD_ANYCOLOR,
    "IMREAD_LOAD_GDAL": cv2.IMREAD_LOAD_GDAL,
    "IMREAD_REDUCED_GRAYSCALE_2": cv2.IMREAD_REDUCED_GRAYSCALE_2,
    "IMREAD_REDUCED_COLOR_2": cv2.IMREAD_REDUCED_COLOR_2,
    "IMREAD_REDUCED_GRAYSCALE_4": cv2.IMREAD_REDUCED_GRAYSCALE_4,
    "IMREAD_REDUCED_COLOR_4": cv2.IMREAD_REDUCED_COLOR_4,
    "IMREAD_REDUCED_GRAYSCALE_8": cv2.IMREAD_REDUCED_GRAYSCALE_8,
    "IMREAD_REDUCED_COLOR_8": cv2.IMREAD_REDUCED_COLOR_8,
    "IMREAD_IGNORE_ORIENTATION": cv2.IMREAD_IGNORE_ORIENTATION
}

ENUM_THRESHOLD_TYPES = {
    "THRESH_BINARY": cv2.THRESH_BINARY,
    "THRESH_BINARY_INV": cv2.THRESH_BINARY_INV,
    "THRESH_TRUNC": cv2.THRESH_TRUNC,
    "THRESH_TOZERO": cv2.THRESH_TOZERO,
    "THRESH_TOZERO_INV": cv2.THRESH_TOZERO_INV,
    "THRESH_MASK": cv2.THRESH_MASK,
    "THRESH_OTSU": cv2.THRESH_OTSU,
    "THRESH_TRIANGLE": cv2.THRESH_TRIANGLE
}

ENUM_INTERPOLATION_FLAGS = {
    "INTER_NEAREST": cv2.INTER_NEAREST,
    "INTER_LINEAR": cv2.INTER_LINEAR,
    "INTER_CUBIC": cv2.INTER_CUBIC,
    "INTER_AREA": cv2.INTER_AREA,
    "INTER_LANCZOS4": cv2.INTER_LANCZOS4,
    "INTER_LINEAR_EXACT": cv2.INTER_LINEAR_EXACT,
    "INTER_NEAREST_EXACT": cv2.INTER_NEAREST_EXACT,
    "INTER_MAX": cv2.INTER_MAX,
    "WARP_FILL_OUTLIERS": cv2.WARP_FILL_OUTLIERS,
    "WARP_INVERSE_MAP": cv2.WARP_INVERSE_MAP
}


class ImreadGui(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)


        self.input = None
        self.output = {"ret": f"{name}.ret"}
        self.filename = None
        self.filename = "resources/example/ocv_1.jpg"
        # self.flags = cv2.IMREAD_COLOR
        self.flags = cv2.IMREAD_GRAYSCALE

        self.var_filename = tk.StringVar()
        self.ent_filename = tk.Entry(self, textvariable=self.var_filename)
        self.var_filename.set(self.filename)

        self.var_flags = tk.StringVar()
        self.cbx_flags = ttk.Combobox(self, textvariable=self.var_flags, state="readonly")
        self.cbx_flags.config(values=tuple(ENUM_IMREAD_MODES.keys()))
        self.cbx_flags.current(newindex=tuple(ENUM_IMREAD_MODES.values()).index(self.flags))

        self.lbl_dst = tk.Label(self, text=self.output)

        self.ent_filename.grid(row=0, column=0)
        self.cbx_flags.grid(row=1, column=0)
        self.lbl_dst.grid(row=2, column=0)

        self.set_values()


    def set_setting(self, setting):
        if bool(setting):
            self.var_filename.set(setting["filename"])
            self.var_flags.set(setting["flags"])
            self.cbx_flags.current(newindex=tuple(ENUM_IMREAD_MODES.values()).index(setting["flags"]))
            self.input = setting["input"]
            self.output =  setting["output"]

            self.set_values()


    def get_setting(self):
        setting = {}

        self.set_values()

        setting.update({"input": self.input})
        setting.update({"output": self.output})
        setting.update({"filename": self.filename})
        setting.update({"flags": self.flags})

        return setting


    def get_input(self):
        return self.input


    def get_output(self):
        return self.output


    def run_process(self, images):
        self.set_values()

        image = None
        try:
            if Path(self.filename).is_file():
                image = cv2.imread(self.filename, self.flags)
                images.update({self.output["ret"]: image})
        except:
            pass


    def set_values(self):
        self.filename = self.var_filename.get()
        self.flags = ENUM_IMREAD_MODES[self.var_flags.get()]


class ThresholdGui(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)

        self.input = {"src": None}
        self.output = {"dst": f"{name}.dst"}
        self.thresh = 150.0
        self.maxval = 255.0
        self.type = cv2.THRESH_BINARY

        self.var_thresh = tk.DoubleVar()
        scl_thresh = tk.Scale(self, variable=self.var_thresh, from_=0, to=255, orient=tk.HORIZONTAL)
        scl_thresh.set(self.thresh)

        self.var_maxval = tk.DoubleVar()
        scl_maxval = tk.Scale(self, variable=self.var_maxval, from_=0, to=255, orient=tk.HORIZONTAL)
        scl_maxval.set(self.maxval)

        self.var_type = tk.StringVar()
        self.cbx_type = ttk.Combobox(self, textvariable=self.var_type, state="readonly")
        self.cbx_type.config(values=tuple(ENUM_THRESHOLD_TYPES.keys()))
        self.cbx_type.current(newindex=tuple(ENUM_THRESHOLD_TYPES.values()).index(self.type))

        self.lbl_dst = tk.Label(self, text=self.output)

        scl_thresh.grid(row=0, column=0)
        scl_maxval.grid(row=0, column=1)
        self.cbx_type.grid(row=1, column=0, columnspan=2)
        self.lbl_dst.grid(row=2, column=0, columnspan=2)

        self.set_values()


    def set_setting(self, setting):
        if bool(setting):
            self.var_thresh.set(setting["thresh"])
            self.var_maxval.set(setting["maxval"])
            self.var_type.set(setting["type"])
            self.cbx_type.current(newindex=tuple(ENUM_THRESHOLD_TYPES.values()).index(setting["type"]))
            self.input = setting["input"]
            self.output =  setting["output"]

            self.set_values()


    def get_setting(self):
        setting = {}

        self.set_values()

        setting.update({"input": self.input})
        setting.update({"output": self.output})
        setting.update({"thresh": self.thresh})
        setting.update({"maxval": self.maxval})
        setting.update({"type": self.type})

        return setting


    def get_input(self):
        return self.input


    def get_output(self):
        return self.output


    def run_process(self, image_list):
        self.set_values()

        image = None
        try:
            _, image = cv2.threshold(image_list[self.input["src"]], self.thresh, self.maxval, self.type)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            image_list.update({self.output["dst"]: image})
        except:
            pass


    def set_values(self):
        self.thresh = self.var_thresh.get()
        self.maxval = self.var_maxval.get()
        self.type = ENUM_THRESHOLD_TYPES[self.var_type.get()]


class ResizeGui(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)

        self.input = {"src": None}
        self.output = {"dst": f"{name}.dst"}
        self.dsize = (0, 0)
        self.fx = 0.3
        self.fy = 0.3
        self.interpolation = cv2.INTER_NEAREST

        self.var_dsize_width = tk.IntVar()
        scl_dsize_width = tk.Scale(self, variable=self.var_dsize_width, from_=0, to=255, orient=tk.HORIZONTAL, command=self.reset_factor)
        scl_dsize_width.set(self.dsize[0])

        self.var_dsize_height = tk.IntVar()
        scl_dsize_height = tk.Scale(self, variable=self.var_dsize_height, from_=0, to=255, orient=tk.HORIZONTAL, command=self.reset_factor)
        scl_dsize_height.set(self.dsize[1])

        self.var_fx = tk.DoubleVar()
        scl_fx = tk.Scale(self, variable=self.var_fx, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.reset_dsize)
        scl_fx.set(self.fx)

        self.var_fy = tk.DoubleVar()
        scl_fy = tk.Scale(self, variable=self.var_fy, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.reset_dsize)
        scl_fy.set(self.fy)

        self.var_interpolation = tk.StringVar()
        self.cbx_interpolation = ttk.Combobox(self, textvariable=self.var_interpolation, state="readonly")
        self.cbx_interpolation.config(values=tuple(ENUM_INTERPOLATION_FLAGS.keys()))
        self.cbx_interpolation.current(newindex=tuple(ENUM_INTERPOLATION_FLAGS.values()).index(self.interpolation))

        self.lbl_dst = tk.Label(self, text=self.output)

        scl_dsize_width.grid(row=0, column=0)
        scl_dsize_height.grid(row=0, column=1)
        scl_fx.grid(row=1, column=0)
        scl_fy.grid(row=1, column=1)
        self.cbx_interpolation.grid(row=2, column=0, columnspan=2)
        self.lbl_dst.grid(row=4, column=0, columnspan=2)

        self.set_values()


    def reset_factor(self, source):
        self.var_fx.set(0)
        self.var_fy.set(0)


    def reset_dsize(self, source):
        self.var_dsize_width.set(0)
        self.var_dsize_height.set(0)


    def set_setting(self, setting):
        if bool(setting):
            self.var_dsize_width.set(setting["dsize"][0])
            self.var_dsize_height.set(setting["dsize"][1])
            self.var_fx.set(setting["fx"])
            self.var_fy.set(setting["fy"])
            self.var_interpolation.set(setting["interpolation"])
            self.cbx_interpolation.current(newindex=tuple(ENUM_INTERPOLATION_FLAGS.values()).index(setting["interpolation"]))
            self.input = setting["input"]
            self.output =  setting["output"]

            self.set_values()


    def get_setting(self):
        setting = {}

        self.set_values()

        setting.update({"input": self.input})
        setting.update({"output": self.output})
        setting.update({"dsize": self.dsize})
        setting.update({"fx": self.fx})
        setting.update({"fy": self.fy})
        setting.update({"interpolation": self.interpolation})

        return setting


    def get_input(self):
        return self.input


    def get_output(self):
        return self.output


    def run_process(self, image_list):
        self.set_values()

        image = None
        try:
            image = cv2.resize(image_list[self.input["src"]], dsize=self.dsize, fx=self.fx, fy=self.fy, interpolation=self.interpolation)
            image_list.update({self.output["dst"]: image})
        except:
            pass


    def set_values(self):
        self.dsize = (self.var_dsize_width.get(), self.var_dsize_height.get())
        self.fx = self.var_fx.get()
        self.fy = self.var_fy.get()
        self.interpolation = ENUM_INTERPOLATION_FLAGS[self.var_interpolation.get()]
