#!/usr/bin/env python3.5


#********************************************************************************************************

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

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

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

#********************************************************************************************************

import msgpack
import socket
from Messages import controllerMsgs
from random import randint
import sys
import asyncio

#********************************************************************************************************

mode_messages = { 'Idle'                   : controllerMsgs.TX_MSG_SET_IDLE_MODE,
                  'Manual'                 : controllerMsgs.TX_MSG_SET_MANUAL_MODE,
                  'State Space Controller' : controllerMsgs.TX_MSG_SET_STATE_SPACE_MODE,
                  'PID Controller'         : controllerMsgs.TX_MSG_SET_PID_MODE,
                  'Fuzzy Logic Controller' : controllerMsgs.TX_MSG_SET_FUZZY_LOGIC_MODE,
                  'AI Controller'          : controllerMsgs.TX_MSG_SET_AI_MODE,
                  'Pendulum Period Test'   : controllerMsgs.TX_MSG_SET_PENDULUM_PERIOD_MODE,
                  'Pendulum Length Test'   : controllerMsgs.TX_MSG_SET_PENDULUM_LENGTH_MODE,
                  'Rail Length Test'       : controllerMsgs.TX_MSG_SET_RAIL_LENGTH_MODE,
                  'Rail Center Test'       : controllerMsgs.TX_MSG_SET_RAIL_CENTER_MODE,
                  'Windup Test'            : controllerMsgs.TX_MSG_SET_WINDUP_MODE,
                  'Communications Test'    : controllerMsgs.TX_MSG_SET_COMM_TEST_MODE,
                }

#********************************************************************************************************


class WidgetGallery(QDialog):


    def __init__(self, parent=None):


        super(WidgetGallery, self).__init__(parent)

        self.simulate     = True
        self.host         = "192.168.6.2"
        self.port         = 6666
        self.interval     = 50
        self.gain         = 1.0
        self.proportional = 2.0
        self.integral     = 3.0
        self.derivitive   = 4.0
        self.jog          = 2.0
        self.buffer_size  = 200
        self.plot_width   = 1
        self.mode         = controllerMsgs.TX_MSG_SET_IDLE_MODE

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
        self.__createAngleSensorGroupBox()

        self.__createLinearPositionPlotGroupBox()
        self.__createLinearVelocityPlotGroupBox()

        self.__createAngularPositionPlotGroupBox()
        self.__createAngularVelocityPlotGroupBox()

        top = QHBoxLayout()
        top.addStretch(1)

        main = QGridLayout()

        main.addLayout(top, 0, 0, 1, 4)

        main.addWidget(self.modeGroupBox,                1, 0)
        main.addWidget(self.manualGroupBox,              1, 1)
        main.addWidget(self.PIDGroupBox,                 1, 2)
        main.addWidget(self.linearPositionPlotGroupBox,  1, 3)
        main.addWidget(self.angularPositionPlotGroupBox, 1, 4)

        main.addWidget(self.incomingGroupBox,            2, 0)
        main.addWidget(self.outgoingGroupBox,            2, 1)
        main.addWidget(self.angleSensorGroupBox,         2, 2)
        main.addWidget(self.linearVelocityPlotGroupBox,  2, 3)
        main.addWidget(self.angularVelocityPlotGroupBox, 2, 4)

        main.setRowStretch(1, 1)
        main.setRowStretch(2, 1)
        main.setColumnStretch(0, 1)
        main.setColumnStretch(1, 1)

        self.setLayout(main)

        self.setWindowTitle("Inverted Pendulum Controller")

        self.__changeStyle('Fusion')

        if self.simulate == True:
           self.timer = QtCore.QTimer()
           self.timer.setInterval(self.interval)
           self.timer.timeout.connect(self.update_plots)
           self.timer.start()
        else:
           self.sock = socket.socket()
           self.sock.connect((self.host,self.port))

#********************************************************************************************************

    def update_plots(self):

       if self.mode  == controllerMsgs.TX_MSG_SET_PID_MODE:

            self.angularPositionY = self.angularPositionY[1:] 
            self.angularPositionY.append( randint(0,self.buffer_size))  

            self.linearPositionY = self.linearPositionY[1:] 
            self.linearPositionY.append( randint(0,self.buffer_size))  

            self.linearVelocityY = self.linearVelocityY[1:]   
            self.linearVelocityY.append(randint(0,self.buffer_size))  

            self.angularVelocityY = self.angularVelocityY[1:]   
            self.angularVelocityY.append(randint(0,self.buffer_size))  

            self.angularPositionPlotUpdate.setData(self.angularPositionX, self.angularPositionY) 
            self.linearPositionPlotUpdate.setData(self.linearPositionX,self.linearPositionY)

            self.linearVelocityPlotUpdate.setData (self.linearVelocityX, self.linearVelocityY)
            self.angularVelocityPlotUpdate.setData (self.angularVelocityX, self.angularVelocityY)

