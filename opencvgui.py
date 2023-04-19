import cv2
import tkinter as tk
from tkinter import ttk


enumImreadModes = {
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

enumThresholdTypes = {
    "THRESH_BINARY": cv2.THRESH_BINARY,
    "THRESH_BINARY_INV": cv2.THRESH_BINARY_INV,
    "THRESH_TRUNC": cv2.THRESH_TRUNC,
    "THRESH_TOZERO": cv2.THRESH_TOZERO,
    "THRESH_TOZERO_INV": cv2.THRESH_TOZERO_INV,
    "THRESH_MASK": cv2.THRESH_MASK,
    "THRESH_OTSU": cv2.THRESH_OTSU,
    "THRESH_TRIANGLE": cv2.THRESH_TRIANGLE
}

enumInterpolationFlags = {
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
    def __init__(self, master, parameters):
        super().__init__(master)

        self.filename = None
        self.flags = cv2.IMREAD_COLOR

        try:
            self.filename = parameters["filename"]
        except:
            pass

        try:
            self.flags = parameters["flags"]
        except:
            pass

        self.var_filename = tk.StringVar()
        self.ent_filename = tk.Entry(self, textvariable=self.var_filename)
        self.var_filename.set(self.filename)

        self.var_flags = tk.StringVar()
        self.cbx_flags = ttk.Combobox(self, textvariable=self.var_flags)
        self.cbx_flags.config(values=tuple(enumImreadModes.keys()))
        self.cbx_flags.current(newindex=tuple(enumImreadModes.values()).index(self.flags))
        self.cbx_flags.config(state="readonly")

        self.ent_filename.grid(row=0, column=0)
        self.cbx_flags.grid(row=1, column=0)


    def runProcess(self):
        self.getValues()

        dst = None
        try:
            dst = cv2.imread(self.filename, self.flags)
            dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
        except:
            pass

        return dst


    def getValues(self):
        self.filename = self.var_filename.get()
        self.flags = enumImreadModes[self.var_flags.get()]


class ThresholdGui(tk.Frame):
    def __init__(self, master, parameters):
        super().__init__(master)

        self.threshold_value = 0.0
        self.max_value = 255.0
        self.type = cv2.THRESH_BINARY

        try:
            self.threshold_value = parameters["threshold"]
        except:
            pass

        try:
            self.max_value = parameters["maxval"]
        except:
            pass

        try:
            self.type = parameters["type"]
        except:
            pass

        self.var_thval = tk.DoubleVar()
        scl_thval = tk.Scale(self, variable=self.var_thval, from_=0, to=255, orient=tk.HORIZONTAL)
        scl_thval.set(self.threshold_value)

        self.var_maxval = tk.DoubleVar()
        scl_maxval = tk.Scale(self, variable=self.var_maxval, from_=0, to=255, orient=tk.HORIZONTAL)
        scl_maxval.set(self.max_value)

        self.var_type = tk.StringVar()
        self.cbx_type = ttk.Combobox(self, textvariable=self.var_type)
        self.cbx_type.config(values=tuple(enumThresholdTypes.keys()))
        self.cbx_type.current(newindex=tuple(enumThresholdTypes.values()).index(self.type))
        self.cbx_type.config(state="readonly")

        scl_thval.grid(row=0, column=0)
        scl_maxval.grid(row=0, column=1)
        self.cbx_type.grid(row=1, column=0, columnspan=2)


    def runProcess(self, src):
        self.getValues()

        dst = None
        try:
            _, dst = cv2.threshold(src, self.threshold_value, self.max_value, self.type)
            dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
        except:
            pass

        return dst


    def getValues(self):
        self.threshold_value = self.var_thval.get()
        self.max_value = self.var_maxval.get()
        self.type = enumThresholdTypes[self.var_type.get()]


class ResizeGui(tk.Frame):
    def __init__(self, master, parameters):
        super().__init__(master)

        self.dsize = (0, 0)
        self.fx = 0.1
        self.fy = 0.1
        self.interpolation = cv2.INTER_NEAREST

        try:
            self.dsize = parameters["dsize"]
        except:
            pass

        try:
            self.fx = parameters["fx"]
        except:
            pass

        try:
            self.fy = parameters["fy"]
        except:
            pass

        try:
            self.interpolation = parameters["interpolation"]
        except:
            pass

        self.var_dsize_width = tk.IntVar()
        scl_dsize_width = tk.Scale(self, variable=self.var_dsize_width, from_=0, to=255, orient=tk.HORIZONTAL, command=self.resetFactor)
        scl_dsize_width.set(self.dsize[0])

        self.var_dsize_height = tk.IntVar()
        scl_dsize_height = tk.Scale(self, variable=self.var_dsize_height, from_=0, to=255, orient=tk.HORIZONTAL, command=self.resetFactor)
        scl_dsize_height.set(self.dsize[1])

        self.var_fx = tk.DoubleVar()
        scl_fx = tk.Scale(self, variable=self.var_fx, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.resetDsize)
        scl_fx.set(self.fx)

        self.var_fy = tk.DoubleVar()
        scl_fy = tk.Scale(self, variable=self.var_fy, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.resetDsize)
        scl_fy.set(self.fy)

        self.var_interpolation = tk.StringVar()
        self.cbx_interpolation = ttk.Combobox(self, textvariable=self.var_interpolation)
        self.cbx_interpolation.config(values=tuple(enumInterpolationFlags.keys()))
        self.cbx_interpolation.current(newindex=tuple(enumInterpolationFlags.values()).index(self.interpolation))
        self.cbx_interpolation.config(state="readonly")

        scl_dsize_width.grid(row=0, column=0)
        scl_dsize_height.grid(row=0, column=1)
        scl_fx.grid(row=1, column=0)
        scl_fy.grid(row=1, column=1)
        self.cbx_interpolation.grid(row=2, column=0, columnspan=2)


    def resetFactor(self, source):
        self.var_fx.set(0)
        self.var_fy.set(0)


    def resetDsize(self, source):
        self.var_dsize_width.set(0)
        self.var_dsize_height.set(0)


    def runProcess(self, src):
        self.getValues()

        dst = None
        try:
            dst = cv2.resize(src, dsize=self.dsize, fx=self.fx, fy=self.fy, interpolation=self.interpolation)
        except:
            pass

        return dst


    def getValues(self):
        self.dsize = (self.var_dsize_width.get(), self.var_dsize_height.get())
        self.fx = self.var_fx.get()
        self.fy = self.var_fy.get()
        self.interpolation = enumInterpolationFlags[self.var_interpolation.get()]
