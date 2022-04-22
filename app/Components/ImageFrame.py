import logging
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from app.MarkingController import MarkingController

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ImageFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas_w, self.canvas_h = kwargs['width'], kwargs['height']
        self.image, self.imageid, self.im_width, self.im_height, self.bbox = None, None, None, None, None
        self.image_number = 0
        self.penwidth = 10
        self.is_drawing = False
        self.old_x = None
        self.old_y = None

        self.marking_controller = MarkingController()

        # Create canvas and put image on it
        self.canvas = tk.Canvas(self, highlightthickness=0,
                                bg='black',
                                width=self.canvas_w, height=self.canvas_h)
        self.canvas.pack()
        # set image on canvas
        self.bbox = (self.canvas.canvasx(0),  # get visible area of the canvas
                self.canvas.canvasy(0),
                self.canvas.canvasx(self.canvas.winfo_width()),
                self.canvas.canvasy(self.canvas.winfo_height()))

        self.set_mouse_bindings()

    def set_canvas_image(self, filepath):
        # set image
        try:
            image = Image.open(filepath)
            self.image = image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
        except Exception:
            msg = f'Cannot open selected file {filepath}. Not on image.'
            logging.info(msg)

        self.im_width, self.im_height = self.image.size

        imagetk = ImageTk.PhotoImage(self.image)

        if self.imageid:
            self.canvas.itemconfigure(self.imageid, image=imagetk)
        else:
            self.imageid = self.canvas.create_image((self.bbox[0], self.bbox[1]), anchor='nw', image=imagetk)
        self.canvas.lower(self.imageid)  # set image into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def clear_canvas(self):
        self.canvas.delete('mask')
        self.marking_controller.delete_all_markings()
        if not self.is_drawing:
            self.canvas.delete('bg_mask')

    def save_images(self):
        pass

    def save_mask(self):
        im_path = self.parent.images[self.image_number-1]
        im_filename = im_path.split('.')[0].split('/')[-1]
        # prefix_path = '/'.join(im_path.split(".")[0].split("/")[:-1])
        # mask_filename = f'{prefix_path}/{im_filename}_mask.png'

        new_path = 'new_images/'
        new_image_filename = f'{new_path}{im_filename}.png'
        new_mask_filename = f'{new_path}{im_filename.split(".")[0]}_mask.png'

        markings = self.marking_controller.get_markings()
        im = Image.new('RGBA', size=(self.im_width, self.im_height))
        draw = ImageDraw.Draw(im)
        for marking_id, marking in markings.items():
            draw.line(marking['coordinates'], fill='white')

        im.save(new_mask_filename)  # save image mask to folder
        self.image.save(new_image_filename)  # save image to folder

    def remove_classifications(self):
        pass

    def remove_mask(self):
        pass

    def set_mouse_bindings(self):
        pass

    def move_mouse(self, event):
        if self.image:
            if hasattr(self.canvas, '_cursor_id'):
                self.canvas.delete(self.canvas._cursor_id)
            x, y = event.x, event.y

            x_max = x + self.penwidth/2
            x_min = x - self.penwidth/2
            y_max = y + self.penwidth/2
            y_min = y - self.penwidth/2

            self.canvas._cursor_id = self.canvas.create_oval(x_min, y_max, x_max, y_min, fill='black')

    def remove_cursor(self, event):
        if hasattr(self.canvas, '_cursor_id'):
            self.canvas.delete(self.canvas._cursor_id)

    def start_drawing(self):
        if self.image:
            self.is_drawing = True

            self.create_transparent_window(0, 0, int(self.canvas_w), int(self.canvas_h),
                                           fill='#d3d3d3', alpha=0.4)

            self.canvas.bind("<B1-Motion>", lambda e: self.paint(e))
            self.canvas.bind("<ButtonRelease-1>", self.reset)
            self.canvas.bind("<ButtonPress-1>", lambda e: self.paint(e))
            self.canvas.bind("<Motion>", self.move_mouse)
            self.canvas.bind("<Leave>", self.remove_cursor)

    def stop_drawing(self):
        if self.image:
            self.is_drawing = False

            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Leave>")

            self.clear_canvas()

    def create_transparent_window(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = tuple(int(item % 256) for item in self.parent.winfo_rgb(fill)) + (alpha,)
            im = Image.new(mode='RGBA', size=(x2 - x1, y2 - y1), color=fill)
            self.canvas._im_tk = ImageTk.PhotoImage(im)
            self.canvas._draw_rect = self.canvas.create_image(x1, y1, image=self.canvas._im_tk, anchor='nw', tags='bg_mask')
        self.canvas._draw_rect = self.canvas.create_rectangle(x1, y1, x2, y2, tags='bg_mask', **kwargs)

    def RBGAImage(self, path):
        return Image.open(path).convert("RGBA")

    def paint(self, event):
        x, y = event.x, event.y

        if event.type.name == 'Motion':
            if hasattr(self.canvas, '_cursor_id'):
                self.canvas.delete(self.canvas._cursor_id)

        marking_id = None
        coordinates = None
        if self.old_x and self.old_y:
            marking_id = self.canvas.create_line(self.old_x, self.old_y, x, y, width=self.penwidth,
                                                 capstyle=tk.ROUND, smooth=True, tags='mask', stipple='gray50')
            coordinates = [self.old_x, self.old_y, x, y]
        else:
            marking_id = self.canvas.create_line(x, y, x, y, width=self.penwidth,
                                                 capstyle=tk.ROUND, smooth=True, tags='mask', stipple='gray50')
            coordinates = [x, y, x, y]

        if marking_id and coordinates:
            marking = {
                'marking_id': marking_id,
                'coordinates': coordinates,
                'width': self.penwidth,
                'classification': None
            }
            self.marking_controller.add_marking(marking)

        self.old_x = x
        self.old_y = y

    def reset(self, e):
        self.old_x = None
        self.old_y = None

    def change_pen_width(self, event):
        self.penwidth = int(event)

