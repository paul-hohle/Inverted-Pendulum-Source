#!/usr/bin/env python3.5



#********************************************************************************************************

from PyQt5 import QtGui

#********************************************************************************************************

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QTimer

#********************************************************************************************************

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QDial
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget 
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QInputDialog

#********************************************************************************************************

import msgpack
import socket

#********************************************************************************************************

TX_MSG_GENERAL_BASE = 0

TX_MSG_RESET         = TX_MSG_GENERAL_BASE+0
TX_MSG_INIT          = TX_MSG_GENERAL_BASE+1
TX_MSG_SHUTDOWN      = TX_MSG_GENERAL_BASE+2
TX_MSG_PANIC         = TX_MSG_GENERAL_BASE+3

#----------------------- PID Control Messages ------------------------------

TX_MSG_SEND_PID_BASE = 0x1000

TX_MSG_SEND_PID      = TX_MSG_SEND_PID_BASE+0
TX_MSG_SEND_PID_GAIN = TX_MSG_SEND_PID_BASE+1

#--------------------- Outgoing Controller Mode Messages --------------------

TX_MSG_SET_MODE_BASE = 0x2000

TX_MSG_SET_IDLE_MODE            = TX_MSG_SET_MODE_BASE+0
TX_MSG_SET_MANUAL_MODE          = TX_MSG_SET_MODE_BASE+1
TX_MSG_SET_PID_MODE             = TX_MSG_SET_MODE_BASE+2
TX_MSG_SET_STATE_SPACE_MODE     = TX_MSG_SET_MODE_BASE+3
TX_MSG_SET_AD_HOC_MODE          = TX_MSG_SET_MODE_BASE+4
TX_MSG_SET_AI_MODE              = TX_MSG_SET_MODE_BASE+5
TX_MSG_SET_PENDULUM_PERIOD_MODE = TX_MSG_SET_MODE_BASE+6
TX_MSG_SET_PENDULUM_LENGTH_MODE = TX_MSG_SET_MODE_BASE+7
TX_MSG_SET_RAIL_LENGTH_MODE     = TX_MSG_SET_MODE_BASE+8
TX_MSG_SET_RAIL_CENTER_MODE     = TX_MSG_SET_MODE_BASE+9
TX_MSG_SET_WINDUP_MODE          = TX_MSG_SET_MODE_BASE+10
TX_MSG_SET_COMM_TEST_MODE       = TX_MSG_SET_MODE_BASE+11

mode_messages = { 'Idle'                   : TX_MSG_SET_IDLE_MODE,
                  'Manual'                 : TX_MSG_SET_MANUAL_MODE,
                  'PID Controller'         : TX_MSG_SET_PID_MODE,
                  'State Space Controller' : TX_MSG_SET_STATE_SPACE_MODE,
                  'Ad Hoc Controller'      : TX_MSG_SET_AD_HOC_MODE,
                  'AI Controller'          : TX_MSG_SET_AI_MODE,
                  'Pendulum Period Test'   : TX_MSG_SET_PENDULUM_PERIOD_MODE,
                  'Pendulum Length Test'   : TX_MSG_SET_PENDULUM_LENGTH_MODE,
                  'Rail Length Test'       : TX_MSG_SET_RAIL_LENGTH_MODE,
                  'Rail Center Test'       : TX_MSG_SET_RAIL_CENTER_MODE,
                  'Windup Test'            : TX_MSG_SET_WINDUP_MODE,
                  'Communications Test'    : TX_MSG_SET_COMM_TEST_MODE     
                }

#------------------------- Manual Control Messages ----------------------

TX_MSG_MANUAL_CONTROL_BASE = 0x3000

