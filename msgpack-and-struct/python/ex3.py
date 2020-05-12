

import msgpack
import struct

MSG_UPDATE_PID = 0x2000

#***************************************************************************************************************

def msgpack_ex():

  proportional = 1.0
  integral     = 2.0
  derivitive   = 3.0

#***************************************************************************************************************

def struct_ex():

  payload      = 'idddd'
  header       = MSG_UPDATE_PID
  proportional = 1.1
  integral     = 2.2
  derivitive   = 3.3
  gain         = 4.0

  packer = struct.Struct(payload)
  pid    = (header,proportional,integral,derivitive,gain)

  tx = packer.pack(*pid)
  rx = struct.unpack(payload, tx) 

  print("Packed TX packet   : ",tx)
  print("Unpacked RX packet : ",rx) 

#***************************************************************************************************************

struct_ex()
