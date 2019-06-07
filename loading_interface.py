from tkinter import messagebox
import sys

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

import loading_interface_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Login_Interface (root)
    loading_interface_support.init(root, top)
    root.mainloop()

w = None
def create_Login_Interface(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Login_Interface (w)
    loading_interface_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Login_Interface():
    global w
    w.destroy()
    w = None

class Login_Interface:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family {Open Sans} -size 15 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("650x451+1983+153")
        top.title("X-MAIL")
        top.configure(background="#212121")
        top.configure(highlightcolor="black")

        self.messagebox=messagebox

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=-0.015, rely=0.0, relheight=1.009, relwidth=1.131)


        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="1")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#212121")
        self.Frame1.configure(highlightbackground="#212121")
        self.Frame1.configure(width=735)

        self.Loadbar = ttk.Progressbar(self.Frame1)
        self.Loadbar.place(relx=0.313, rely=0.374, relwidth=0.286, relheight=0.0
                , height=19)
        self.Loadbar.configure(length="210")
        self.Loadbar.configure(mode='indeterminate')
        self.Loadbar.start(10)
        

        self.TLabel1 = ttk.Label(self.Frame1)
        self.TLabel1.place(relx=0.136, rely=0.33, height=61, width=90)
        self.TLabel1.configure(background="#212121")
        self.TLabel1.configure(foreground="#f4f4f4")
        self.TLabel1.configure(font=font11)
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(text='''Loading''')
        self.TLabel1.configure(width=90)

        self.Message1 = tk.Message(self.Frame1)
        self.Message1.place(relx=0.286, rely=0.044, relheight=0.22
                , relwidth=0.344)
        self.Message1.configure(background="#212121")
        self.Message1.configure(font=font11)
        self.Message1.configure(foreground="#eaeaea")
        self.Message1.configure(text='''Please wait ...''')
        self.Message1.configure(width=253)

        self.CancelB = ttk.Button(self.Frame1)
        self.CancelB.place(relx=0.367, rely=0.637, height=38, width=113)
        self.CancelB.configure(takefocus="")
        self.CancelB.configure(text='''Cancel''')
        self.CancelB.configure(width=113)
        self.CancelB.configure(command=loading_interface_support.CancelAct)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

if __name__ == '__main__':
    vp_start_gui()
