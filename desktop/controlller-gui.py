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

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

#********************************************************************************************************

import msgpack
import socket
from Messages import controllerMsgs
from random import randint

#********************************************************************************************************


mode_messages = { 'Idle'                   : controllerMsgs.TX_MSG_SET_IDLE_MODE,
                  'Manual'                 : controllerMsgs.TX_MSG_SET_MANUAL_MODE,
                  'PID Controller'         : controllerMsgs.TX_MSG_SET_PID_MODE,
                  'State Space Controller' : controllerMsgs.TX_MSG_SET_STATE_SPACE_MODE,
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

        self.interval     = 50
        self.simulate     = True
        self.gain         = 1.0
        self.proportional = 2.0
        self.integral     = 3.0
        self.derivitive   = 4.0
        self.jog          = 2.0
        self.buffer_size  = 100
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
        self.__createSliderPlotGroupBox()
        self.__createAnglePlotGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()

        mainLayout.addLayout(topLayout, 0, 0, 1, 3)

        mainLayout.addWidget(self.modeGroupBox, 1, 0)
        mainLayout.addWidget(self.manualGroupBox, 1, 1)
        mainLayout.addWidget(self.incomingGroupBox, 2, 0)
        mainLayout.addWidget(self.outgoingGroupBox, 2, 1)
        mainLayout.addWidget(self.PIDGroupBox, 1, 2)
        mainLayout.addWidget(self.angleSensorGroupBox, 2, 2)
        mainLayout.addWidget(self.anglePlotGroupBox, 2, 3)
        mainLayout.addWidget(self.xPlotGroupBox, 1, 3)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("Inverted Pendulum Controller")

        self.__changeStyle('Fusion')

        if self.simulate == True:
           self.timer = QtCore.QTimer()
           self.ticks = 0
           self.timer.setInterval(self.interval)
           self.timer.timeout.connect(self.update_plot_data)
           self.timer.start()
        else:
           host      = "192.168.6.2"
           port      = 6666
           self.sock = socket.socket()
           self.sock.connect((host,port))

#********************************************************************************************************

    def update_plot_data(self):

        self.angleX = self.angleX[1:]  
        new = self.angleX[-1] + self.interval
        self.angleX.append(new) 

        self.angleY = self.angleY[1:] 
        self.angleY.append( randint(0,self.buffer_size))  

        self.sliderX = self.sliderX[1:]  
        new = self.sliderX[-1] + self.interval
        self.sliderX.append(new) 

        self.sliderY = self.sliderY[1:] 
        self.sliderY.append( randint(0,self.buffer_size))  

        self.anglePlotUpdate.setData(self.angleX, self.angleY) 
        self.sliderPlotUpdate.setData(self.sliderX,self.sliderY)

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


        accelerometerRadioButton.toggled.connect(lambda:self.angleSensorRadioButtonHandler(accelerometerRadioButton))
        rotaryEncoderRadioButton.toggled.connect(lambda:self.angleSensorRadioButtonHandler(rotaryEncoderRadioButton))

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

        idleRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(idleRadioButton))
        manualRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(manualRadioButton))
        pidRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(pidRadioButton))
        stateSpaceRadioButton.toggled.connect(lambda:self.modeRadioButtonHandler(stateSpaceRadioButton))
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

        jogLeftPushButton.toggled.connect(lambda:self.jogLeftHandler())
        jogRightPushButton.toggled.connect(lambda:self.jogRightHandler())
        leftParkPushButton.toggled.connect(lambda:self.leftParkHandler())
        rightParkPushButton.toggled.connect(lambda:self.rightParkHandler())
        centerParkPushButton.toggled.connect(lambda:self.centerParkHandler())
                                                                                        
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

    def __createSliderPlotGroupBox(self):

        self.xPlotGroupBox = QGroupBox("Slide Position")

        self.xPlotGroupBox.setAlignment(Qt.AlignCenter)

        self.graphXWidget = pg.PlotWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.graphXWidget)

        self.xPlotGroupBox.setLayout(layout)

        self.sliderX = list(range(0,self.buffer_size*self.interval,self.interval))  
        self.sliderY = [randint(0,self.buffer_size) for _ in range(0,self.buffer_size*self.interval,self.interval)] 

        pen = pg.mkPen(color=(255, 0, 0),width=2)
        self.graphXWidget.setBackground('w')

        self.graphXWidget.setYRange(-750, 750, padding=0)

        self.graphXWidget.setLabel('left', 'Distance from Center (mm)', color='red', size=30)
        self.graphXWidget.setLabel('bottom', 'Time (ms)', color='red', size=30)

        self.sliderPlotUpdate = self.graphXWidget.plot(self.sliderX, self.sliderY,pen=pen)


#***************************************************************************************

    def __createAnglePlotGroupBox(self):

        self.anglePlotGroupBox = QGroupBox("Angular Deviation")

        self.anglePlotGroupBox.setAlignment(Qt.AlignCenter)

        self.graphAngleWidget = pg.PlotWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.graphAngleWidget)

        self.anglePlotGroupBox.setLayout(layout)

        self.angleX = list(range(0,self.buffer_size*self.interval,self.interval))  
        self.angleY = [randint(-180,180) for _ in range(0,self.buffer_size*self.interval,self.interval)]  

        pen = pg.mkPen(color=(255, 0, 0),width=2)
        self.graphAngleWidget.setBackground('w')

        self.graphAngleWidget.setYRange(-180, 180, padding=0)

        self.graphAngleWidget.setLabel('left', 'Deviation from Vertical (Degrees)', color='red', size=30)
        self.graphAngleWidget.setLabel('bottom', 'Time (ms)', color='red', size=30)

        self.anglePlotUpdate = self.graphAngleWidget.plot(self.angleX, self.angleY,pen=pen)

#***************************************************************************************


if __name__ == '__main__':

    import sys
    import asyncio




    app = QApplication(sys.argv)

    gui = WidgetGallery()

    gui.show()
    gui.putRxDebugConsole("Incoming controller message")

    sys.exit(app.exec_()) 


