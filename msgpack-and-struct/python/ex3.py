

import msgpack
import struct

MSG_UPDATE_PID = 0x2000

#***************************************************************************************************************

def msgpack_ex():

  header       = MSG_UPDATE_PID

  proportional = 1.0
  integral     = 2.0
  derivitive   = 3.0
  gain         = 4.0

  packet = [header,proportional,integral,derivitive,gain]
  tx     = msgpack.packb(packet)
  rx     = msgpack.unpackb(tx)

  _header,_proportional,_integral,_derivitive,_gain = rx

  print("MsgPack Packed TX packet   : ",tx)
  print("MsgPack Unpacked RX packet : ",rx)
  print("Header                     : ",hex(_header)) 
  print("Proportional               : ",_proportional) 
  print("Integral                   : ",_integral) 
  print("Derivitive                 : ",_derivitive) 
  print("Gain                       : ",_gain) 

#***************************************************************************************************************

def struct_ex():

  payload      = 'idddd'
  header       = MSG_UPDATE_PID

  proportional = 1.1
  integral     = 2.2
  derivitive   = 3.3
  gain         = 4.0

  packer = struct.Struct(payload)
  packet = (header,proportional,integral,derivitive,gain)

  tx = packer.pack(*packet)
  rx = struct.unpack(payload, tx) 


  _header,_proportional,_integral,_derivitive,_gain = rx

  print("Struct Packed TX packet   : ",tx)
  print("Struct Unpacked RX packet : ",rx) 
  print("Header                    : ",hex(_header)) 
  print("Proportional              : ",_proportional) 
  print("Integral                  : ",_integral) 
  print("Derivitive                : ",_derivitive) 
  print("Gain                      : ",_gain) 

#***************************************************************************************************************

struct_ex()
print()
msgpack_ex()

