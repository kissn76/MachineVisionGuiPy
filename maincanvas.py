import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mainwindow as mw


class MainCanvas(tk.Canvas):
    def __init__(self, master, bg, can_main_width, can_main_height, can_main_region_width, can_main_region_height):
        super().__init__(master, bg=bg, scrollregion=(0, 0, can_main_region_width, can_main_region_height))

        self.lines = {}

        hbar=ttk.Scrollbar(master, orient=tk.HORIZONTAL)
        hbar.grid(row=1, column=0, sticky="e, w")
        hbar.config(command=self.xview)
        vbar=ttk.Scrollbar(master, orient=tk.VERTICAL)
        vbar.grid(row=0, column=1, sticky="n, s")
        vbar.config(command=self.yview)
        self.config(width=can_main_width, height=can_main_height)
        self.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.can_main_region_width = can_main_region_width
        self.can_main_region_height = can_main_region_height
        self.can_main_width = can_main_width
        self.can_main_height = can_main_height

        self.icon_size = 16
        self.image_move = ImageTk.PhotoImage(Image.open(f"./resources/icons/move_{self.icon_size}.png"))
        self.image_close = ImageTk.PhotoImage(Image.open(f"./resources/icons/close_{self.icon_size}.png"))
        self.image_info = ImageTk.PhotoImage(Image.open(f"./resources/icons/info_{self.icon_size}.png"))
        self.image_settings = ImageTk.PhotoImage(Image.open(f"./resources/icons/settings_{self.icon_size}.png"))
        self.image_delete = ImageTk.PhotoImage(Image.open(f"./resources/icons/delete_{self.icon_size}.png"))
        self.image_picture = ImageTk.PhotoImage(Image.open(f"./resources/icons/picture_{self.icon_size}.png"))
        self.bind('<Button-1>', self.dnd_select_object)


    # DRAG & DROP metódusok
    def dnd_select_object(self, event):
        self.bind('<Motion>', self.dnd_move_object)
        self.bind('<ButtonRelease-1>', self.dnd_deselect_object)

        x, y = event.x, event.y
        x = self.canvasx(x)
        y = self.canvasy(y)
        self.addtag_withtag('selected', tk.CURRENT)


    def dnd_move_object(self, event):
        tags = self.gettags('selected')
        if len(tags) > 0:
            tag = tags[0]
            command_name_tag = tag[0:tag.rfind('.')]
            item_type_tag = tag[tag.rfind('.') + 1:]
            if item_type_tag == "move":
                mouse_x, mouse_y = event.x, event.y
                self.display_move(command_name_tag, mouse_x, mouse_y)


    def dnd_deselect_object(self, event):
        self.dtag('selected')    # removes the 'selected' tag
        self.unbind('<Motion>')
    # DRAG & DROP metódusok END


    # connect commands with line
    def connect_commands(self, command_name):
        if not command_name in mw.used_command_list.keys():
            return

        for output_name in mw.used_command_list[command_name].command_model.output.values():
            output_x0, output_y0, output_x1, output_y1 = self.bbox(output_name)
            children = mw.find_child_commands(output_name)
            for child in children:
                line_name = f"{output_name}-{child}"
                child_x0, child_y0, child_x1, child_y1 = self.bbox(child)
                x0 = int(output_x0 + (output_x1 - output_x0) / 2)
                x1 = int(child_x0 + (child_x1 - child_x0) / 2)
                if line_name in self.lines.keys():
                    self.coords(self.lines[line_name], x0, output_y1, x1, child_y0)
                else:
                    line = self.create_line(x0, output_y1, x1, child_y0, fill="green", width=2)
                    self.lines.update({line_name: line})

        for input_key, input_name in mw.used_command_list[command_name].command_model.input.items():
            if bool(input_name):
                line_name = f"{input_name}-{command_name}.{input_key}"
                parent_x0, parent_y0, parent_x1, parent_y1 = self.bbox(input_name)
                input_x0, input_y0, input_x1, input_y1 = self.bbox(f"{command_name}.{input_key}")
                x0 = int(input_x0 + (input_x1 - input_x0) / 2)
                x1 = int(parent_x0 + (parent_x1 - parent_x0) / 2)
                if line_name in self.lines.keys():
                    self.coords(self.lines[line_name], x0, input_y0, x1, parent_y1)
                else:
                    line = self.create_line(x0, input_y0, x1, parent_y1, fill="green", width=2)
                    self.lines.update({line_name: line})


    def used_command_delete(self, command_name):
        print(f"delete: {command_name}")


    def display_create(self, command_name, x=100, y=100):
        command_obj = mw.used_command_list[command_name]
        id_move = self.create_image(x, y, image=self.image_move, anchor="nw")
        self.addtag_withtag(f"{command_obj.command_name}.move", id_move)

        id_setting = self.create_image(x, y, image=self.image_settings, anchor="nw")
        self.addtag_withtag(f"{command_obj.command_name}.settings", id_setting)
        self.tag_bind(id_setting, '<Button-1>', lambda event: mw.setting_widget_show(command_obj.command_name))

        id_delete = self.create_image(x, y, image=self.image_delete, anchor="nw")
        self.addtag_withtag(f"{command_obj.command_name}.delete", id_delete)
        self.tag_bind(id_delete, '<Button-1>', lambda event: self.used_command_delete(command_obj.command_name))

        frm_command = command_obj.frm_display_main
        id_frm = self.create_window(x, y, window=frm_command, anchor="nw")
        self.addtag_withtag(command_obj.command_name, id_frm)    # a canvas elem tag-ként megkapja a command_name-et, hogy egyedileg meghívható legyen később

        frm_command.update()

        id_background = self.create_rectangle(x, y, x, y, fill='red', outline='red')
        self.addtag_withtag(f"{command_obj.command_name}.background", id_background)
        self.tag_lower(id_background, id_move)

        for input_key, input_name in command_obj.command_model.input.items():
            id_input = self.create_image(0, 0, image=self.image_picture, anchor="nw")
            self.addtag_withtag(f"{command_obj.command_name}.{input_key}", id_input)
            self.tag_bind(id_input, '<Double-Button-1>', lambda event: self.paste_input(command_obj.command_name, input_key))
            self.tag_bind(id_input, '<Enter>', lambda event: print(self.gettags(f"{command_obj.command_name}.{input_key}")))

        for output_key, output_name in command_obj.command_model.output.items():
            id_output = self.create_image(0, 0, image=self.image_picture, anchor="nw")
            self.addtag_withtag(output_name, id_output)
            self.tag_bind(id_output, '<Double-Button-1>', lambda event: mw.copy_output(output_name))
            self.tag_bind(id_output, '<Button-1>', lambda event: mw.preview_set(output_name))
            self.tag_bind(id_output, '<Enter>', lambda event: print(self.gettags(output_name)))

        self.display_move(command_name, x, y)


    def paste_input(self, command_name, input_key):
        command_obj = mw.used_command_list[command_name]
        if not bool(mw.clipboard_io):
            print("Empty clipboard")
        else:
            if not mw.clipboard_io in command_obj.command_model.output.values():
                # vonal törlése a gui-n, ha már volt beállított input
                if bool(command_obj.command_model.input[input_key]):
                    line_name = f"{command_obj.command_model.input[input_key]}-{command_name}.{input_key}"
                    self.delete(self.lines[line_name])
                    self.lines.pop(line_name)

                command_obj.command_model.input[input_key] = mw.clipboard_io
                self.connect_commands(command_name)
            else:
                print("Error: nem lehet a saját maga inputja!")


    def display_move(self, command_name, x, y):
        command_obj = mw.used_command_list[command_name]
        canvas_x = self.canvasx(x)
        canvas_y = self.canvasy(y)
        if x > self.can_main_width:
            self.xview_scroll(1, 'units')
        if x < 1:
            self.xview_scroll(-1, 'units')
        if y > self.can_main_height:
            self.yview_scroll(1, 'units')
        if y < 1:
            self.yview_scroll(-1, 'units')
        if canvas_x < int(self.icon_size / 2):
            canvas_x = int(self.icon_size / 2)
        if canvas_x > self.can_main_region_width:
            canvas_x = self.can_main_region_width - int(self.icon_size / 2)
        if canvas_y < int(self.icon_size / 2):
            canvas_y = int(self.icon_size / 2)
        if canvas_y > self.can_main_region_height:
            canvas_y = self.can_main_region_height - int(self.icon_size / 2)
        self.coords(f"{command_name}.move", canvas_x - int(self.icon_size / 2), canvas_y - int(self.icon_size / 2))

        move_box = self.bbox(f"{command_name}.move")
        if bool(move_box):
            move_x0, move_y0, move_x1, move_y1 = move_box
            self.coords(command_name, move_x1, move_y0)
            frm_x0, frm_y0, frm_x1, frm_y1 = self.bbox(command_name)
            # frm_command = mw.used_command_list[command_name].frm_display_main
            # frm_width = frm_command.winfo_reqwidth()
            # frm_height = frm_command.winfo_reqheight()
            self.coords(f"{command_name}.settings", move_x0, move_y1)
            self.coords(f"{command_name}.delete", move_x0, move_y1 + self.icon_size)
            delete_x0, delete_y0, delete_x1, delete_y1 = self.bbox(f"{command_name}.delete")

            before_input_x0 = frm_x0
            for input_key, input_name in command_obj.command_model.input.items():
                self.coords(f"{command_obj.command_name}.{input_key}", before_input_x0, frm_y0 - self.icon_size)
                _, _, before_input_x0, _ = self.bbox(f"{command_obj.command_name}.{input_key}")

            background_y1 = delete_y1
            before_output_x0 = frm_x0
            for output_key, output_name in command_obj.command_model.output.items():
                self.coords(output_name, before_output_x0, frm_y1)
                output_x0, output_y0, before_output_x0, output_y1 = self.bbox(output_name)

                if background_y1 < output_y1:
                    background_y1 = output_y1

            self.coords(f"{command_name}.background", move_x0, move_y0, frm_x1, background_y1)

            self.connect_commands(command_name)