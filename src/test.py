#!/usr/bin/python3

import os
import sys
from sys import argv
import binascii
import re
import json

sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../protobuf_release/py")

import PbInput_pb2
import PbOutput_pb2
import PbMap_pb2
import base64

from commonUtils import *


def tryPrintMap(filename):
    f = open(filename, 'rb')
    if f:
        bs = f.read()
        print("reading file:" + filename + " len: " + str(len(bs)))
        try:
            out = PbMap_pb2.PbFloor()
            out.ParseFromString(bs)
            print("file type is PbFloor:")
            print(out)
            return
        except:
            print("try PbMap Failed")

        try:
            out = PbInput_pb2.PbInput()
            out.ParseFromString(bs)
            print("file type is PbInput:")
            print(out)
            return
        except:
            print("try  PbInput Failed")

        try:
            out = PbOutput_pb2.PbOutput()
            out.ParseFromString(bs)
            print("file type is PbOutput:")
            print(out)
            return
        except:
            print("try PbOut Failed")

        try:
            out = PbMap_pb2.PbMapData()
            out.ParseFromString(bs)
            print("file type is PbMapData:")
            print(out)
            return
        except:
            print("try  PbMapData Failed")

        try:
            if len(bs) > 10:
                bs2 = bs[10:]
                print(len(bs2))
                out = PbOutput_pb2.PbOutput()
                out.ParseFromString(bs2)
                rawfile = open("pbmapraw.pb", 'wb')
                rawfile.write(bs2, len(bs2))
                rawfile.close()

            print("file type is QGlobalMap:")
            print(out)
            return
        except:
            print("try  QGlobalMap Failed")

    else:
        print("cannot open file " + filename)


if __name__ == '__main__':
    if len(argv) == 2:
        filePath = argv[1]
        tryPrintMap(filePath)

    else:
        print("need file name ")
