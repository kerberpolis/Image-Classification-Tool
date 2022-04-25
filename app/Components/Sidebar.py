import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.next_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                     text="Next", command=self.next_image)
        self.next_button.grid(row=0, column=1)

        self.prev_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                     text="Previous", command=self.prev_image)
        self.prev_button.grid(row=0, column=2)

        self.first_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                      text="First", command=self.go_to_first)
        self.first_button.grid(row=0, column=0)

        self.last_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                     text="Last", command=self.go_to_last)
        self.last_button.grid(row=0, column=4)

        self.clear_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                      text="Clear", command=self.parent.im_frame.reset_mask)
        self.clear_button.grid(row=1, column=0)

        self.draw_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                     text="Draw", command=self.start_drawing)
        self.draw_button.grid(row=1, column=1)

        self.save_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                     text="Save", command=self.parent.save_image)
        self.save_button.grid(row=1, column=2)

        self.pen_width_label = tk.Label(self, text='Pen Width: ', font=('', 15)).grid(row=2, column=0)
        self.slider = tk.Scale(self, from_=5, to=100, command=self.parent.im_frame.change_pen_width,
                               orient=tk.HORIZONTAL)
        self.slider.set(5)
        self.slider.grid(row=2, column=1, ipadx=30)

    def next_image(self):
        if not self.parent.images:
            self.parent.ask_open_folder()
            return
        else:
            if self.parent.im_frame.image_number < len(self.parent.images):
                self.parent.im_frame.image_number += 1
                image_path = self.parent.images[self.parent.im_frame.image_number-1]
                self.parent.open_image(image_path)

    def prev_image(self):
        if not self.parent.images:
            self.parent.ask_open_folder()
            return
        else:
            image_path = None
            if self.parent.im_frame.image_number > 1:
                self.parent.im_frame.image_number -= 1
                image_path = self.parent.images[self.parent.im_frame.image_number-1]
            elif self.parent.im_frame.image_number <= 0:
                image_path = self.parent.images[0]

            if image_path:
                self.parent.open_image(image_path)

    def go_to_first(self):
        if not self.parent.images:
            self.parent.ask_open_folder()
            return
        else:
            self.parent.im_frame.image_number = 1
            image_path = self.parent.images[0]
            self.parent.open_image(image_path)

    def go_to_last(self):
        if not self.parent.images:
            self.parent.ask_open_folder()
            return
        else:
            self.parent.im_frame.image_number = len(self.parent.images)
            image_path = self.parent.images[-1]
            self.parent.open_image(image_path)

    def start_drawing(self):
        self.draw_button.configure(text="Stop Drawing", command=self.stop_drawing)
        self.parent.im_frame.start_drawing()

    def stop_drawing(self):
        self.draw_button.configure(text="Draw", command=self.start_drawing)
        self.parent.im_frame.stop_drawing()
