
import sys
import configparser
import os

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def LogIn():
    username=w.Entry1.get()
    password=w.Entry2.get()
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("config.txt"))
    config['account']['username']=username
    config['account']['password']=password
    with open("config.txt", 'w') as configfile:    # save
        config.write(configfile)
    sys.stdout.flush()
    exit()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import login_interface
    login_interface.vp_start_gui()





