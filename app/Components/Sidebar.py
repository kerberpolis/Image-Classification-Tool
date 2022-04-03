import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.root = root

        self.clear_button = tk.Button(self, font=('calibre', 10, 'normal'),
                                      text="Clear", command=None)
        self.clear_button.grid(row=0, column=0)
