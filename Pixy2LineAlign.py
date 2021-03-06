import pixy
from ctypes import *
from pixy import *
import threading
from networktables import NetworkTables
import math

frontUID = -619097246
rearUID = 316060495

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.46.69.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()
print("Connected!")

# Insert your processing code here

table = NetworkTables.getTable('DataTable')

if pixy.init()!=0:
    print("Pixy 2 not connected")
    exit()

if(pixy.getUID()==frontUID):
    isFrontLine = true
if(pixy.getUID()==rearUID):
    isFrontLine = false

pixy.change_prog ("line")

class Vector (Structure):
  _fields_ = [
    ("m_x0", c_uint),
    ("m_y0", c_uint),
    ("m_x1", c_uint),
    ("m_y1", c_uint),
    ("m_index", c_uint),
    ("m_flags", c_uint) ]

vectors = VectorArray(100)


while 1:
  line_get_all_features ()
  v_count = line_get_vectors (100, vectors)
  
  if(isFrontLine == true):
    if v_count > 0:
        for index in range (0, v_count):
                            yDifference = vectors[index].m_y1-vectors[index].m_y0
                            xDifference = vectors[index].m_x1-vectors[index].m_x0
                            distance = math.hypot(yDifference,xDifference)
                            angle = math.degrees(math.asin(xDifference/distance))
                            table.putNumber("LineX0F", vectors[index].m_x0)
                            table.putNumber("LineY0F", vectors[index].m_y0)
                            table.putNumber("LineX1F", vectors[index].m_x1)
                            table.putNumber("LineY1F", vectors[index].m_y1)
                            table.putNumber("LineAngleF", angle)
                            print '[VECTOR: INDEX=%d X0=%3d Y0=%3d X1=%3d Y1=%3d ANGLE=%3f]' % (vectors[index].m_index, vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1, angle)
    else:
        table.putNumber("isLineFDetected", false)
  else if(isFrontLine == false):
    if v_count > 0:
        for index in range (0, v_count):
                            yDifference = vectors[index].m_y1-vectors[index].m_y0
                            xDifference = vectors[index].m_x1-vectors[index].m_x0
                            distance = math.hypot(yDifference,xDifference)
                            angle = math.degrees(math.asin(xDifference/distance))
                            table.putNumber("LineX0R", vectors[index].m_x0)
                            table.putNumber("LineY0R", vectors[index].m_y0)
                            table.putNumber("LineX1R", vectors[index].m_x1)
                            table.putNumber("LineY1R", vectors[index].m_y1)
                            table.putNumber("LineAngleR", angle)
                            print '[VECTOR: INDEX=%d X0=%3d Y0=%3d X1=%3d Y1=%3d ANGLE=%3f]' % (vectors[index].m_index, vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1, angle)
    else:
        table.putNumber("isLineRDetected", false)

