#!/usr/bin/python3

import os
import sys
sys.path.append("..")
sys.path.append("../protobuf_release/py")

#from protobuf_release.py import *
#from PbInput_pb2.py import *
#from ../protobuf_release/py import PbInput_pb2
import PbInput_pb2
import base64
import binascii
import re
import json

from commonUtils import *

# 系统级log
SYSTEM_LOG_LEVEL = [
    ('[D]',                  '[D]'),
    ('[I]',                  '[I]'),
    ("[\033[1;31mE\033[0m]", '[E]'),
    ("[\033[1;33mW\033[0m]", '[W]'),
]

LOG_CAT = r'^\[([DIEW])\](\S*)[ ]{2,6}([0-9\.]*)[\s]+([\S]*):([0-9]*)[\s]*\| (.*)$'

RE_LISTS = []


def printBuffromB64(base64Str):
    try:
        print( base64Str )
        buf = base64Str.encode(encoding="utf-8")
        raw = base64.b64decode(base64Str)
        input = PbInput_pb2.PbInput()
        input.ParseFromString(raw)
        print(input)
        return input
    except:
        return "Exception when parse base"


def loadLogFile(filename):
    linecnt = 0
    filesize = 0
    loglist = []
    f = None
    last_line = None
    try:
        f = open(filename)
        filesize = os.path.getsize(filename)

        for line in f:
            tmpline = line.replace('\n', '')
            isLvl = False
            for re in SYSTEM_LOG_LEVEL:
                if tmpline.find(re[0]) >= 0:
                    tmpline = tmpline.replace(re[0], re[1])
                    isLvl = True
                    if last_line:
                        linecnt += 1
                        loglist.append(last_line)
                    last_line = tmpline
            if not isLvl and last_line and tmpline:
                last_line = last_line + tmpline
        if last_line:
            loglist.append(last_line)
    except:
        print("error got ")
    return linecnt, filesize, loglist


def filterll(listraw, RELists, logLanguageIndex):
    outList = []

    # 如果选择的language index既不是1也不是2那么默认为1
    if 1 != logLanguageIndex and 2 != logLanguageIndex:
        logLanguageIndex = 1

    for catogory in RELists:
        print("cat:: ",catogory )
        for pat in RELists[catogory]:
            print(pat)

    for l in listraw:
        needprint = False
        for catogory in RELists:
            flag = False;
            for pat in RELists[catogory]:
                mg = re.match(eval(pat[0]), l.log)
                if mg:
                    needprint = True
                    l.filteredInfo = pat[logLanguageIndex] % mg.groups()
                    # 如果pat[logLanguageIndex]只包含“%s”，说明没有过滤到正确信息，所以直接跳过
                    if False == checkStrComposition(pat[logLanguageIndex].replace(" ", ""), ["s", "%"]):
                        flag = True
                        break

            if True == flag:
                break
        if needprint:
            outList.append(l.filteredInfo)

    return outList


class LogItem:
    def __init__(self):
        self.lvl = ""           # log级别
        self.category = ""      # log类别
        self.time = float(0)
        self.file = ""
        self.line = int(0)
        self.log = ""
        self.filteredInfo = ""  # 正则表达式过滤得到的信息
        self.filteredInfoDisplayFlag = False

    def __str__(self):
        return '%s %s %f %s %d ::::: %s' % ( self.lvl, self.category, self.time, self.file, self.line, self.log )

    @staticmethod
    def generate(log):
        gp = re.match(LOG_CAT, log)
        if not gp:
            print("ERROR:",log)
            return None
        else:
            s = LogItem()
            s.lvl = "[" + gp.group(1) + "]"
            s.category = gp.group(2)
            s.time = float(gp.group(3))
            s.file = gp.group(4)
            s.line = int(gp.group(5))
            s.log = gp.group(6)
            return s


def filter_category(listraw):
    itemlist = []
    for l in listraw:
        ll = LogItem.generate(l)
        if (ll):
            itemlist.append(ll)

    return itemlist


def parseItemFile(filePath):
    global RE_LISTS

    fileHandle = open(filePath, "r", encoding = "utf-8")
    readFile = fileHandle.read()
    RE_LISTS = json.loads(readFile)

    return RE_LISTS


if __name__ == '__main__':
    filePath="/home/bacon/logmain_log_file000.log"
    re_list = parseItemFile("test.json")
    #print(re_list)
    line, size, lists = loadLogFile(filePath)
    itlist = filter_category(lists)
    aa = filterll(itlist, RE_LISTS)
    for a in aa:
        print(a)
    #printBuffromB64("gAELygITCgdLaXRjaGVuGggyOUM2OUY3NQ==")


    
    #print(line,size,len(lists))
    #printBuffromB64("MQ==")
