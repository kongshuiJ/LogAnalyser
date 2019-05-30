#!/usr/bin/python3
import os
import sys
sys.path.append("..")
sys.path.append("../protobuf_release/py")

from protobuf_release.py import *
import base64
import binascii
import re

LOG_LEVEL = [
    ('[D]',                  '[D]'),
    ('[I]',                  '[I]'),
    ("[\033[1;31mE\033[0m]", '[E]'),
    ("[\033[1;33mW\033[0m]", '[W]'),
]

LOG_CAT = r'^\[([DIEW])\](\S*)[ ]{2,6}([0-9\.]*)[\s]+([\S]*):([0-9]*)[\s]*\| (.*)$'


RE_UC = [
    (r'.*USR_CTR_(\S*).*', '用户信号: %s', 'User Signal: %s '),
    ]

RE_LISTS = [RE_UC, ]


def printBuffromB64(str ):
    try:
        buf = str.encode(encoding="utf-8")
        raw = base64.b64decode(str)
        input = PbInput_pb2.PbInput()
        input.ParseFromString(raw)
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
            for re in LOG_LEVEL:
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


def filter(listraw, RELists):
    outList = []
    for l in listraw:
        needprint = False
        lout = ""
        for catogory in RELists:
            for pat in catogory:
                mg = re.match(pat[0], l)
                if mg:
                    print(lout)
                    needprint = True
                    lout = pat[1] % mg.groups()

        if needprint:
            outList.append(lout)
            print(lout)
    return outList


class LogItem:
    def __init__(self):
        self.lvl = ""
        self.category = ""
        self.time = float(0)
        self.file = ""
        self.line = int(0)
        self.log = ""

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
            s.lvl = gp.group(1)
            s.category = gp.group(2)
            s.time = float(gp.group(3))
            s.file = gp.group(4)
            s.line = int(gp.group(5))
            s.log = gp.group(6)
            return s


def filter_category(listraw,itemlist):
    itemlist = []
    for l in listraw:
        ll = LogItem.generate(l)
        if (ll):
            itemlist.append(ll)



if __name__ == '__main__':
    filepath="/Users/bacon/Documents/test.log"
    line, size, lists = loadLogFile(filepath)
    itlist = []
    filter_category(lists, itlist)

#   filter(lists, RE_LISTS)
#   print(line,size,len(lists))
#   printBuffromB64("SAE=")



