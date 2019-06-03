import tkinter as tk
from tkinter import *
from tkinter import scrolledtext    # 导入滚动文本框的模块
import sys
import os
import re
import time
import threading
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox

from logparser import *

RE_LISTS = []

# systemLevelLogDict存放每个系统级log的选中状态 选中 True  未选中 False
# 如 [D] [I] [E] [M]
systemLevelLogDict = {}

class Win:
    def __init__(self):
        self.win = tk.Tk()
        self.stlable = tk.scrolledtext.ScrolledText(self.win, bg="grey", width=98, height=20 )
        self.win_checkbox = None
        self.list_checkboxes = None
        self.filePath=""
        self.logLists = []
        self.itemsList = []
        self.logLevelList = []
        self.b64str = StringVar()
        self.logScrolledText = None
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
        fileMenu.add_command(label="load file...", command=self._parseFile)
        fileMenu.add_command(label="exit", command=self._quit)


    def setupCheckboxes(self):
        lf_encheck= LabelFrame(self.win, text="Items", width=900, height=10)
        lf_encheck.pack(side=TOP, fill=X)
        global win_checkbox
        win_checkbox = PanedWindow(lf_encheck, width=900)
        win_checkbox.pack(fill=X)


    def setupLogText(self):
        self.logScrolledText = scrolledtext.ScrolledText(self.win, width = 500, height = 35)
        self.logScrolledText.pack()
        sl = Scrollbar(self.win)
        sl.pack(side = RIGHT,fill = Y)


    def setupStatus(self):
        ## setup status
        lf_status = LabelFrame(self.win, text="Test", width=900, height=10)
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
        self.setupLogText()
        self.setupCheckButton()
        self.setupB64Entry()
        self.setupStatus()


    def var_states(self,):
        print("male: %d,\nfemale: %d" % (11,33))


    def add_checkbox(self, name, callback):
        cb_items = Checkbutton(win_checkbox, text=name, bg='grey', command=callback, width=10)
        win_checkbox.add(cb_items, sticky="w")


    def add_checkbox1(self, name, callback):
        global systemLevelLogDict
        systemLevelLogDict[name] = False
        cb_items = Checkbutton(win_checkbox, text=name, bg='grey', command=callback, width=10, height = 1)
        win_checkbox.add(cb_items, sticky="w")


    def refreshTextInfo(self,):
        global systemLevelLogDict

        self.logScrolledText.delete('1.0','end')

        for listContent in self.logLevelList:
            for level in systemLevelLogDict:
                if level == listContent.lvl and True == systemLevelLogDict[level]:
                    self.logScrolledText.insert(INSERT, str(listContent.time))
                    self.logScrolledText.insert(INSERT, "   ")
                    self.logScrolledText.insert(INSERT, listContent.log)
                    self.logScrolledText.insert(INSERT, "\n")

            if True == listContent.filteredInfoDisplayFlag:
                self.logScrolledText.insert(INSERT, str(listContent.time))
                self.logScrolledText.insert(INSERT, "   ")
                self.logScrolledText.insert(INSERT, listContent.filteredInfo)
                self.logScrolledText.insert(INSERT, "\n")
        

    def systemLog(self, name):
        global systemLevelLogDict

        systemLevelLogDict[name] = bool(1 - systemLevelLogDict[name])
        print("name:" , name)
        print(systemLevelLogDict[name])
        self.refreshTextInfo()


    def USR_CTR_log(self, name):
        if 0 == len(self.itemsList):
            self.itemsList = filterll(self.logLevelList, RE_LISTS)

        for listContent in self.logLevelList:
            for l in RE_LISTS[name]:
                if 0 <= listContent.filteredInfo.find(l[1]):
                    listContent.filteredInfoDisplayFlag = bool(1 - listContent.filteredInfoDisplayFlag)

        self.refreshTextInfo()


    def setupCheckButton(self,):
        global RE_LISTS

        self.add_checkbox1(LOG_LEVEL[0][1], lambda:self.systemLog(LOG_LEVEL[0][1]))
        self.add_checkbox1(LOG_LEVEL[1][1], lambda:self.systemLog(LOG_LEVEL[1][1]))
        self.add_checkbox1(LOG_LEVEL[2][1], lambda:self.systemLog(LOG_LEVEL[2][1]))
        self.add_checkbox1(LOG_LEVEL[3][1], lambda:self.systemLog(LOG_LEVEL[3][1]))

        #for itemName in RE_LISTS:
        #    self.add_checkbox(itemName, lambda:self.USR_CTR_log(itemName, 0))
        self.add_checkbox("RE_UC", lambda:self.USR_CTR_log("RE_UC"))
        self.add_checkbox("RE_UD", lambda:self.USR_CTR_log("RE_UD"))


    def clean_checkbox(self):
        cb_items = Checkbutton(win_checkbox, text="name", bg='grey')
        win_checkbox.add(cb_items)


    def _quit(self):
        exit(0)


    def _parseFile(self):
        filePath = tk.filedialog.askopenfilename(filetypes=[("logtype", ("*.log", "*.last")), ("all", "*.*")])
        if os.path.exists(filePath):
            print("open file", filePath)

            # 确定打开文件后,对log文件进行解析
            fileLine, fileSize, self.logLists = loadLogFile(filePath)
            self.logLevelList = filter_category(self.logLists)

        else:
            print("file not exist!", filePath)
            filePath = ""


if __name__ == '__main__':

    RE_LISTS = parseItemFile("test.json")

    win_ = Win()

    win_.loop()
