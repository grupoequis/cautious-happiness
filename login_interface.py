
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

import login_interface_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Login_Interface (root)
    login_interface_support.init(root, top)
    root.mainloop()

w = None
def create_Login_Interface(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Login_Interface (w)
    login_interface_support.init(w, top, *args, **kwargs)
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

        top.geometry("368x258+300+131")
        top.title("X-MAIL")
        top.configure(highlightcolor="black")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.027, rely=0.039, relheight=0.911
                , relwidth=0.938)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(width=345)

        self.Entry1 = tk.Entry(self.Frame1)
        self.Entry1.place(relx=0.319, rely=0.426,height=20, relwidth=0.423)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")

        self.Entry2 = tk.Entry(self.Frame1)
        self.Entry2.place(relx=0.319, rely=0.638,height=20, relwidth=0.423)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="#c4c4c4")
        self.Entry2.configure(show="*")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.087, rely=0.426, height=18, width=65)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Username''')

        self.Label2 = tk.Label(self.Frame1)
        self.Label2.place(relx=0.087, rely=0.638, height=18, width=60)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Password''')

        self.Message1 = tk.Message(self.Frame1)
        self.Message1.place(relx=0.087, rely=0.128, relheight=0.17
                , relwidth=0.82)
        self.Message1.configure(text='''Welcome to X-MAIL''')
        self.Message1.configure(width=283)

        self.Login = tk.Button(self.Frame1)
        self.Login.place(relx=0.406, rely=0.809, height=28, width=61)
        self.Login.configure(activebackground="#f9f9f9")
        self.Login.configure(command=login_interface_support.LogIn)
        self.Login.configure(state='active')
        self.Login.configure(text='''Login''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

if __name__ == '__main__':
    vp_start_gui()