#********************************************************************************************************

    def putRxDebugConsole(self,text):

        self.incoming.append(text)
        self.incoming.moveCursor(QtGui.QTextCursor.End)


#********************************************************************************************************

    def putTxDebugConsole(self,text):

        self.outgoing.append(text)
        self.outgoing.moveCursor(QtGui.QTextCursor.End)


#********************************************************************************************************

    def __sendControllerMsg(self,message,text,arg1=None,arg2=None,arg3=None,arg4=None):

        dummy = 0.0

        self.putTxDebugConsole(text)
   
        if arg4 != None:

           packet = [message,arg1,arg2,arg3,arg4]

        elif arg3 != None:

           packet = [message,arg1,arg2,arg3,dummy]

        elif arg2 != None:

           packet = [message,arg1,arg2,dummy,dummy]

        elif arg1 != None:

           packet = [message,arg1,dummy,dummy,dummy]

        else:
           packet = [message,dummy,dummy,dummy,dummy]


        if self.simulate == False:
           self.sock.send(msgpack.packb(packet))


#********************************************************************************************************

    def __updatePID(self):

        self.__sendControllerMsg(controllerMsgs.TX_MSG_SEND_PID,"Send PID Data",self.proportional,self.integral, self.derivitive, self.gain)

#********************************************************************************************************

    def __changeStyle(self, styleName):

        QApplication.setStyle(QStyleFactory.create(styleName))

#********************************************************************************************************

    def __createPIDGroupBox(self):

        self.PIDGroupBox = QGroupBox("PID")

        self.PIDGroupBox.setAlignment(Qt.AlignCenter)

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

    def angleSensorRadioButtonHandler(self,radio):

        if radio.isChecked():

           if radio.text() == "Rotary Encoder":
              self.__sendControllerMsg(controllerMsgs.TX_MSG_USE_ROTARY_ENCODER,radio.text())
           elif radio.text() == "Accelerometer":
              self.__sendControllerMsg(controllerMsgs.TX_MSG_USE_ACCELEROMETER,radio.text())
           else: 
              print("Undefined angle sensor message string: " + radio.text())
 

#********************************************************************************************************

    def __createAngleSensorGroupBox(self):

        self.angleSensorGroupBox = QGroupBox("Pendulum Angle Sensor")

        self.angleSensorGroupBox.setAlignment(Qt.AlignCenter)

        accelerometerRadioButton = QRadioButton("Accelerometer")
        rotaryEncoderRadioButton = QRadioButton("Rotary Encoder")


        actor = lambda:self.angleSensorRadioButtonHandler(accelerometerRadioButton)
        accelerometerRadioButton.toggled.connect(actor)

        actor = lambda:self.angleSensorRadioButtonHandler(rotaryEncoderRadioButton)
        rotaryEncoderRadioButton.toggled.connect(actor)

        rotaryEncoderRadioButton.setChecked(True)

        layout = QVBoxLayout()

        layout.addWidget(rotaryEncoderRadioButton)
        layout.addWidget(accelerometerRadioButton)


        layout.addStretch(1)

        self.angleSensorGroupBox.setLayout(layout)  

#********************************************************************************************************

    def __createModeGroupBox(self):

        self.modeGroupBox = QGroupBox("Mode")

        self.modeGroupBox.setAlignment(Qt.AlignCenter)

        idleRadioButton            = QRadioButton("Idle")
        manualRadioButton          = QRadioButton("Manual")
        pidRadioButton             = QRadioButton("PID Controller")
        stateSpaceRadioButton      = QRadioButton("State Space Controller")
        aiRadioButton              = QRadioButton("AI Controller")
        periodRadioButton          = QRadioButton("Pendulum Period Test")
        pendulumLengthRadioButton  = QRadioButton("Pendulum Length Test")
        railLengthRadioButton      = QRadioButton("Rail Length Test")
        centerRadioButton          = QRadioButton("Rail Center Test")
        windupRadioButton          = QRadioButton("Windup Test")
        commTestRadioButton        = QRadioButton("Communications Test")

        actor = lambda:self.modeRadioButtonHandler(idleRadioButton)
        idleRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(manualRadioButton)
        manualRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(pidRadioButton)
        pidRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(stateSpaceRadioButton)
        stateSpaceRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(aiRadioButton)
        aiRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(periodRadioButton)
        periodRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(pendulumLengthRadioButton)
        pendulumLengthRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(railLengthRadioButton)
        railLengthRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(centerRadioButton)
        centerRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(windupRadioButton)
        windupRadioButton.toggled.connect(actor)

        actor = lambda:self.modeRadioButtonHandler(commTestRadioButton)
        commTestRadioButton.toggled.connect(actor)

        idleRadioButton.setChecked(True)

        layout = QVBoxLayout()

        layout.addWidget(idleRadioButton)
        layout.addWidget(manualRadioButton)
        layout.addWidget(pidRadioButton)
        layout.addWidget(stateSpaceRadioButton)
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

           msg = mode_messages.get(radio.text())

           if msg == None:
              print("Undefined mode message string: " + radio.text())

           else: 
              self.mode = msg
              self.__sendControllerMsg(msg,radio.text())
 
           

