#!/usr/bin/python3

import os
import sys
from sys import argv
import binascii
import re
import json

sys.path.append(sys.path[0]+"/..")
sys.path.append(sys.path[0]+"/../protobuf_release/py")

import PbInput_pb2
import PbOutput_pb2
import PbMap_pb2
import base64

from commonUtils import *

# 第一个返回值: 如果返回""，说明没有识别出object type, 第二个返回值无效
# 第二个返回值: object
def getMapObject(filename):
    fileHandle = open(filename, 'rb')
    if fileHandle :
        bs = fileHandle.read()
        objectType = ""
        print("reading file:" + filename +" len: " + str(len(bs)))
        try:
            mapObject = PbMap_pb2.PbFloor()
            mapObject.ParseFromString(bs)
            objectType = "PbFloor"
            return objectType, mapObject
        except:
            print("try %s Failed" % objectType)

        try:
            mapObject = PbInput_pb2.PbInput()
            mapObject.ParseFromString(bs)
            objectType = "PbInput"
            return objectType, mapObject
        except:
            print("try %s Failed" % objectType)

        try:
            mapObject = PbOutput_pb2.PbOutput()
            mapObject.ParseFromString(bs)
            objectType = "PbOutput"
            return objectType, mapObject
        except:
            print("try %s Failed" % objectType)

        try:
            mapObject = PbMap_pb2.PbMapData()
            mapObject.ParseFromString(bs)
            objectType = "PbMapData"
            return objectType, mapObject
        except:
            print("try %s Failed" % objectType)

        try:
            if len(bs) > 10:
                bs2 = bs[10:]
                print(len(bs2))
                mapObject = PbOutput_pb2.PbOutput()
                mapObject.ParseFromString(bs2)
                rawfile = open("pbmapraw.pb",'wb')
                rawfile.write(bs2,len(bs2))
                rawfile.close()
            
            objectType = "QGlobalMap"
            return objectType, mapObject
        except:
            print("try %s Failed" % objectType)

    else :
        print("cannot open file: " + filename)
        return objectType, ""


if __name__ == '__main__':
    if len(argv) == 2 :
        filePath=argv[1]
        getMapObject(filePath)

    else :
        print("need file name ")
