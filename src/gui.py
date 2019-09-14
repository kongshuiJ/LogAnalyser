#!/usr/bin/python3

import sys
sys.path.append("..")
sys.path.append("../protobuf_release/py")
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext  # 导入滚动文本框的模块
import os
import re
import time
import threading
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox

import logparser
import quickViewLog_gui
import quickViewAyla_gui
import commonUtils
import pmapParser

# yapf: disable

VERSION = "0.1.8"

# systemLevelLogDict存放每个系统级log的选中状态 选中 True  未选中 False
# 如 [D] [I] [E] [M]
systemLevelLogDict = {}

# yapf: enable


class Win:
    def __init__(self):
        # yapf: disable
        self.win            = tk.Tk()
        self.stlable        = None
        self.win_checkbox   = None
        self.font           = commonUtils.setFont(12)
        self.logFilePath    = ""
        self.pmapFilePath   = ""
        self.logList        = []
        self.b64str         = StringVar()
        self.logListbox     = None
        self.logScrollbar   = None

        self.label_logFilePath          = StringVar()
        self.userLevelLogList           = []
        self.list_checkboxes            = None
        self.userLevelLogWin_checkbox   = None

        self.setupWindow()

        self.logLanguageIndex           = 2    # 1: chinese    2:english 对应json文件
        self.quickViewLogToplevel       = None
        self.systemLevelLogWin_checkbox = None
        # yapf: enable

    def loop(self):
        self.win.mainloop()
        self.stlable.setvar()

    def onB64StrChange(self, searchStr):
        global systemLevelLogDict
        self.stlable.delete(1.0, END)
        base64Str = searchStr.get()
        if 0 == len(base64Str):
            return


