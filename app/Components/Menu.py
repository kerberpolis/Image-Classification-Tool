import tkinter as tk


class Menu:
    """ Menu widget for the main GUI window """
    def __init__(self, parent, shortcuts, functions):
        """ Initialize the Menu """
        self.parent = parent
        self.shortcuts = shortcuts  # obtain link on keyboard shortcuts
        self.functions = functions  # obtain link on dictionary of functions
        self.menubar = tk.Menu(parent)  # create main menu bar, public for the main GUI

        # Create menu for the image
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.file.add_command(label='Open image',
                              command=self.parent.ask_open_image,
                              accelerator=None)
        self.file.add_command(label='Open image folder',
                              command=self.parent.ask_open_folder,
                              accelerator=None)
        self.file.add_command(label='Save image',
                              command=self.shortcuts[0][2],
                              accelerator=self.shortcuts[0][0])
        self.file.add_command(label='Close image',
                              command=self.shortcuts[1][2],
                              accelerator=self.shortcuts[1][0])
        self.file.add_separator()
        self.file.add_command(label='Exit',
                              command=self.functions['destroy'],
                              accelerator='Alt+F4')
        self.menubar.add_cascade(label='File', menu=self.file)
