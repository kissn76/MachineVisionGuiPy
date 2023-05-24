# pip install tkinterweb
from tkinterweb import HtmlFrame
import tkinter as tk

root = tk.Tk() #create the tkinter window
frame = HtmlFrame(root) #create HTML browser

frame.load_website("https://docs.opencv.org/4.7.0/d8/d6a/group__imgcodecs__flags.html")
frame.pack(fill="both", expand=True)
root.mainloop()