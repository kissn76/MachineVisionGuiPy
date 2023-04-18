import cv2
import tkinter as tk


class OcvThreshold(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.threshold_value = 0.0
        self.max_value = 255.0
        self.type = cv2.THRESH_BINARY

        self.var_thval = tk.DoubleVar()
        scl_thval = tk.Scale(self, variable=self.var_thval, from_=0, to=255, orient=tk.HORIZONTAL)
        scl_thval.set(self.threshold_value)

        self.var_maxval = tk.DoubleVar()
        scl_maxval = tk.Scale(self, variable=self.var_maxval, from_=0, to=255, orient=tk.HORIZONTAL)
        scl_maxval.set(self.max_value)

        types = [
            (cv2.THRESH_BINARY, "THRESH_BINARY"),
            (cv2.THRESH_BINARY_INV, "THRESH_BINARY_INV"),
            (cv2.THRESH_TRUNC, "THRESH_TRUNC"),
            (cv2.THRESH_TOZERO, "THRESH_TOZERO"),
            (cv2.THRESH_TOZERO_INV, "THRESH_TOZERO_INV"),
            (cv2.THRESH_MASK, "THRESH_MASK"),
            (cv2.THRESH_OTSU, "THRESH_OTSU"),
            (cv2.THRESH_TRIANGLE, "THRESH_TRIANGLE")
        ]
        self.lbx_type = tk.Listbox(self)
        for type in types:
            self.lbx_type.insert(type[0], type[1])

        self.lbx_type.select_set(self.type)

        scl_thval.pack()
        scl_maxval.pack()
        self.lbx_type.pack()

    def printvalues(self):
        self.threshold_value = self.var_thval.get()
        self.max_value = self.var_maxval.get()
        self.type = self.lbx_type.curselection()
        print(self.var_thval.get())
        print(self.var_maxval.get())
        print(self.lbx_type.curselection())

# def main():
#     root = tk.Tk()
#     # root.geometry("700x550")
#     root.title("OpenCV Threshold")
#     ocvThresh = OcvThreshold(root)
#     btn_ok = tk.Button(root, text="Ok", command=ocvThresh.printvalues)
#     ocvThresh.pack()
#     btn_ok.pack()
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()
