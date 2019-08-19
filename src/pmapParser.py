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


# 第一个返回值: 如果返回""，说明没有识别出object type, 第二个返回值无效
# 第二个返回值: mapObject
def getMapObject(filename):
    fileHandle = open(filename, 'rb')
    if fileHandle:
        bs = fileHandle.read()
        mapObjectType = ""
        print("reading file:" + filename + " len: " + str(len(bs)))
        try:
            mapObjectType = "PbFloor"
            mapObject = PbMap_pb2.PbFloor()
            mapObject.ParseFromString(bs)
            return mapObjectType, mapObject
        except:
            print("try %s Failed" % mapObjectType)

        try:
            mapObjectType = "PbInput"
            mapObject = PbInput_pb2.PbInput()
            mapObject.ParseFromString(bs)
            return mapObjectType, mapObject
        except:
            print("try %s Failed" % mapObjectType)

        try:
            mapObjectType = "PbOutput"
            mapObject = PbOutput_pb2.PbOutput()
            mapObject.ParseFromString(bs)
            return mapObjectType, mapObject
        except:
            print("try %s Failed" % mapObjectType)

        try:
            mapObjectType = "PbMapData"
            mapObject = PbMap_pb2.PbMapData()
            mapObject.ParseFromString(bs)
            return mapObjectType, mapObject
        except:
            print("try %s Failed" % mapObjectType)

        try:
            if len(bs) > 10:
                bs2 = bs[10:]
                print(len(bs2))
                mapObject = PbOutput_pb2.PbOutput()
                mapObject.ParseFromString(bs2)
                rawfile = open("pbmapraw.pb", 'wb')
                rawfile.write(bs2, len(bs2))
                rawfile.close()

            mapObjectType = "QGlobalMap"
            return mapObjectType, mapObject
        except:
            print("try %s Failed" % mapObjectType)

    else:
        mapObjectType = ""
        print("cannot open file: " + filename)
        return mapObjectType, ""


if __name__ == '__main__':
    if len(argv) == 2:
        filePath = argv[1]
        getMapObject(filePath)

    else:
        print("need file name ")
