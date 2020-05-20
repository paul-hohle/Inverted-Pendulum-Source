#!/usr/bin/python3.7

#**************************************************************************

import socket
import msgpack
import sys
from Messages import controllerMsgs as Msg

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

def handle_ai_mode_msg(packet):
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

def handle_windup_mode_msg(packet):
    print ("Set windup test mode")
    return False

def handle_comm_test_mode_msg(packet):
    print ("Set comm test mode")
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

messages = { Msg.TX_MSG_SET_IDLE_MODE             : handle_idle_mode_msg,
             Msg.TX_MSG_SET_MANUAL_MODE           : handle_manual_mode_msg,
             Msg.TX_MSG_SET_PID_MODE              : handle_pid_mode_msg,
             Msg.TX_MSG_SET_STATE_SPACE_MODE      : handle_state_space_mode_msg,
             Msg.TX_MSG_SET_AI_MODE               : handle_ai_mode_msg,
             Msg.TX_MSG_SET_PENDULUM_PERIOD_MODE  : handle_pendulum_period_mode_msg,
             Msg.TX_MSG_SET_PENDULUM_LENGTH_MODE  : handle_pendulum_length_mode_msg,
             Msg.TX_MSG_SET_RAIL_LENGTH_MODE      : handle_rail_length_mode_msg,
             Msg.TX_MSG_SET_RAIL_CENTER_MODE      : handle_rail_center_mode_msg,
             Msg.TX_MSG_SET_WINDUP_MODE           : handle_windup_mode_msg,
             Msg.TX_MSG_SET_COMM_TEST_MODE        : handle_comm_test_mode_msg,
             Msg.TX_MSG_USE_ROTARY_ENCODER        : handle_rotary_encoder_msg,
             Msg.TX_MSG_USE_ACCELEROMETER         : handle_accelerometer_msg,

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