TX_MSG_MANUAL_CONTROL_JOG_LEFT    = TX_MSG_MANUAL_CONTROL_BASE+0
TX_MSG_MANUAL_CONTROL_JOG_RIGHT   = TX_MSG_MANUAL_CONTROL_BASE+1
TX_MSG_MANUAL_CONTROL_LEFT_HOME   = TX_MSG_MANUAL_CONTROL_BASE+2
TX_MSG_MANUAL_CONTROL_CENTER_HOME = TX_MSG_MANUAL_CONTROL_BASE+3
TX_MSG_MANUAL_CONTROL_RIGHT_HOME  = TX_MSG_MANUAL_CONTROL_BASE+4
TX_MSG_MANUAL_CONTROL_JOG_SIZE    = TX_MSG_MANUAL_CONTROL_BASE+5

#------------------------- Received Messages ---------------------------

RX_MSG_BASE = 0x4000



#********************************************************************************************************


class WidgetGallery(QDialog):


    def __init__(self, parent=None):


        super(WidgetGallery, self).__init__(parent)

        host = "192.168.6.2"
        port = 6666

        self.sock = socket.socket()
        self.sock.connect((host,port))

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.__createIncomingGroupBox()
        self.__createOutgoingGroupBox()
        self.__createModeGroupBox()
        self.__createManualGroupBox()
        self.__createPIDGroupBox()


        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()

        mainLayout.addLayout(topLayout, 0, 0, 1, 2)

        mainLayout.addWidget(self.modeGroupBox, 1, 0)
        mainLayout.addWidget(self.manualGroupBox, 1, 1)
        mainLayout.addWidget(self.incomingGroupBox, 2, 0)
        mainLayout.addWidget(self.outgoingGroupBox, 2, 1)
        mainLayout.addWidget(self.PIDGroupBox, 1, 2)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("                                Inverted Pendulum Controller")
        self.__changeStyle('Fusion')

        self.gain         = 1.0
        self.proportional = 2.0
        self.integral     = 3.0
        self.derivitive   = 4.0
        self.jog          = 2.0



#********************************************************************************************************

    def putRxConsole(self,text):

        self.incoming.append(text)
        self.incoming.moveCursor(QtGui.QTextCursor.End)


#********************************************************************************************************

    def putTxConsole(self,text):

        self.outgoing.append(text)
        self.outgoing.moveCursor(QtGui.QTextCursor.End)


#********************************************************************************************************

    def __sendControllerMsg(self,message,text,arg1=None,arg2=None,arg3=None,arg4=None):

        dummy = 0.0

        self.putTxConsole(text)
   
        if arg4 != None:

           packet = [message,arg1,arg2,arg3,arg4]
           print ("TX(4) : ",packet)

        elif arg3 != None:

           packet = [message,arg1,arg2,arg3,dummy]
           print ("TX(3) : ",packet)

        elif arg2 != None:

           packet = [message,arg1,arg2,dummy,dummy]
           print ("TX(2) : ",packet)

        elif arg1 != None:

           packet = [message,arg1,dummy,dummy,dummy]
           print ("TX(1) : ",packet)

        else:
           packet = [message,dummy,dummy,dummy,dummy]
           print ("TX(0) : ",packet)


        self.sock.send(msgpack.packb(packet, use_bin_type=True))


#********************************************************************************************************

    def __updatePID(self):

        self.__sendControllerMsg(TX_MSG_SEND_PID,"Send PID Data",self.proportional,self.integral, self.derivitive, self.gain)

#********************************************************************************************************

    def __changeStyle(self, styleName):

        QApplication.setStyle(QStyleFactory.create(styleName))

