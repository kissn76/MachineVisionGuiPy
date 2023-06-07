import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from time import time, sleep


class MainCanvas(tk.Canvas):
    def __init__(self, master, command_container, bg, can_main_width, can_main_height, can_main_region_width, can_main_region_height):
        super().__init__(master, bg=bg, scrollregion=(0, 0, can_main_region_width, can_main_region_height))

        self.test_counter = 0

        self.preview_command = None
        self.clipboard_io = None

        self.command_container = command_container

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
        self.bind('<Button-1>', self.widget_dnd_select)


    # DRAG & DROP metódusok
    def widget_dnd_select(self, move):
        self.bind('<Motion>', self.widget_dnd_move)
        self.bind('<ButtonRelease-1>', self.widget_dnd_deselect)
        self.addtag_withtag('selected', tk.CURRENT)


    def widget_dnd_move(self, event):
        tags = self.gettags('selected')
        if len(tags) > 0:
            tag = tags[0]
            command_name_tag = tag[0:tag.rfind('.')]
            item_type_tag = tag[tag.rfind('.') + 1:]
            if item_type_tag == "move":
                mouse_x, mouse_y = event.x, event.y
                self.widget_move(command_name_tag, mouse_x, mouse_y)


    def widget_dnd_deselect(self, event):
        self.dtag('selected')    # removes the 'selected' tag
        self.unbind('<Motion>')


    def widget_move(self, command_name, x, y):
        padding = 4
        command_obj = self.command_container.get_object(command_name)
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
            self.coords(f"{command_name}.settings", move_x0, move_y1 + padding)
            settings_x0, settings_y0, settings_x1, settings_y1 = self.bbox(f"{command_name}.settings")
            self.coords(f"{command_name}.delete", settings_x0, settings_y1 + padding)
            delete_x0, delete_y0, delete_x1_, delete_y1 = self.bbox(f"{command_name}.delete")

            command_y0 = move_y0 - padding
            background_x1 = move_x1
            before_input_x0 = move_x1
            for input_key in command_obj.command_model.input.keys():
                command_y0 = move_y1
                self.coords(f"{command_name}.{input_key}", before_input_x0 + padding, move_y0)
                _, _, before_input_x0, _ = self.bbox(f"{command_name}.{input_key}")

                if background_x1 < before_input_x0:
                    background_x1 = before_input_x0

            self.coords(command_name, move_x1 + padding, command_y0 + padding)
            name_x0, _, name_x1, name_y1 = self.bbox(command_name)
            if background_x1 < name_x1:
                background_x1 = name_x1

            background_y1 = delete_y1
            before_output_x0 = move_x1
            for output_name in command_obj.command_model.output.values():
                self.coords(output_name, before_output_x0 + padding, name_y1 + padding)
                _, _, before_output_x0, output_y1 = self.bbox(output_name)

                if background_y1 < output_y1:
                    background_y1 = output_y1
                if background_x1 < before_output_x0:
                    background_x1 = before_output_x0

            self.coords(f"{command_name}.background", move_x0 - padding, move_y0 - padding, background_x1 + padding, background_y1 + padding)

            self.io_widgets_connect(command_name)
    # DRAG & DROP metódusok END


    # connect commands with line
    def io_widgets_connect(self, command_name):
        if not command_name in self.command_container.keys():
            return

        for output_name in self.command_container.get_object(command_name).command_model.output.values():
            output_x0, output_y0, output_x1, output_y1 = self.bbox(output_name)
            children = self.command_container.find_input_keys(output_name)
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

        for input_key, input_name in self.command_container.get_object(command_name).command_model.input.items():
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


    def widget_delete(self, command_name):
        print(f"delete: {command_name}")


    def widget_create(self, command_name, x=100, y=100):
        command_obj = self.command_container.get_object(command_name)
        id_move = self.create_image(x, y, image=self.image_move, anchor="nw")
        self.addtag_withtag(f"{command_obj.command_name}.move", id_move)

        id_setting = self.create_image(x, y, image=self.image_settings, anchor="nw")
        self.addtag_withtag(f"{command_obj.command_name}.settings", id_setting)
        self.tag_bind(id_setting, '<Button-1>', lambda event: self.command_container.setting_widget_show(command_obj.command_name))

        id_delete = self.create_image(x, y, image=self.image_delete, anchor="nw")
        self.addtag_withtag(f"{command_obj.command_name}.delete", id_delete)
        self.tag_bind(id_delete, '<Button-1>', lambda event: self.widget_delete(command_obj.command_name))

        for input_key in command_obj.command_model.input.keys():
            id_input = self.create_image(0, 0, image=self.image_picture, anchor="nw")
            self.addtag_withtag(f"{command_obj.command_name}.{input_key}", id_input)
            self.tag_bind(id_input, '<Double-Button-1>', lambda event: self.paste_input(command_obj.command_name, input_key))
            self.tag_bind(id_input, '<Enter>', lambda event: self.popup_create(event, id_input, f"{command_obj.command_name}.{input_key}"))
            # self.tag_bind(id_input, '<Leave>', self.popup_delete)

        id_command = self.create_text(x, y, text=command_obj.command_name, anchor="nw")
        self.addtag_withtag(command_obj.command_name, id_command)

        for output_name in command_obj.command_model.output.values():
            id_output = self.create_image(0, 0, image=self.image_picture, anchor="nw")
            self.addtag_withtag(output_name, id_output)
            self.tag_bind(id_output, '<Double-Button-1>', lambda event: self.copy_output(event, output_name))
            self.tag_bind(id_output, '<Button-1>', lambda event: self.preview_set(output_name))
            self.tag_bind(id_output, '<Enter>', lambda event: self.popup_create(event, id_output, output_name))
            self.tag_bind(id_output, '<Leave>', self.popup_delete)

        id_background = self.create_rectangle(x, y, x, y, fill='red', outline='red')
        self.addtag_withtag(f"{command_obj.command_name}.background", id_background)
        self.tag_lower(id_background, id_move)

        self.widget_move(command_name, x, y)


    def paste_input(self, command_name, input_key):
        command_obj = self.command_container.get_object(command_name)
        if not bool(self.clipboard_io):
            print("Empty clipboard")
        else:
            if not self.clipboard_io in command_obj.command_model.output.values():
                # vonal törlése a gui-n, ha már volt beállított input
                if bool(command_obj.command_model.input[input_key]):
                    line_name = f"{command_obj.command_model.input[input_key]}-{command_name}.{input_key}"
                    self.delete(self.lines[line_name])
                    self.lines.pop(line_name)

                command_obj.command_model.input[input_key] = self.clipboard_io
                self.io_widgets_connect(command_name)
            else:
                print("Error: nem lehet a saját maga inputja!")


    def copy_output(self, event, text):
        x0, y0, x1, y1 = self.bbox(tk.CURRENT)

        self.delete("clipboard")

        id_background = self.create_rectangle(x0, y0, x1, y1, fill='blue')
        self.addtag_withtag("clipboard", id_background)
        self.tag_lower(id_background, tk.CURRENT)

        self.clipboard_io = text
        print("Clipboard:", self.clipboard_io)


    def preview_set(self, output_name):
        x0, y0, x1, y1 = self.bbox(tk.CURRENT)

        self.delete("preview")

        id_background = self.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline='yellow')
        self.addtag_withtag("preview", id_background)
        self.tag_lower(id_background, tk.CURRENT)


    def popup_create(self, event, id, text):
        self.popup_delete()

        x0, y0, x1, y1 = self.bbox(id)

        id_text = self.create_text(x1 + 6, y0 - 6, text=text, anchor="nw")
        self.addtag_withtag("popup", id_text)
        text_x0, text_y0, text_x1, text_y1 = self.bbox(id_text)

        id_background = self.create_rectangle(text_x0 - 6, text_y0 - 6, text_x1 + 6, text_y1 + 6, fill='yellow', outline='yellow')
        self.addtag_withtag("popup_background", id_background)
        self.tag_lower(id_background, id_text)


    def popup_delete(self, event=None):
        print("Delete", self.test_counter)
        self.test_counter += 1
        # self.delete("popup_background")
        # self.delete("popup")
