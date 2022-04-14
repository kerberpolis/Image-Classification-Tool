import logging
import os
import tkinter as tk
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ImageFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas_w, self.canvas_h = kwargs['width'], kwargs['height']

        self.image, self.imageid, self.im_width, self.im_height = None, None, None, None
        self.image_number = 0
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self, highlightthickness=0,
                                bg='black',
                                width=self.canvas_w, height=self.canvas_h)
        self.canvas.pack()
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

        # set image on canvas
        bbox = (self.canvas.canvasx(0),  # get visible area of the canvas
                self.canvas.canvasy(0),
                self.canvas.canvasx(self.canvas.winfo_width()),
                self.canvas.canvasy(self.canvas.winfo_height()))

        imagetk = ImageTk.PhotoImage(self.image)

        if self.imageid:
            self.canvas.itemconfigure(self.imageid, image=imagetk)
        else:
            self.imageid = self.canvas.create_image((bbox[0], bbox[1]), anchor='nw', image=imagetk)
        self.canvas.lower(self.imageid)  # set image into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def clear_canvas(self):
        pass

    def save_images(self):
        pass

    def remove_classifications(self):
        pass

    def remove_mask(self):
        pass

    def set_mouse_bindings(self):
        pass
