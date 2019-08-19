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

from logparser import *
from quickViewLog_gui import *
from quickViewAyla_gui import *
from commonUtils import *
from pmapParser import *

# yapf: disable

VERSION = "0.1.6"

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
        self.font           = setFont(12)
        self.logFilePath    = ""
        self.pmapFilePath   = ""
        self.logList        = []
        self.b64str         = StringVar()
        self.logListbox     = None
        self.logScrollbar   = None

        self.userLevelLogList           = []
        self.list_checkboxes            = None
        self.userLevelLogWin_checkbox   = None

        self.setupWindow()

        self.logLanguageIndex           = 1    # 1: chinese    2:english 对应json文件
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
            self.userLevelLogList = filterll(self.logList, RE_LISTS,
                                             self.logLanguageIndex)

    def _englishLanguage(self):
        self.logLanguageIndex = 2
        if 0 != len(self.userLevelLogList):
            self.userLevelLogList.clear()
            self.userLevelLogList = filterll(self.logList, RE_LISTS,
                                             self.logLanguageIndex)

    def quickViewLog(self):
        self.quickViewLog = QuickViewLog(self.logFilePath)

    def quickViewAyla(self):
        self.quickViewAyla = QuickViewAyla(self.logFilePath)

    def setupMenu(self):
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        fileMenu = Menu(menuBar)

        # 文件栏
        menuBar.add_cascade(label="文件", menu=fileMenu, font=setFont(12))
        fileMenu.add_command(label="打开log文件",
                             command=lambda: self._parseFile("log"),
                             font=setFont(12))
        fileMenu.add_command(label="打开pmap文件",
                             command=lambda: self._parseFile("pmap"),
                             font=setFont(12))
        fileMenu.add_command(label="退出", command=self._quit, font=setFont(12))

        # 语言栏
        languageMenu = Menu(menuBar)
        menuBar.add_cascade(label="语言", menu=languageMenu, font=setFont(12))
        # 此处的command调用的函数应该可以用lambda代替lambda : (self.logLanguageIndex = 1)
        languageMenu.add_command(label="中文",
                                 command=self._chineseLanguage,
                                 font=setFont(12))
        languageMenu.add_command(label="english",
                                 command=self._englishLanguage,
                                 font=setFont(12))

        # 视图栏
        viewMenu = Menu(menuBar)
        menuBar.add_cascade(label="快捷模式", menu=viewMenu, font=setFont(12))
        viewMenu.add_command(label="快速查看log信息",
                             command=self.quickViewLog,
                             font=setFont(12))
        viewMenu.add_command(label="快速查看Ayla指令",
                             command=self.quickViewAyla,
                             font=setFont(12))

    def setupCheckboxes(self):
        lf_encheck = LabelFrame(self.win,
                                text="搜索项",
                                width=900,
                                height=10,
                                font=setFont(12))
        lf_encheck.pack(side=TOP, fill=X)

        self.win_checkbox = PanedWindow(lf_encheck, orient=VERTICAL)
        self.win_checkbox.pack(fill=X)

        # 系统级log
        self.systemLevelLogWin_checkbox = PanedWindow(self.win_checkbox)
        self.win_checkbox.add(self.systemLevelLogWin_checkbox)
        systemLevelLogLabel = tk.Label(self.systemLevelLogWin_checkbox,
                                       text=" 系统级: ",
                                       font=setFont(11))
        self.systemLevelLogWin_checkbox.add(systemLevelLogLabel)

        # 用户级log
        self.userLevelLogWin_checkbox = PanedWindow(self.win_checkbox)
        self.win_checkbox.add(self.userLevelLogWin_checkbox)
        userLevelLogLabel = tk.Label(self.userLevelLogWin_checkbox,
                                     text=" 用户级: ",
                                     font=setFont(11))
        self.userLevelLogWin_checkbox.add(userLevelLogLabel)

    def setupScrollbar(self):
        self.logScrollbar = Scrollbar(self.win)
        self.logScrollbar.pack(side=RIGHT, fill=Y)
        self.logListbox = Listbox(self.win,
                                  width=500,
                                  height=35,
                                  yscrollcommand=self.logScrollbar.set,
                                  font=setFont(11))
        self.logScrollbar.config(command=self.logListbox.yview)

    def setupStatus(self):
        ## setup status
        lf_status = LabelFrame(self.win,
                               text="过滤后的信息",
                               width=900,
                               height=10,
                               font=setFont(12))
        lf_status.pack(side=BOTTOM, fill=X)
        self.stlable = tk.scrolledtext.ScrolledText(lf_status,
                                                    bg="grey",
                                                    width=98,
                                                    height=20)
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
                              font=setFont(12))
        lf_enbox.pack(side=BOTTOM, fill=X)
        enbox = Entry(lf_enbox, width=98, textvariable=self.b64str)
        enbox.pack(fill=X)

    def setupWindow(self):
        self.win.title("qfeel log tools %s" % VERSION)
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

    def var_states(self, ):
        print("male: %d,\nfemale: %d" % (11, 33))

    # 添加用户级log的按钮
    def addUserLevelCheckbox(self, name, callback):
        cb_items = Checkbutton(self.userLevelLogWin_checkbox,
                               text=name,
                               bg='grey',
                               command=callback,
                               width=10,
                               height=1,
                               indicatoron=False)
        self.userLevelLogWin_checkbox.add(cb_items, sticky="w")

    # 添加系统级log的按钮,默认勾选
    def addSystemLevelCheckbox(self, name, callback):
        global systemLevelLogDict
        systemLevelLogDict[name] = True
        cb_items = Checkbutton(self.systemLevelLogWin_checkbox,
                               text=name,
                               bg='grey',
                               command=callback,
                               width=10,
                               height=1,
                               indicatoron=False)
        self.systemLevelLogWin_checkbox.add(cb_items, sticky="w")

        cb_items.select()

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
            self.userLevelLogList = filterll(self.logList, RE_LISTS,
                                             self.logLanguageIndex)

        for listContent in self.logList:
            for l in RE_LISTS[name]:
                if 0 <= listContent.filteredInfo.find(
                        l[self.logLanguageIndex]
                    [0:l[self.logLanguageIndex].find("%s")]):
                    listContent.filteredInfoDisplayFlag = bool(
                        1 - listContent.filteredInfoDisplayFlag)

        self.refreshTextInfo()

    def setupCheckButton(self, ):
        global RE_LISTS
        global SYSTEM_LOG_LEVEL

        for logLevel in SYSTEM_LOG_LEVEL:
            self.addSystemLevelCheckbox(
                logLevel[1],
                (lambda x: lambda: self.systemLevelLog(x))(logLevel[1]))

        for itemName in RE_LISTS:
            self.addUserLevelCheckbox(
                itemName, (lambda x: lambda: self.userLevelLog(x))(itemName))

        self.refreshTextInfo()

    def clean_checkbox(self):
        cb_items = Checkbutton(systemLevelLogWin_checkbox,
                               text="name",
                               bg='grey')
        systemLevelLogWin_checkbox.add(cb_items)

    def _quit(self):
        exit(0)

    def _parseFile(self, fileType):
        filePath = ""
        if "log" == fileType:
            filePath = tk.filedialog.askopenfilename(
                filetypes=[("logtype", ("*.log", "*.last")), ("all", "*.*")])
            self.logFilePath = filePath
        elif "pmap" == fileType:
            filePath = tk.filedialog.askopenfilename(
                filetypes=[("pmaptype", ("*.pmap")), ("all", "*.*")])
            self.pmapFilePath = filePath

        if os.path.exists(filePath):
            print("open file", filePath)

            if "log" == fileType:
                # 确定打开文件后,对log文件进行解析
                fileLine, fileSize, logList = loadLogFile(filePath)
                self.logList = filter_category(logList)
                self.refreshTextInfo()
            elif "pmap" == fileType:
                # 确定打开文件后,对pmap文件进行解析
                mapObjectType, mapObject = getMapObject(filePath)
                if "" != mapObjectType:
                    self.stlable.insert('end', mapObject)
                    self.stlable.insert('end', "\n")

        else:
            print("file not exist!", self.logFilePath)
            self.logFilePath = ""
            self.pmapFilePath = ""

if __name__ == '__main__':

    RE_LISTS = parseItemFile("test.json")

    win_ = Win()

    win_.loop()
