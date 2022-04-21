import logging
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

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
        self.old_x = None
        self.old_y = None
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

    def save_images(self):
        pass

    def remove_classifications(self):
        pass

    def remove_mask(self):
        pass

    def set_mouse_bindings(self):
        self.canvas.bind("<Motion>", self.move_mouse)
        self.canvas.bind("<Leave>", self.remove_cursor)

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

    def paint_img(self, event):
        x, y = event.x, event.y
        # self.draw_im.ellipse((x-5, y-5, x+5, y+5), fill='black')
        # self.canvas._im_tk = ImageTk.PhotoImage(self.im)
        # self.canvas.itemconfigure(self.canvas._im_draw_id, image=self.canvas._im_tk)

    def show_drawing_image(self):
        # self.im = Image.new("RGBA", (self.im_width, self.im_height))
        # self.draw_im = ImageDraw.Draw(self.im)
        #
        # self.canvas._im_tk = ImageTk.PhotoImage(self.im)
        #
        # self.canvas._im_draw_id = self.canvas.create_image((self.bbox[0], self.bbox[1]),
        #                                                    image=self.canvas._im_tk,
        #                                                    anchor='nw')
        self.canvas.bind("<B1-Motion>", lambda e: self.paint(e))
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<ButtonPress-1>", lambda e: self.paint(e))

    def RBGAImage(self, path):
        return Image.open(path).convert("RGBA")

    def paint(self, e):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth,
                                    fill='black', capstyle=tk.ROUND, smooth=True, tags='mask')
        else:
            x_max = e.x + self.penwidth / 2
            x_min = e.x - self.penwidth / 2
            y_max = e.y + self.penwidth / 2
            y_min = e.y - self.penwidth / 2
            self.canvas.create_oval(x_min, y_max, x_max, y_min, fill='black',  tags='mask')

        self.old_x = e.x
        self.old_y = e.y

    def reset(self, e):
        self.old_x = None
        self.old_y = None

    def change_pen_width(self, event):
        self.penwidth = int(event)

