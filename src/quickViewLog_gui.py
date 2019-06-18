import tkinter as tk
from tkinter import *
import tkinter.messagebox
import re

from commonUtils import *

class QuickViewLog:    
    def __init__(self, logFilePath):
        self.quickViewWin = None
        self.quickViewScrollbar = None
        self.quickViewListbox = None
        self.logScrollbar = None
        self.logListbox = None
        self.logFilePath = logFilePath
        self.result = []
        self.stateResult = []
        self.errorResult = []
        self.audioResult = []
        self.ctrResult = []
        
        self.setupWindow()
        self.setupScrollbar()
        self.setupMenu()
        self.signalLOGAnalysis()


    def signalLOGAnalysis(self):
        f = open(self.logFilePath, "r", encoding = "utf-8")
        for line in f.readlines():
            line = line.strip()
            if "STATE:: == EN ==>" in line:
                line = re.sub(u"([^\u0030-\u0039 . \u0041-\u005a])", "", line)
                spl = [stateDict[x] if x in stateDict else x for x in line.split( )]
                temp = ("%-15s" + spl[5]) % spl[1]
                self.stateResult.append(temp)
                self.result.append(temp)

            elif "ERROR_" in line:
                line = re.sub(u"([^\u0030-\u0039 . _ \u0041-\u005a])", "", line)
                spl = [errorDict[x] if x in errorDict else x for x in line.split( )]
                temp = ("%-15s" + spl[5]) % spl[1]
                self.errorResult.append(temp)
                self.result.append(temp)

            elif "AUDIO" in line:
                line = re.sub(u"([^\u0030-\u0039 . _ \u0041-\u005a])", "", line)
                spl = line.split( )
                temp = ("%-15s" + spl[4]) % spl[1]
                self.audioResult.append(temp)
                self.result.append(temp)

            elif "USR_CTR" in line:
                line = re.sub(u"([^\u0030-\u0039 . _ \u0041-\u005a])", "", line)
                spl = [ctrDict[x] if x in ctrDict else x for x in line.split( )]
                temp = ("%-15s" + spl[4]) % spl[1]
                self.ctrResult.append(temp)
                self.result.append(temp)


    # 整体分析
    def SFMAnalysis(self):
        self.logListbox.delete(0, END)
        for listContent in self.result:
            self.logListbox.insert(END, listContent)
            self.logListbox.pack(side = LEFT, fill = BOTH)

    # 状态分析
    def SFMStateAnalysis(self):
        self.logListbox.delete(0, END)
        for listContent in self.stateResult:
            self.logListbox.insert(END, listContent)
            self.logListbox.pack(side = LEFT, fill = BOTH)

    # 错误分析
    def SFMAudioAnalysis(self):
        self.logListbox.delete(0, END)
        for listContent in self.audioResult:
            self.logListbox.insert(END, listContent)
            self.logListbox.pack(side = LEFT, fill = BOTH)

    # 语音分析
    def SFMErrorAnalysis(self):
        self.logListbox.delete(0, END)
        for listContent in self.errorResult:
            self.logListbox.insert(END, listContent)
            self.logListbox.pack(side = LEFT, fill = BOTH)


    # 按键分析
    def SFMCtrAnalysis(self):
        self.logListbox.delete(0, END)
        for listContent in self.ctrResult:
            self.logListbox.insert(END, listContent)
            self.logListbox.pack(side = LEFT, fill = BOTH)


    def setupWindow(self):
        self.quickViewWin = tk.Tk()
        self.quickViewWin.title("quick view log")
        self.quickViewWin.resizable(True, True)
        self.quickViewWin.geometry('700x700')


    def setupScrollbar(self):
        self.logScrollbar = Scrollbar(self.quickViewWin)
        self.logScrollbar.pack(side = RIGHT, fill = Y)
        self.logListbox = Listbox(self.quickViewWin, width = 500, height = 35, yscrollcommand = self.logScrollbar.set, font = setFont(11))
        self.logScrollbar.config(command = self.logListbox.yview)


    def setupMenu(self):
        self.menubar = Menu(self.quickViewWin)
        self.quickViewWin.config(menu = self.menubar)
        self.sfmMenu = Menu(self.menubar)
        self.menubar.add_cascade(label = "状态机分析", menu = self.sfmMenu, font = setFont(12))

        for item in SFMList:
            if item == "整体分析":
                self.sfmMenu.add_command(label=item, command=self.SFMAnalysis, font=setFont(12))
            elif item == "状态分析":
                self.sfmMenu.add_command(label=item, command=self.SFMStateAnalysis, font=setFont(12))
            elif item == "错误分析":
                self.sfmMenu.add_command(label=item, command=self.SFMErrorAnalysis, font=setFont(12))
            elif item == "语音分析":
                self.sfmMenu.add_command(label=item, command=self.SFMAudioAnalysis, font=setFont(12))
            elif item == "按键分析":
                self.sfmMenu.add_command(label=item, command=self.SFMCtrAnalysis, font=setFont(12))
            else:
                print ("Function Is Not Achieve In SFM\n")