#********************************************************************************************************

    def __createManualGroupBox(self):

        self.manualGroupBox = QGroupBox("Manual Controls")

        self.manualGroupBox.setAlignment(Qt.AlignCenter)

        leftParkPushButton = QPushButton("Left Park")
        leftParkPushButton.setCheckable(True)

        centerParkPushButton = QPushButton("Center Park")
        centerParkPushButton.setCheckable(True)

        rightParkPushButton = QPushButton("Right Park")
        rightParkPushButton.setCheckable(True)

        jogLeftPushButton = QPushButton("Jog Left")
        jogLeftPushButton.setCheckable(True)

        jogRightPushButton = QPushButton("Jog Right")
        jogRightPushButton.setCheckable(True)

        actor = lambda:self.jogLeftHandler()
        jogLeftPushButton.toggled.connect(actor)

        actor = lambda:self.jogRightHandler()
        jogRightPushButton.toggled.connect(actor)

        actor = lambda:self.leftParkHandler()
        leftParkPushButton.toggled.connect(actor)

        actor = lambda:self.rightParkHandler()
        rightParkPushButton.toggled.connect(actor)

        actor = lambda:self.centerParkHandler()
        centerParkPushButton.toggled.connect(actor)
                                                                                        
        jogSizeButton = QPushButton('Edit Jog Size', self)
        jogSizeButton.clicked.connect(self.showJogSizeDialog)

        layout = QVBoxLayout()

        layout.addWidget(leftParkPushButton)
        layout.addWidget(centerParkPushButton)
        layout.addWidget(rightParkPushButton)
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
            self.__sendControllerMsg(controllerMsgs.TX_MSG_MANUAL_CONTROL_JOG_SIZE,"Update Jog Size",self.jog)

#***************************************************************************************

    def jogLeftHandler(self):

       if self.mode == controllerMsgs.TX_MSG_SET_MANUAL_MODE:
          self.__sendControllerMsg(controllerMsgs.TX_MSG_MANUAL_CONTROL_JOG_LEFT,"Jog Left")


#***************************************************************************************

    def jogRightHandler(self):

       if self.mode == controllerMsgs.TX_MSG_SET_MANUAL_MODE:
           self.__sendControllerMsg(controllerMsgs.TX_MSG_MANUAL_CONTROL_JOG_RIGHT,"Jog Right")

#***************************************************************************************

    def leftParkHandler(self):

       if self.mode == controllerMsgs.TX_MSG_SET_MANUAL_MODE:
           self.__sendControllerMsg(controllerMsgs.TX_MSG_MANUAL_CONTROL_LEFT_PARK,"Left Park")


#***************************************************************************************

    def centerParkHandler(self):

       if self.mode == controllerMsgs.TX_MSG_SET_MANUAL_MODE:
           self.__sendControllerMsg(controllerMsgs.TX_MSG_MANUAL_CONTROL_CENTER_PARK,"Center Park")

#***************************************************************************************

    def rightParkHandler(self):

       if self.mode == controllerMsgs.TX_MSG_SET_MANUAL_MODE:
           self.__sendControllerMsg(controllerMsgs.TX_MSG_MANUAL_CONTROL_RIGHT_PARK,"Right Park")

#***************************************************************************************

    def __createIncomingGroupBox(self):

        self.incomingGroupBox = QGroupBox("Incoming Messages")

        self.incomingGroupBox.setAlignment(Qt.AlignCenter)

        self.incoming = QTextEdit()

        layout = QVBoxLayout()

        layout.addWidget(self.incoming)

        self.incomingGroupBox.setLayout(layout)    



#***************************************************************************************

    def __createOutgoingGroupBox(self):

        self.outgoingGroupBox = QGroupBox("Outgoing Messages")

        self.outgoingGroupBox.setAlignment(Qt.AlignCenter)

        self.outgoing = QTextEdit()

        layout = QVBoxLayout()

        layout.addWidget(self.outgoing)

        self.outgoingGroupBox.setLayout(layout)

