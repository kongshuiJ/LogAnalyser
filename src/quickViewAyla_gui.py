#!/usr/bin/python3

import tkinter as tk
from tkinter import *
import tkinter.messagebox
import re

import logparser
LOG_CAT = r'^\[([DIEW])\](\S*)[ ]{1,6}([0-9\.]*)[\s]+([\S]*):([0-9]*)[\s]*\| (.*)$'


class QuickViewAyla:
    def __init__(self, logFilePath):
        # yapf: disable
        self.quickViewWin   = None
        self.stlable        = None
        self.logFilePath    = logFilePath
        self.SFMList        = []
        self.errorDict      = []
        self.stateDict      = []
        self.ctrDict        = []
        self.result         = []
        self.stateResult    = []
        self.errorResult    = []
        self.audioResult    = []
        self.ctrResult      = []
        # yapf: enable

        self.setupWindow()
        self.setUpStlable()
        self.signalLOGAnalysis()

    def signalLOGAnalysis(self):
        f = open(self.logFilePath, "r", encoding="utf-8")
        self.stlable.delete(1.0, END)
        for line in f.readlines():
            # 将每行Ayla:[]包含的指令获取到
            line = line[len('1453366216 INFO QF : '):]
            line = line.strip()
            AylaStr = "Ayla:["
            start = line.find(AylaStr)
            end = line.find("]", start)
            if 0 < start and 0 < end:
                time = 0
                # 获取时间
                gp = re.match(LOG_CAT, line)
                if not gp:
                    continue
                else:
                    time = float(gp.group(3))

                base64Str = line[start + len(AylaStr):end]
                self.stlable.insert('end', "time: %.3fs\n" % time)
                self.stlable.insert('end', "encode:\n")
                self.stlable.insert('end', "    %s\n" % base64Str)
                self.stlable.insert('end', "dencode:\n    ")
                self.stlable.insert('end',
                                    logparser.printBuffromB64(base64Str))
                self.stlable.insert('end',
                                    "===================================\n")
                self.stlable.pack(side=LEFT, fill=BOTH)

    def setupWindow(self):
        self.quickViewWin = tk.Tk()
        self.quickViewWin.title("quick view log: %s" % self.logFilePath)
        self.quickViewWin.resizable(True, True)
        self.quickViewWin.geometry('700x700')

    def setUpStlable(self):
        self.stlable = tk.scrolledtext.ScrolledText(self.quickViewWin,
                                                    width=98,
                                                    height=20)
        self.stlable.pack(side=BOTTOM, fill=X)
