import tkinter as tk
from tkinter import *
import sys
import os
import re
import time
import threading
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox

from src.logparser import *


class Win:
    def __init__(self):
        self.win = tk.Tk()
        self.stlable = tk.scrolledtext.ScrolledText(self.win, bg="grey", width=98, height=20 )
        self.fin = None
        self.win_checkbox = None
        self.list_checkboxes = None
        self.filepath=""
        self.b64str = StringVar()
        self.setupWindow()

    def loop(self):
        self.win.mainloop()
        self.stlable.setvar()

    def onB64StrChange(self, str):
        st = str.get()
        print(printBuffromB64(st))
        #self.b64str.set( printBuffromB64(st))


    def setupMenu(self):
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="load file...", command=self._openfile)
        fileMenu.add_command(label="exit", command=self._quit)


    def setupCheckboxes(self):
        lf_encheck= LabelFrame(self.win, text="Items", width=900, height=10)
        lf_encheck.pack(side=TOP, fill=X)
        global win_checkbox
        win_checkbox = PanedWindow(lf_encheck, width=900)
        win_checkbox.pack(fill=X)


    def setupStatus(self):
        ## setup status
        lf_status = LabelFrame(self.win, text="", width=900, height=10)
        lf_status.pack(side=BOTTOM, fill=X)
        stlable = tk.scrolledtext.ScrolledText(lf_status, bg="grey", width=98, height=20 )
        stlable.pack(side=BOTTOM, fill=X)

    def setupB64Entry(self):
        ## setup entry
        self.b64str.trace("w", lambda name, index, mode, sv=self.b64str:self.onB64StrChange(sv))
        self.b64str.set("please type Protobuf.Base64 here")
        lf_enbox = LabelFrame(self.win, text="base64", width=98, height=10)
        #lf_enbox.grid(row=0)
        lf_enbox.pack(side=BOTTOM, fill=X)
        enbox = Entry(lf_enbox, width=98, textvariable=self.b64str)
        enbox.pack(fill=X)


    def setupWindow(self):
        self.win.title("qfeel log tools")
        self.win.resizable(True, True)
        self.win.geometry('900x900')
        self.setupMenu()
        # setup workspace
        ## setup checkbox
        self.setupCheckboxes()
        self.setupCheckbox()
        self.setupB64Entry()
        self.setupStatus()



    def var_states(self,):
        print("male: %d,\nfemale: %d" % (11,33))


    def add_checkbox(self,name,callback):
        cb_items = Checkbutton(win_checkbox, text=name, bg='grey', command=callback, width=10)
        win_checkbox.add(cb_items, sticky="w")

    def setupCheckbox(self,):
        self.add_checkbox("aaaaa", self.var_states)
        self.add_checkbox("aaaaa", self.var_states)
        self.add_checkbox("aaaaa", self.var_states)
        self.add_checkbox("aaaaa", self.var_states)
        self.add_checkbox("aaaaa", self.var_states)


    def clean_checkbox(self):
        cb_items = Checkbutton(win_checkbox, text="name", bg='grey')
        win_checkbox.add(cb_items)



    def _quit(self):
        exit(0)


    def _openfile(self):
        filepath = tk.filedialog.askopenfilename(filetypes=[("logtype", ("*.log", "*.last")), ("all", "*.*")])
        if os.path.exists(filepath):
            print("open file", filepath)
            fin = open(filepath, 'r', encoding="utf-8")
            self.ststr.set(filepath)
        else:
            print("file not exist!", filepath)
            filepath = ""


if __name__ == '__main__':

    win_ = Win()

    win_.loop()
