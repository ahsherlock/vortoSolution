import math
import io

#Create file of helper classes to reduce redundancy in code.
class Cartesian:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Driver:
    def __init__(self, distance=0.0, route=[]):
        self.distanceTravelled = distancegit
        self.route = route

class DriverLoad:
    def __init__(self, id, pickup, dropoff):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.assigned = None
        self.delivery_distance = EuclideanDistance(pickup, dropoff)
        
def EuclideanDistance(p1, p2):
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    return math.sqrt(xDiff*xDiff + yDiff*yDiff)

def loadFromFile(filePath):
    f = open(filePath, "r")
    problemStr = f.read()
    f.close()
    return getProblemStr(problemStr)

def pointFromPointStr(pointStr):
    pointStr = pointStr.replace("(","").replace(")","")
    splits = pointStr.split(",")
    return Cartesian(float(splits[0]), float(splits[1]))

def getProblemStr(problemStr):
    loads = []
    buf = io.StringIO(problemStr)
    gotHeader = False
    while True:
        line = buf.readline()
        if not gotHeader:
            gotHeader = True
            continue
        if len(line) == 0:
            break
        line = line.replace("\n", "")
        splits = line.split()
        id = splits[0]
        pickup = pointFromPointStr(splits[1])
        dropoff = pointFromPointStr(splits[2])
        loads.append(DriverLoad(id, pickup, dropoff))
    return loads