import logging
import tkinter as tk

from Components.Main import Main


def setup_logging():
    """Configure logger"""
    # Log application startup
    logging.basicConfig(filename="../image_classification_tool.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    app_logger = logging.getLogger(__name__)
    app_logger.setLevel(logging.INFO)
    app_logger.info("Running Image Classification Tool")


if __name__ == "__main__":
    setup_logging()

    title = 'Image Classification Tool'
    root = tk.Tk(className=title)
    root.title(title)

    screen_width = root.winfo_screenwidth()/3
    screen_height = root.winfo_screenheight()/3

    Main(root, width=screen_width, height=screen_height)
    root.mainloop()
