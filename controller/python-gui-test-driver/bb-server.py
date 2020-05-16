#!/usr/bin/python3.7

#**************************************************************************

import socket
import msgpack
import sys

#**************************************************************************

def handle_idle_mode_msg(packet):

    print ("Set idle mode")
    return False


def handle_manual_mode_msg(packet):

    print ("Set manual mode")
    return False


def handle_pid_mode_msg(packet):

    print ("Set PID mode")
    return False

def handle_state_space_mode_msg(packet):

    print ("Set State Space mode")
    return False

def handle_ai_controller_mode_msg(packet):
    print ("Set AI controller mode")
    return False

def handle_pendulum_period_mode_msg(packet):
    print ("Set pendulum period test mode")
    return False

def handle_pendulum_length_mode_msg(packet):
    print ("Set pendulum length test mode")
    return False

def handle_rail_length_mode_msg(packet):
    print ("Set rail length test mode")
    return False

def handle_rail_center_mode_msg(packet):
    print ("Set rail center test mode")
    return False

def handle_accelerometer_msg(packet):

    print ("Use accelerometer angle sensor")
    return False

def handle_rotary_encoder_msg(packet):

    print ("Use rotary encoder angle sensor")
    return False

def handle_shutdown_msg(packet):

    print ("Shutdown")
    return True

messages = { 0x2000 : handle_idle_mode_msg,
             0x2001 : handle_manual_mode_msg,
             0x2002 : handle_pid_mode_msg,
             0x2003 : handle_state_space_mode_msg,
             0x2004 : handle_ai_controller_mode_msg,
             0x2005 : handle_pendulum_period_mode_msg,
             0x2006 : handle_pendulum_length_mode_msg,
             0x2007 : handle_rail_length_mode_msg,
             0x2008 : handle_rail_center_mode_msg,

             0x4000 : handle_rotary_encoder_msg,
             0x4001 : handle_accelerometer_msg,

             0xffff : handle_shutdown_msg,
           }

#**************************************************************************

def Main():

    host = "192.168.6.2"
    port = 6666

    print (socket.gethostname())

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    shutdown = False

    while shutdown == False:
            received = conn.recv(1024)

            if received:
               packet = msgpack.unpackb(received)

               header  = packet[0]
               print (header)

               handler = messages[header]
               if handler != None:
                  shutdown = handler(packet)
               else:
                   print ("No msg handler: ",hex(header))
                   shutdown = True


    conn.close()

if __name__ == '__main__':
    Main()