#********************************************************************************************************

    def __createPIDGroupBox(self):

        self.PIDGroupBox = QGroupBox("PID")


        proportionalButton = QPushButton('Edit Proportional', self)
        proportionalButton.clicked.connect(self.showProportionalDialog)

        integralButton = QPushButton('Edit Integral', self)
        integralButton.clicked.connect(self.showIntegralDialog)

        derivitiveButton = QPushButton('Edit Derivitive', self)
        derivitiveButton.clicked.connect(self.showDerivitiveDialog)
                                                                                        
        gainButton = QPushButton('Edit Gain', self)
        gainButton.clicked.connect(self.showGainDialog)

        PIDButton = QPushButton('Update', self)
        PIDButton.clicked.connect(self.__updatePID)
                                                                                        
        layout = QVBoxLayout()

        layout.addWidget(proportionalButton)
        layout.addWidget(integralButton)
        layout.addWidget(derivitiveButton)
        layout.addWidget(gainButton)
        layout.addWidget(PIDButton)
 
        layout.addStretch(1)

        self.PIDGroupBox.setLayout(layout)    

#********************************************************************************************************

    def showGainDialog(self):

        scratchpad, ok = QInputDialog.getDouble(self, 'Gain', '',self.gain)

        if ok == True:
           self.gain = scratchpad

#********************************************************************************************************

    def showProportionalDialog(self):

       scratchpad, ok = QInputDialog.getDouble(self, 'Proportional', '',self.proportional)

       if ok == True:
           self.proportional = scratchpad

#********************************************************************************************************

    def showIntegralDialog(self):

         scratchpad, ok = QInputDialog.getDouble(self, 'Integral', '',self.integral)

         if ok == True:
            self.integral = scratchpad

#********************************************************************************************************

    def showDerivitiveDialog(self):

         scratchpad, ok = QInputDialog.getDouble(self, 'Derivitive', '',self.derivitive)

         if ok == True:
             self.derivitive = scratchpad

#********************************************************************************************************

    def __createModeGroupBox(self):

        self.modeGroupBox = QGroupBox("Mode")

        idleRadioButton            = QRadioButton("Idle")
        manualRadioButton          = QRadioButton("Manual")
        pidRadioButton             = QRadioButton("PID Controller")
        stateSpaceRadioButton      = QRadioButton("State Space Controller")
        adHocRadioButton           = QRadioButton("Ad Hoc Controller")
        aiRadioButton              = QRadioButton("AI Controller")
        periodRadioButton          = QRadioButton("Pendulum Period Test")
        pendulumLengthRadioButton  = QRadioButton("Pendulum Length Test")
        railLengthRadioButton      = QRadioButton("Rail Length Test")
        centerRadioButton          = QRadioButton("Rail Center Test")
        windupRadioButton          = QRadioButton("Windup Test")
        commTestRadioButton        = QRadioButton("Communications Test")

        idleRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(idleRadioButton))
        manualRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(manualRadioButton))
        pidRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(pidRadioButton))
        stateSpaceRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(stateSpaceRadioButton))
        adHocRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(adHocRadioButton))
        aiRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(aiRadioButton))
        periodRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(periodRadioButton))
        pendulumLengthRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(pendulumLengthRadioButton))
        railLengthRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(railLengthRadioButton))
        centerRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(centerRadioButton))
        windupRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(windupRadioButton))
        commTestRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(commTestRadioButton))

        idleRadioButton.setChecked(True)

        layout = QVBoxLayout()

        layout.addWidget(idleRadioButton)
        layout.addWidget(manualRadioButton)
        layout.addWidget(pidRadioButton)
        layout.addWidget(stateSpaceRadioButton)
        layout.addWidget(adHocRadioButton)
        layout.addWidget(aiRadioButton)
        layout.addWidget(periodRadioButton)
        layout.addWidget(pendulumLengthRadioButton)
        layout.addWidget(railLengthRadioButton)
        layout.addWidget(centerRadioButton)
        layout.addWidget(windupRadioButton)
        layout.addWidget(commTestRadioButton)

        layout.addStretch(1)

        self.modeGroupBox.setLayout(layout)    

#********************************************************************************************************

    def modeRadioButtonHandler(self,radio):


        if radio.isChecked():

           mode = mode_messages.get(radio.text())

           if mode != None:
              self.__sendControllerMsg(mode,radio.text())
           else: 
              print("Undefined mode message string: " + radio.text())
 
           

