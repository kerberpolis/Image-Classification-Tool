import logging
import tkinter as tk

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ImageFrame(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.root = root
        self.grid_columnconfigure(0, weight=1)  # make canvas expand in width
        self.canvas_w, self.canvas_h = kwargs['width'], kwargs['height']

        # Create canvas and put image on it
        self.canvas = tk.Canvas(self, highlightthickness=0,
                                bg='black',
                                width=self.canvas_w, height=self.canvas_h)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.canvas.update()  # wait till canvas is created

        # Make the canvas expandable
        self.rowconfigure(0, weight=1)

        self.set_mouse_bindings()

    def save_images(self):
        pass

    def remove_classifications(self):
        pass

    def remove_mask(self):
        pass

    def set_mouse_bindings(self):
        pass
