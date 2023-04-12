from PIL import Image, ImageTk
import cv2
from numpy import size
from tkinter import LEFT, TOP, X, FLAT, RAISED, N, S, E, W, END
from tkinter import Tk, Frame, Menu, Button, PhotoImage, Label, Listbox, Scrollbar

import numpy as np

root = Tk()
frm_main = Frame(root)
frm_images = Frame(frm_main)
frm_commands = Frame(frm_main)
frm_awailable_commands = Frame(frm_main)
lb_commands = Listbox(frm_commands)
sb_commands = Scrollbar(frm_commands)
lb_awailable_commands = Listbox(frm_awailable_commands)
sb_awailable_commands = Scrollbar(frm_awailable_commands)
lb_commands_lastindex = None


def print_event(event):
    print("Event:", event)


def set_value(event):
    try:
        lb_commands_lastindex = lb_commands.curselection()[0]
    except:
        pass

    print(lb_commands_lastindex)


def insert_value(event):
    print(lb_commands_lastindex)
    lb_commands.insert(END, lb_awailable_commands.curselection()[0])


def main():
    # root.geometry("700x550")
    root.title("Try Tk")

    frm_main.grid(row=0, column=0)

    frm_images.grid(row=0, column=0)

    frm_commands.grid(row=0, column=1, sticky=N + S)
    frm_commands.rowconfigure(0, weight=1)

    frm_awailable_commands.grid(row=0, column=2, sticky=N + S)
    frm_awailable_commands.rowconfigure(0, weight=1)

    img = cv2.imread('/home/nn/Képek/ocv.jpg')
    blue, green, red = cv2.split(img)
    img = cv2.merge((red, green, blue))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    lbl_image_1 = Label(frm_images, image=imgtk)
    lbl_image_1.grid(row=0, column=0)
    # lbl_image_2 = Label(frm_images, image=imgtk)
    # lbl_image_2.grid(row=1, column=0)
    # lbl_image_3 = Label(frm_images, image=imgtk)
    # lbl_image_3.grid(row=2, column=0)

    # used opencv commands
    lb_commands.grid(row=0, column=0, sticky=N + S)
    sb_commands.grid(row=0, column=1, sticky=N + S)

    # for values in range(10):
    #     lb_commands.insert(END, values)

    lb_commands.config(yscrollcommand=sb_commands.set)
    sb_commands.config(command=lb_commands.yview)

    # awailable opencv commands
    lb_awailable_commands.grid(row=0, column=0, sticky=N + S)
    sb_awailable_commands.grid(row=0, column=1, sticky=N + S)

    lb_commands.bind("<<ListboxSelect>>", set_value)
    lb_commands.bind("<Double-1>", lambda e: lb_commands.delete(lb_commands.curselection()[0]))
    lb_awailable_commands.bind("<Double-1>", insert_value)

    for values in range(100):
        lb_awailable_commands.insert(END, values)

    lb_awailable_commands.config(yscrollcommand=sb_awailable_commands.set)
    sb_awailable_commands.config(command=lb_awailable_commands.yview)

    root.mainloop()


if __name__ == '__main__':
    main()