#********************************************************************************************************

    def __createManualGroupBox(self):

        self.manualGroupBox = QGroupBox("Manual Controls")

        leftHomePushButton = QPushButton("Left Home")
        leftHomePushButton.setCheckable(True)

        centerHomePushButton = QPushButton("Center Home")
        centerHomePushButton.setCheckable(True)

        rightHomePushButton = QPushButton("Right Home")
        rightHomePushButton.setCheckable(True)

        jogLeftPushButton = QPushButton("Jog Left")
        jogLeftPushButton.setCheckable(True)

        jogRightPushButton = QPushButton("Jog Right")
        jogRightPushButton.setCheckable(True)

        jogLeftPushButton.toggled.connect(lambda:self.jogLeftHandler())
        jogRightPushButton.toggled.connect(lambda:self.jogRightHandler())
        leftHomePushButton.toggled.connect(lambda:self.leftHomeHandler())
        rightHomePushButton.toggled.connect(lambda:self.rightHomeHandler())
        centerHomePushButton.toggled.connect(lambda:self.centerHomeHandler())
                                                                                        
        jogSizeButton = QPushButton('Edit Jog Size', self)
        jogSizeButton.clicked.connect(self.showJogSizeDialog)

        layout = QVBoxLayout()

        layout.addWidget(leftHomePushButton)
        layout.addWidget(centerHomePushButton)
        layout.addWidget(rightHomePushButton)
        layout.addWidget(jogLeftPushButton)
        layout.addWidget(jogRightPushButton)
        layout.addWidget(jogSizeButton)

        layout.addStretch(1)

        self.manualGroupBox.setLayout(layout)

#********************************************************************************************************

    def showJogSizeDialog(self):

         scratchpad, ok = QInputDialog.getDouble(self, 'Jog Size', '',self.jog)
         
         if ok == True and scratchpad > 0.0:
            self.jog = scratchpad
            self.__sendControllerMsg(TX_MSG_MANUAL_CONTROL_JOG_SIZE,"Update Jog Size",self.jog)

#***************************************************************************************

    def jogLeftHandler(self):

       self.__sendControllerMsg(TX_MSG_MANUAL_CONTROL_JOG_LEFT,"Jog Left")


#***************************************************************************************

    def jogRightHandler(self):

       self.__sendControllerMsg(TX_MSG_MANUAL_CONTROL_JOG_RIGHT,"Jog Right")

#***************************************************************************************

    def leftHomeHandler(self):

       self.__sendControllerMsg(TX_MSG_MANUAL_CONTROL_LEFT_HOME,"Left Home")


#***************************************************************************************

    def centerHomeHandler(self):

       self.__sendControllerMsg(TX_MSG_MANUAL_CONTROL_CENTER_HOME,"Center Home")

#***************************************************************************************

    def rightHomeHandler(self):

       self.__sendControllerMsg(TX_MSG_MANUAL_CONTROL_RIGHT_HOME,"Right Home")

#***************************************************************************************

    def __createIncomingGroupBox(self):

        self.incomingGroupBox = QGroupBox("Incoming Messages")

        self.incoming = QTextEdit()

        layout = QVBoxLayout()

        layout.addWidget(self.incoming)

        self.incomingGroupBox.setLayout(layout)    


#***************************************************************************************

    def __createOutgoingGroupBox(self):

        self.outgoingGroupBox = QGroupBox("Outgoing Messages")

        self.outgoing = QTextEdit()

        layout = QVBoxLayout()

        layout.addWidget(self.outgoing)

        self.outgoingGroupBox.setLayout(layout)



    #***************************************************************************************


if __name__ == '__main__':

    import sys
    import asyncio




    app = QApplication(sys.argv)

    gui = WidgetGallery()

    gui.show()
    gui.putRxConsole("Incoming controller message")

    sys.exit(app.exec_()) 


