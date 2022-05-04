import logging
import numpy
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
        self.is_drawing, self.is_erasing = False, False
        self.old_x, self.old_y = None, None

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
        self.clear_canvas()

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

    def set_canvas_markings(self):
        if self.image and self.is_drawing:

            try:
                markings = self.marking_controller.get_image_markings(self.image_number)
            except KeyError:
                markings = []
                pass

            for marking in markings:
                x1, y1, x2, y2 = marking['coordinates']
                self.canvas.create_line(x1, y1, x2, y2, width=marking['width'],
                                        capstyle=tk.ROUND, smooth=True, tags='mask', stipple='gray50')

    def reset_mask(self):
        self.clear_canvas()
        self.marking_controller.delete_image_markings(self.image_number)

    def clear_canvas(self):
        self.canvas.delete('mask')
        if not self.is_drawing:
            self.canvas.delete('bg_mask')

    def save_images(self):
        pass

    @staticmethod
    def bresenhams(coordinates):
        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end

        >>> points1 = get_line((0, 0), (3, 4))
        >>> points2 = get_line((3, 4), (0, 0))
        >>> assert(set(points1) == set(points2))
        >>> print points1
        [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
        >>> print points2
        [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        """
        # Setup initial conditions

        x1, y1, x2, y2 = coordinates
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

    def save_mask(self, filename):
        im = Image.new('RGB', size=(self.im_width, self.im_height))
        draw = ImageDraw.Draw(im)
        image_markings = self.marking_controller.get_image_markings(self.image_number)

        for marking in image_markings:
            points = self.bresenhams(marking['coordinates'])

            for point in points:
                x, y = point
                radius = marking['width']/2
                x_min = x - radius
                x_max = x + radius
                y_min = y - radius
                y_max = y + radius

                draw.ellipse([x_min, y_min, x_max, y_max], fill='white')

        im.save(filename)  # save image mask to folder

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
            self.stop_removing()
            self.is_drawing = True

            self.create_transparent_window(0, 0, int(self.canvas_w), int(self.canvas_h),
                                           fill='#d3d3d3', alpha=0.4)

            self.canvas.bind("<B1-Motion>", lambda e: self.paint(e))
            self.canvas.bind("<ButtonRelease-1>", self.reset)
            self.canvas.bind("<ButtonPress-1>", lambda e: self.paint(e))
            self.canvas.bind("<Motion>", self.move_mouse)
            self.canvas.bind("<Leave>", self.remove_cursor)

            self.set_canvas_markings()

    def stop_drawing(self):
        if self.image:
            self.is_drawing = False

            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Leave>")

            self.clear_canvas()

    def start_removing(self):
        if self.image:
            self.is_erasing = True

            self.canvas.bind("<B1-Motion>", lambda e: self.erase(e))
            self.canvas.bind("<ButtonPress-1>", lambda e: self.erase(e))

    def stop_removing(self):
        if self.image:
            self.is_erasing = False

    def create_transparent_window(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = tuple(int(item % 256) for item in self.parent.winfo_rgb(fill)) + (alpha,)
            im = Image.new(mode='RGBA', size=(x2 - x1, y2 - y1), color=fill)
            self.canvas._im_tk = ImageTk.PhotoImage(im)
            self.canvas._draw_rect = self.canvas.create_image(x1, y1, image=self.canvas._im_tk,
                                                              anchor='nw', tags='bg_mask')
        self.canvas._draw_rect = self.canvas.create_rectangle(x1, y1, x2, y2, tags='bg_mask', **kwargs)

    @staticmethod
    def RBGAImage(path):
        return Image.open(path).convert("RGBA")

    def erase(self, event):
        x, y = event.x, event.y
        
        markings = self.marking_controller.get_image_markings(self.image_number)
        for marking in markings:
            cx1, cy1, cx2, cy2 = marking['coordinates']
            marking_id = marking['marking_id']
            if cx1 < x < cx2 and cy1 < y < cy2:
                self.canvas.delete(marking_id)
                self.marking_controller.remove_marking_by_id(marking_id)

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
                'image': self.image_number,
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

    def undo(self):
        current_markings = self.marking_controller.get_image_markings(self.image_number)
        if current_markings:
            last_marking = current_markings.pop(-1)
            self.canvas.delete(last_marking['marking_id'])
            self.canvas.update()
