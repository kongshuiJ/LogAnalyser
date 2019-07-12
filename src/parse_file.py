import PbOutput_pb2
import PbInput_pb2
#import PbDefines_pb2
#import PbMessages_pb2
import base64
import sys
import PbMap_pb2

byte = None

sys.argv = ['python', '/Users/lzl/temp/no_credit.prop', 'pbfloor']

if len(sys.argv) < 3 :
    print("pleae input: %s input|output str" % (sys.argv[0]))
    sys.exit(1)

file = sys.argv[1]
type = sys.argv[2]
# data = base64.b64decode(str)
data = None
with open(file, "rb") as f:
    data = f.read()
    
if type == "input":
    print("\nPbInput: \"%s\"" % str)
    print("------------------------\n")
    input = PbInput_pb2.PbInput()
    input.ParseFromString(data)
    print(input)
    print("------------------------\n")
elif type == "output":
    print("\nPbOutput: \"%s\"" % str)
    print("------------------------\n")
    output = PbOutput_pb2.PbOutput()
    output.ParseFromString(data)
    print(output)
    print("------------------------\n")
elif type == "pbmap" :
    print("\nPbMap: \"%s\"" % str)
    print("------------------------\n")
    output = PbMap_pb2.PbMapData()
    output.ParseFromString(data)
    print(output)
    print("------------------------\n")
elif type == "pbfloor" :
    print("\pbFloor: \"%s\"" % str)
    print("------------------------\n")
    output = PbMap_pb2.PbFloor()
    output.ParseFromString(data)
    print(output)
    print("------------------------\n")        
else:
    print("pleae input: %s input|output str" % (sys.argv[0]))

