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

# systemLevelLogDict存放每个系统级log的选中状态 选中 True  未选中 False
# 如 [D] [I] [E] [M]
systemLevelLogDict = {}

class Win:
    def __init__(self):
        self.win = tk.Tk()
        self.stlable = None
        self.win_checkbox = None
        self.systemLevelLogWin_checkbox = None
        self.userLevelLogWin_checkbox = None
        self.list_checkboxes = None
        self.filePath = ""
        self.logList = []
        self.userLevelLogList = []
        self.b64str = StringVar()
        self.logListbox = None
        self.logScrollbar = None
        self.setupWindow()


    def loop(self):
        self.win.mainloop()
        self.stlable.setvar()


    def onB64StrChange(self, str):
        self.stlable.delete(1.0, END)
        base64Str = str.get()
        if 0 == len(base64Str):
            return

        # 判断输入的base64字符串是否被包含在被选中的log信息中
        if 0 == len(self.logListbox.curselection()):
            return 

        curSelectStr = self.logListbox.get(self.logListbox.curselection())
        if 0 <= curSelectStr.find(base64Str):
            self.stlable.insert('end', curSelectStr)


    def setupMenu(self):
        menuBar = Menu(self.win)
        self.win.config(menu = menuBar)
        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label = "File", menu = fileMenu, font = ('Arial', 13, 'bold'))
        fileMenu.add_command(label = "load log file...", command = self._parseFile, font = ('Arial', 10, 'bold'))
        fileMenu.add_command(label = "exit", command = self._quit, font = ('Arial', 10, 'bold'))


    def setupCheckboxes(self):
        lf_encheck= LabelFrame(self.win, text = "Items", width = 900, height = 10, font = ('Arial', 11, 'bold'))
        lf_encheck.pack(side=TOP, fill = X)

        self.win_checkbox = PanedWindow(lf_encheck, orient = VERTICAL)
        self.win_checkbox.pack(fill = X)

        # 系统级log
        self.systemLevelLogWin_checkbox = PanedWindow(self.win_checkbox)
        self.win_checkbox.add(self.systemLevelLogWin_checkbox)
        systemLevelLogLabel = tk.Label(self.systemLevelLogWin_checkbox, text = "system level item: ", font = ('Arial', 10, 'bold'))
        self.systemLevelLogWin_checkbox.add(systemLevelLogLabel)

        # 用户级log
        self.userLevelLogWin_checkbox = PanedWindow(self.win_checkbox)
        self.win_checkbox.add(self.userLevelLogWin_checkbox)
        userLevelLogLabel = tk.Label(self.userLevelLogWin_checkbox, text = "  user level item  : ", font =('Arial', 10, 'bold'))
        self.userLevelLogWin_checkbox.add(userLevelLogLabel)


    def setupScrollbar(self):
        self.logScrollbar = Scrollbar(self.win)
        self.logScrollbar.pack(side = RIGHT, fill = Y)
        self.logListbox = Listbox(self.win, width = 500, height = 35, yscrollcommand = self.logScrollbar.set)
        self.logScrollbar.config(command = self.logListbox.yview)


    def setupStatus(self):
        ## setup status
        lf_status = LabelFrame(self.win, text = "Test", width = 900, height = 10, font = ('Arial', 11, 'bold'))
        lf_status.pack(side = BOTTOM, fill = X)
        self.stlable = tk.scrolledtext.ScrolledText(lf_status, bg="grey", width = 98, height = 20)
        self.stlable.pack(side=BOTTOM, fill=X)


    def setupB64Entry(self):
        ## setup entry
        self.b64str.set("please type Protobuf.Base64 here")
        self.b64str.trace("w", lambda name, index, mode, sv=self.b64str:self.onB64StrChange(sv))
        lf_enbox = LabelFrame(self.win, text = "base64", width = 98, height = 10, font = ('Arial', 11, 'bold'))
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
        self.setupScrollbar()
        self.setupCheckButton()
        self.setupStatus()
        self.setupB64Entry()


    def var_states(self,):
        print("male: %d,\nfemale: %d" % (11,33))


    # 添加用户级log的按钮
    def addUserLevelCheckbox(self, name, callback):
        cb_items = Checkbutton(self.userLevelLogWin_checkbox, text = name, bg = 'grey', command = callback, width = 10, height = 1)
        self.userLevelLogWin_checkbox.add(cb_items, sticky="w")


    # 添加系统级log的按钮,默认勾选
    def addSystemLevelCheckbox(self, name, callback):
        global systemLevelLogDict
        systemLevelLogDict[name] = True
        cb_items = Checkbutton(self.systemLevelLogWin_checkbox, text = name, bg = 'grey', command = callback, width = 10, height = 1)
        self.systemLevelLogWin_checkbox.add(cb_items, sticky="w")

        cb_items.select()


    # 刷新文本框，全部重新输出
    def refreshTextInfo(self,):
        global systemLevelLogDict

        self.logListbox.delete(0, END)

        for listContent in self.logList:
            for level in systemLevelLogDict:
                if level == listContent.lvl and True == systemLevelLogDict[level]:
                    self.logListbox.insert(END, str(listContent.time) + "       " + listContent.log)
                    self.logListbox.pack(side = LEFT, fill = BOTH)

            if True == listContent.filteredInfoDisplayFlag:
                self.logListbox.insert(END, str(listContent.time) + "       " + listContent.filteredInfo)
                self.logListbox.pack(side = LEFT, fill = BOTH)
        

    # 系统级log SYSTEM_LOG_LEVEL
    def systemLevelLog(self, name):
        global systemLevelLogDict

        systemLevelLogDict[name] = bool(1 - systemLevelLogDict[name])
        self.refreshTextInfo()


    # 用户级log json文件内正则表达式过滤出来的信息
    def userLevelLog(self, name):
        if 0 == len(self.userLevelLogList):
            self.userLevelLogList = filterll(self.logList, RE_LISTS)

        for listContent in self.logList:
            for l in RE_LISTS[name]:
                if 0 <= listContent.filteredInfo.find(l[1]):
                    listContent.filteredInfoDisplayFlag = bool(1 - listContent.filteredInfoDisplayFlag)

        self.refreshTextInfo()


    def setupCheckButton(self,):
        global RE_LISTS
        global SYSTEM_LOG_LEVEL 

        for logLevel in SYSTEM_LOG_LEVEL:
            self.addSystemLevelCheckbox(logLevel[1], (lambda x : lambda:self.systemLevelLog(x))(logLevel[1]))

        for itemName in RE_LISTS:
            self.addUserLevelCheckbox(itemName, (lambda x : lambda : self.userLevelLog(x))(itemName))

        self.refreshTextInfo()


    def clean_checkbox(self):
        cb_items = Checkbutton(systemLevelLogWin_checkbox, text="name", bg='grey')
        systemLevelLogWin_checkbox.add(cb_items)


    def _quit(self):
        exit(0)


    def _parseFile(self):
        filePath = tk.filedialog.askopenfilename(filetypes=[("logtype", ("*.log", "*.last")), ("all", "*.*")])
        if os.path.exists(filePath):
            print("open file", filePath)

            # 确定打开文件后,对log文件进行解析
            fileLine, fileSize, logList = loadLogFile(filePath)
            self.logList = filter_category(logList)
            self.refreshTextInfo()

        else:
            print("file not exist!", filePath)
            filePath = ""


if __name__ == '__main__':

    RE_LISTS = parseItemFile("test.json")

    win_ = Win()

    win_.loop()