#       # 判断输入的base64字符串是否被包含在被选中的log信息中
#       if 0 == len(self.logListbox.curselection()):
#           return
#       curSelectStr = self.logListbox.get(self.logListbox.curselection())
#       if 0 <= curSelectStr.find(base64Str):
#           self.stlable.insert('end', curSelectStr)

        for listContent in self.logList:
            for level in systemLevelLogDict:
                if True == listContent.filteredInfoDisplayFlag and level == listContent.lvl and True == systemLevelLogDict[
                        level]:
                    if 0 <= listContent.filteredInfo.find(
                            base64Str) or 0 <= str(listContent.time).find(
                                base64Str) or 0 <= listContent.lvl.find(
                                    base64Str):
                        printContent = (
                            "%-12s" + "%-10s" +
                            listContent.filteredInfo) % (str(
                                ("%.3f" % listContent.time)), listContent.lvl)
                        self.stlable.insert('end', printContent)
                        self.stlable.insert('end', "\n")

    def _chineseLanguage(self):
        self.logLanguageIndex = 1
        if 0 != len(self.userLevelLogList):
            self.userLevelLogList.clear()
            self.userLevelLogList = logparser.filterll(self.logList, RE_LISTS,
                                             self.logLanguageIndex)

    def _englishLanguage(self):
        self.logLanguageIndex = 2
        if 0 != len(self.userLevelLogList):
            self.userLevelLogList.clear()
            self.userLevelLogList = logparser.filterll(self.logList, RE_LISTS,
                                             self.logLanguageIndex)

    def quickViewLog(self):
        self.quickViewLog = quickViewLog_gui.QuickViewLog(self.logFilePath)

    def quickViewAyla(self):
        self.quickViewAyla = quickViewAyla_gui.QuickViewAyla(self.logFilePath)

    def setupMenu(self):
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        fileMenu = Menu(menuBar)

        # 文件栏
        menuBar.add_cascade(label="files", menu=fileMenu, font=commonUtils.setFont(12))
        fileMenu.add_command(label="open log file",
                             command=lambda: self._parseFile("log"),
                             font=commonUtils.setFont(12))
        fileMenu.add_command(label="open pmap file",
                             command=lambda: self._parseFile("pmap"),
                             font=commonUtils.setFont(12))
        fileMenu.add_command(label="exit",
                             command=self._quit,
                             font=commonUtils.setFont(12))

        # 语言栏
        languageMenu = Menu(menuBar)
        menuBar.add_cascade(label="language",
                            menu=languageMenu,
                            font=commonUtils.setFont(12))
        # 此处的command调用的函数应该可以用lambda代替lambda : (self.logLanguageIndex = 1)
        languageMenu.add_command(label="中文",
                                 command=self._chineseLanguage,
                                 font=commonUtils.setFont(12))
        languageMenu.add_command(label="english",
                                 command=self._englishLanguage,
                                 font=commonUtils.setFont(12))

        # 视图栏
        viewMenu = Menu(menuBar)
        menuBar.add_cascade(label="quick view",
                            menu=viewMenu,
                            font=commonUtils.setFont(12))
        viewMenu.add_command(label="log file",
                             command=self.quickViewLog,
                             font=commonUtils.setFont(12))
        viewMenu.add_command(label="Ayla instruction",
                             command=self.quickViewAyla,
                             font=commonUtils.setFont(12))

    def setupCheckboxes(self):
        global RE_LISTS

        lf_encheck = LabelFrame(self.win,
                                text="Search term",
                                width=900,
                                height=10,
                                font=commonUtils.setFont(12))
        lf_encheck.pack(side=TOP, fill=X)

        self.win_checkbox = PanedWindow(lf_encheck, orient=VERTICAL)
        self.win_checkbox.pack(fill=X)

        # 系统级log
        systemLevelLogLabel = tk.Label(self.win_checkbox,
                                       text=" system level: ",
                                       font=commonUtils.setFont(11)).grid(row=7)
        for index, logLevel in enumerate(logparser.SYSTEM_LOG_LEVEL):
            self.addSystemLevelCheckbox(
                index, logLevel[1],
                (lambda x: lambda: self.systemLevelLog(x))(logLevel[1]))

        # 用户级log
        userLevelLogLabel = tk.Label(self.win_checkbox,
                                     text="   user level:   ",
                                     font=commonUtils.setFont(11)).grid(row=9)
        for index, itemName in enumerate(RE_LISTS):
            self.addUserLevelCheckbox(
                index, itemName,
                (lambda x: lambda: self.userLevelLog(x))(itemName))

    def setupScrollbar(self):
        self.logScrollbar = Scrollbar(self.win)
        self.logScrollbar.pack(side=RIGHT, fill=Y)
        self.logListbox = Listbox(self.win,
                                  width=500,
                                  height=45,
                                  yscrollcommand=self.logScrollbar.set,
                                  font=commonUtils.setFont(11))
        self.logScrollbar.config(command=self.logListbox.yview)

    def setupStatus(self):
        ## setup status
        lf_status = LabelFrame(self.win,
                               text="Filtered information",
                               width=900,
                               height=10,
                               font=commonUtils.setFont(12))
        lf_status.pack(side=BOTTOM, fill=X)
        self.stlable = tk.scrolledtext.ScrolledText(lf_status,
                                                    bg="grey",
                                                    width=98,
                                                    height=15)
        self.stlable.pack(side=BOTTOM, fill=X)

    def setupB64Entry(self):
        ## setup entry
        self.b64str.set("please type Protobuf.Base64 here")
        self.b64str.trace(
            "w",
            lambda name, index, mode, sv=self.b64str: self.onB64StrChange(sv))
        lf_enbox = LabelFrame(self.win,
                              text="base64",
                              width=98,
                              height=10,
                              font=commonUtils.setFont(12))
        lf_enbox.pack(side=BOTTOM, fill=X)
        enbox = Entry(lf_enbox, width=98, textvariable=self.b64str)
        enbox.pack(fill=X)

    def setupWindow(self):
        self.win.title("qfeel log tools %s" % VERSION)
        self.win.resizable(True, True)
        self.win.geometry('900x900')
        self.setupMenu()

        # Label窗口显示文件名
        self.label_logFilePath.set("No files are currently open")
        tk.Label(self.win,
                 textvariable=self.label_logFilePath,
                 font=commonUtils.setFont(12)).pack()

        # setup workspace
        ## setup checkbox
        self.setupCheckboxes()
        self.setupScrollbar()
        self.setupStatus()
        self.setupB64Entry()

    def var_states(self, ):
        print("male: %d,\nfemale: %d" % (11, 33))

    # 添加用户级log的按钮
    def addUserLevelCheckbox(self, index, name, callback):
        cb_items = Checkbutton(self.win_checkbox,
                               text=name,
                               command=callback,
                               width=15,
                               height=1,
                               indicatoron=False)
        cb_items.grid(row=10, column=index)

    # 添加系统级log的按钮,默认勾选
    def addSystemLevelCheckbox(self, index, name, callback):
        global systemLevelLogDict
        systemLevelLogDict[name] = True
        cb_items = Checkbutton(self.win_checkbox,
                               text=name,
                               command=callback,
                               width=15,
                               height=1,
                               indicatoron=False)
        cb_items.select()
        cb_items.grid(row=8, column=index)

    # 刷新文本框，全部重新输出
    def refreshTextInfo(self, ):
        global systemLevelLogDict

        self.logListbox.delete(0, END)

        for listContent in self.logList:
            for level in systemLevelLogDict:
                if True == listContent.filteredInfoDisplayFlag and level == listContent.lvl and True == systemLevelLogDict[
                        level]:
                    printContent = (
                        "%-12s" + "%-10s" + listContent.filteredInfo) % (str(
                            ("%.3f" % listContent.time)), ("%-10s" %
                                                           listContent.lvl))
                    self.logListbox.insert(END, printContent)
                    self.logListbox.pack(side=LEFT, fill=BOTH)

    # 系统级log SYSTEM_LOG_LEVEL
    def systemLevelLog(self, name):
        global systemLevelLogDict

        systemLevelLogDict[name] = bool(1 - systemLevelLogDict[name])
        self.refreshTextInfo()

    # 用户级log json文件内正则表达式过滤出来的信息
    def userLevelLog(self, name):
        if 0 == len(self.userLevelLogList):
            self.userLevelLogList = logparser.filterll(self.logList, RE_LISTS,
                                             self.logLanguageIndex)

        for listContent in self.logList:
            for l in RE_LISTS[name]:
                if 0 <= listContent.filteredInfo.find(
                        l[self.logLanguageIndex]
                    [0:l[self.logLanguageIndex].find("%s")]):
                    listContent.filteredInfoDisplayFlag = bool(
                        1 - listContent.filteredInfoDisplayFlag)

        self.refreshTextInfo()

    def clean_checkbox(self):
        cb_items = Checkbutton(systemLevelLogWin_checkbox,
                               text="name",
                               bg='grey')
        systemLevelLogWin_checkbox.add(cb_items)

    def _quit(self):
        exit(0)

    def _parseFile(self, fileType):
        # 一旦选择新开一个文件，之前的解析的文件内容全部清空
        if 0 < len(self.logFilePath):
            # yapf: disable
            self.logFilePath        = ""
            self.pmapFilePath       = ""
            self.logList            = []
            self.userLevelLogList   = []
            self.label_logFilePath.set("No files are currently open")
            # yapf: enable

        filePath = None
        if "log" == fileType:
            filePath = tk.filedialog.askopenfilename(
                filetypes=[("logtype", ("*.log", "*.last")), ("all", "*.*")])
            self.logFilePath = filePath
        elif "pmap" == fileType:
            filePath = tk.filedialog.askopenfilename(
                filetypes=[("pmaptype", ("*.pmap")), ("all", "*.*")])
            self.pmapFilePath = filePath

        # 没有选择文件就直接关掉窗口
        if isinstance(filePath, tuple):
            return

        if os.path.exists(filePath):
            print("open file", filePath)

            if "log" == fileType:
                # 确定打开文件后,对log文件进行解析
                fileLine, fileSize, logList = logparser.loadLogFile(filePath)
                self.logList = logparser.filter_category(logList)
                self.refreshTextInfo()
            elif "pmap" == fileType:
                # 确定打开文件后,对pmap文件进行解析
                mapObjectType, mapObject = pmapParser.getMapObject(filePath)
                if "" != mapObjectType:
                    self.stlable.insert('end', mapObject)
                    self.stlable.insert('end', "\n")

            # label窗口显示当前打开的文件名
            self.label_logFilePath.set(filePath)
        else:
            print("file not exist!", self.logFilePath)
            self.logFilePath = ""
            self.pmapFilePath = ""

if __name__ == '__main__':

    RE_LISTS = logparser.parseItemFile("test.json")

    win_ = Win()

    win_.loop()