#***************************************************************************************

    def __createLinearPositionPlotGroupBox(self):

        self.linearPositionPlotGroupBox = QGroupBox("Linear Position")

        self.linearPositionPlotGroupBox.setAlignment(Qt.AlignCenter)

        widget = pg.PlotWidget()

        layout = QVBoxLayout()

        layout.addWidget(widget)

        self.linearPositionPlotGroupBox.setLayout(layout)

        self.linearPositionX = list(range(-self.buffer_size*self.interval,0,self.interval))  
        self.linearPositionY = [randint(0,self.buffer_size) for _ in range(0,self.buffer_size*self.interval,self.interval)] 

        pen = pg.mkPen(color=(255, 0, 0),width=self.plot_width)
        widget.setBackground('w')

        widget.setYRange(-750, 750, padding=0)

        widget.setLabel('left', 'Millimeters', color='red', size=30)
        widget.setLabel('bottom', 'Milliseconds', color='red', size=30)

        self.linearPositionPlotUpdate = widget.plot(self.linearPositionX, self.linearPositionY,pen=pen)


#***************************************************************************************

    def __createAngularPositionPlotGroupBox(self):

        self.angularPositionPlotGroupBox = QGroupBox("Angular Position")

        self.angularPositionPlotGroupBox.setAlignment(Qt.AlignCenter)


        widget = pg.PlotWidget()
        layout = QVBoxLayout()

        layout.addWidget(widget)

        self.angularPositionPlotGroupBox.setLayout(layout)

        self.angularPositionX = list(range(-self.buffer_size*self.interval,0,self.interval))  
        self.angularPositionY = [randint(-180,180) for _ in range(0,self.buffer_size*self.interval,self.interval)]  

        pen = pg.mkPen(color=(255, 0, 0),width=self.plot_width)

        widget.setBackground('w')

        widget.setYRange(-180, 180, padding=0)

        widget.setLabel('left', 'Degrees', color='red', size=30)
        widget.setLabel('bottom', 'Milliseconds', color='red', size=30)

        self.angularPositionPlotUpdate = widget.plot(self.angularPositionX, self.angularPositionY,pen=pen)

#***************************************************************************************

    def __createAngularVelocityPlotGroupBox(self):

        self.angularVelocityPlotGroupBox = QGroupBox("Angular Velocity")
        self.angularVelocityPlotGroupBox.setAlignment(Qt.AlignCenter)

        widget = pg.PlotWidget()

        layout = QVBoxLayout()

        layout.addWidget(widget)

        self.angularVelocityPlotGroupBox.setLayout(layout)

        self.angularVelocityX = list(range(-self.buffer_size*self.interval,0,self.interval))  
        self.angularVelocityY = [randint(-180,180) for _ in range(0,self.buffer_size*self.interval,self.interval)]  

        pen = pg.mkPen(color=(255, 0, 0),width=self.plot_width)

        widget.setBackground('w')

        widget.setYRange(-180, 180, padding=0)

        widget.setLabel('left', 'Degrees/Second', color='red', size=30)
        widget.setLabel('bottom', 'Milliseconds', color='red', size=30)

        self.angularVelocityPlotUpdate = widget.plot(self.angularVelocityX, self.angularVelocityY,pen=pen)

#***************************************************************************************

    def __createAngularPlotsGroupBox(self):
        stub = True

#***************************************************************************************

    def __createLinearPlotsGroupBox(self):
        stub = True

#***************************************************************************************

    def __createLinearVelocityPlotGroupBox(self):

        self.linearVelocityPlotGroupBox = QGroupBox("Linear Velocity")
        self.linearVelocityPlotGroupBox.setAlignment(Qt.AlignCenter)

        widget = pg.PlotWidget()

        layout = QVBoxLayout()

        layout.addWidget(widget)

        self.linearVelocityPlotGroupBox.setLayout(layout)

        self.linearVelocityX = list(range(-self.buffer_size*self.interval,0,self.interval))  
        self.linearVelocityY = [randint(-180,180) for _ in range(0,self.buffer_size*self.interval,self.interval)]  

        pen = pg.mkPen(color=(255, 0, 0),width=self.plot_width)

        widget.setBackground('w')

        widget.setLabel('left', 'Millimeters/Second', color='red', size=30)
        widget.setLabel('bottom', 'Milliseconds', color='red', size=30)

        self.linearVelocityPlotUpdate = widget.plot(self.linearVelocityX, self.linearVelocityY,pen=pen)

#***************************************************************************************


if __name__ == '__main__':


    app = QApplication(sys.argv)

    gui = WidgetGallery()

    gui.show()
    gui.putRxDebugConsole("Incoming controller message")

    sys.exit(app.exec_()) 


