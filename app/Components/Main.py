import logging
import os
import tkinter as tk
from Components.ImageFrame import ImageFrame
from Components.Menu import Menu
from Components.SavingWidget import SavingWidget
from Components.Sidebar import Sidebar
from tkinter import filedialog, messagebox
import glob
from PIL import Image


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.width, self.height = self['width'], self['height']
        self.default_title = 'Image Classification Tool'
        self.parent.title(self.default_title)
        self.parent.geometry(f'{self.width}x{self.height}')  # size of the main window
        self.pack()
        self.parent.minsize(1000, 600)
        # self.parent.rowconfigure(0, weight=1)  # make the application widget expandable
        # self.parent.columnconfigure(0, weight=1)
        self.previous_state = None

        self.keycode = {}  # init key codes
        if os.name == 'nt':  # Windows OS
            self.keycode = {
                's': 83,
                'w': 87,

            }
        elif os.name == 'posix':  # Linux OS
            self.keycode = {
                's': 39,
                'w': 25,
            }

        self.shortcuts = [
            ['Ctrl+S', self.keycode['s'], self.save_image],  # 1 save polygons of the image
            ['Ctrl+W', self.keycode['w'], self.close_image],  # 1 save polygons of the image
        ]
        self.parent.bind('<Key>', lambda event: self.master.after_idle(self.keystroke, event))
        self.images = []

        self.create_menu()
        self.im_frame = ImageFrame(self, width=self.width*0.9, height=self.height*0.9,
                                   bd=1)
        self.sidebar = Sidebar(self, width=self.width * 0.2, height=200, bd=1)

        self.im_frame.pack(side='top', fill='both')
        self.sidebar.pack(side='bottom', fill='x')

    def keystroke(self, event):
        """ Language independent handle events from the keyboard
            Link1: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
            Link2: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html """
        if event.state - self.previous_state == 4:  # check if <Control> key is pressed
            for shortcut in self.shortcuts:
                if event.keycode == shortcut[1]:
                    shortcut[2]()
        else:  # remember previous state of the event
            self.previous_state = event.state

    def create_menu(self):
        """ Menu widget for GUI created here """
        self.functions = {  # dictionary of functions for menu widget
            "destroy": self.destroy,
        }
        self.menu = Menu(self, self.shortcuts, self.functions)
        self.parent.configure(menu=self.menu.menubar)

    def initialise_image(self):
        if self.images:
            self.im_frame.image_number = 0
            self.sidebar.next_image()
        else:
            logging.info('Error loading images')
        return

    def ask_open_folder(self, directory=None):
        if not directory:
            directory = filedialog.askdirectory(initialdir="C:/")

        if directory is None: return
        self.images = []

        filepaths = [path for list in [glob.glob(f'{directory}/*.%s' % ext) for ext in ["jpg", "jpeg", "png"]] for path in list]
        for filepath in filepaths:
            try:
                Image.open(filepath)
                self.images.append(filepath)
            except Exception:
                msg = f'Cannot open selected file {filepath}. Not on image.'
                logging.info(msg)

        self.initialise_image()

    def ask_open_image(self):
        """ Open image """
        image_file = filedialog.askopenfile(initialdir="C:/",
                                            filetypes=(
                                                ('Image files', '.png .jpg .jpeg'),
                                                ('All Files', '.*'))
                                            )
        if image_file is None: return
        self.images = []

        self.images.append(image_file.name)
        self.initialise_image()

    def open_image(self, filename):
        """ Open image """
        try:
            self.parent.title(self.default_title + ': {}'.format(filename))  # change window title
            self.im_frame.set_canvas_image(filename)
            self.im_frame.set_canvas_markings()
        except Exception:
            msg = f'Cannot open selected file {filename}'
            logging.info(msg)
            messagebox.showwarning(title="Error", message=msg)

    def close_image(self):
        """ Close image """
        self.im_frame.clear_canvas()
        self.parent.title(self.default_title)  # set default window title
        self.images = []

    def save_image(self):
        im_path = self.images[self.im_frame.image_number - 1]
        im_filename = im_path.split('.')[0].split('/')[-1]

        new_path = 'new_images/'
        image_filepath = f'{new_path}{im_filename}.png'
        mask_filepath = f'{new_path}{im_filename.split(".")[0]}_mask.png'

        self.im_frame.image.save(image_filepath)
        self.im_frame.save_mask(mask_filepath)

    def destroy(self):
        """ Destroy the main frame object and release all resources """
        logging.info('Close GUI')
        self.quit()
