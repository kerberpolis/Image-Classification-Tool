import logging
import os
import tkinter as tk
from Components.ImageFrame import ImageFrame
from Components.Menu import Menu
from Components.SavingWidget import SavingWidget
from Components.Sidebar import Sidebar
from tkinter import filedialog


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.width, self.height = self['width'], self['height']
        self.default_title = 'Image Classification Tool'
        self.parent.title(self.default_title)
        self.parent.geometry(f'{self.width}x{self.height}')  # size of the main window
        self.parent.minsize(1200, 800)
        self.parent.rowconfigure(0, weight=1)  # make the application widget expandable
        self.parent.columnconfigure(0, weight=1)
        self.previous_state = None

        self.keycode = {}  # init key codes
        if os.name == 'nt':  # Windows OS
            self.keycode = {
                'o': 79,
                'w': 87,
                's': 83,
            }
        elif os.name == 'posix':  # Linux OS
            self.keycode = {
                'o': 32,
                'w': 25,
                's': 39,
            }
        self.shortcuts = [['Ctrl+O', self.keycode['o'], self.open_image],  # 0 open image
                          ['Ctrl+W', self.keycode['w'], self.close_image],  # 1 close image
                          ['Ctrl+S', self.keycode['s'], self.save_image],  # 2 save polygons of the image
                          ]
        self.parent.bind('<Key>', lambda event: self.master.after_idle(self.keystroke, event))

        self.create_menu()

        self.parent.bind("<Configure>", self.resize)

    def resize(self, event):
        if self.width != event.width or self.height != event.height:
            # print(f'{event.widget}=: {event.height}=, {event.width}=\n')
            self.width, self.height = event.width, event.height

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

    def open_image(self):
        """ Open image """
        image_file = filedialog.askopenfile(initialdir="C:/",
                                            filetypes=(
                                              ('All Files', '.*'), ('All Files', '.*'),
                                              ('image files', ('.png', '.jpg', 'jpeg', '.tiff', '.tif')))
                                            )
        if image_file is None: return
        path = image_file.name

        # open image
        try:
            image = Image.open(path)
            self.parent.title(self.default_title + ': {}'.format(path))  # change window title
        except Exception:
            msg = f'Cannot open selected file {path}'
            logging.info(msg)
            tk.messagebox.showwarning(title="Error",
                                      message=msg)

    def close_image(self):
        pass

    def save_image(self):
        pass

    def destroy(self):
        """ Destroy the main frame object and release all resources """
        logging.info('Close GUI')
        self.quit()
