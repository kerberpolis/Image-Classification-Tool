import tkinter as tk
from tkinter.ttk import Progressbar


class SavingWidget(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.width, self.height = kwargs['width'], kwargs['height']

        self.win = tk.Toplevel(self, width=self.width, height=self.height)
        self.win.wm_transient(self.parent)
        self.win.wm_title("Saving")

        self.label = tk.Label(self.win, text="Saving...please wait...")
        self.label.grid(row=0, column=0)

        self.cancel_button = tk.Button(self.win, text='Cancel', command=self.win.destroy)
        self.cancel_button.grid(row=2, column=0, padx=10, pady=10)

        self.pb = Progressbar(self.win, orient='horizontal', mode='indeterminate', length=480)
        self.pb.grid(row=1, column=0)

        self.pb.start()


