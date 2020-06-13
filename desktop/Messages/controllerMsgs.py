TX_MSG_GENERAL_BASE = 0

TX_MSG_RESET         = TX_MSG_GENERAL_BASE+0
TX_MSG_INIT          = TX_MSG_GENERAL_BASE+1
TX_MSG_SHUTDOWN      = TX_MSG_GENERAL_BASE+2
TX_MSG_PANIC         = TX_MSG_GENERAL_BASE+3

#----------------------- PID Control Messages ------------------------------

TX_MSG_SEND_PID_BASE = 0x1000

TX_MSG_SEND_PID      = TX_MSG_SEND_PID_BASE+0
TX_MSG_SEND_PID_GAIN = TX_MSG_SEND_PID_BASE+1


#----------------------- Manual Control Messages --------------------------

TX_MSG_MANUAL_CONTROL_BASE = 0x3000

TX_MSG_MANUAL_CONTROL_JOG_LEFT    = TX_MSG_MANUAL_CONTROL_BASE+0
TX_MSG_MANUAL_CONTROL_JOG_RIGHT   = TX_MSG_MANUAL_CONTROL_BASE+1
TX_MSG_MANUAL_CONTROL_LEFT_PARK   = TX_MSG_MANUAL_CONTROL_BASE+2
TX_MSG_MANUAL_CONTROL_CENTER_PARK = TX_MSG_MANUAL_CONTROL_BASE+3
TX_MSG_MANUAL_CONTROL_RIGHT_PARK  = TX_MSG_MANUAL_CONTROL_BASE+4
TX_MSG_MANUAL_CONTROL_JOG_SIZE    = TX_MSG_MANUAL_CONTROL_BASE+5

#-------------------- Angle Sensor Control Messages ----------------------

TX_MSG_ANGLE_SENSOR_BASE = 0x4000

TX_MSG_USE_ROTARY_ENCODER = TX_MSG_ANGLE_SENSOR_BASE+0
TX_MSG_USE_ACCELEROMETER  = TX_MSG_ANGLE_SENSOR_BASE+1

#------------------------- Received Messages ---------------------------


RX_MSG_BASE = 0x5000

#--------------------- Outgoing Controller Mode Messages --------------------

TX_MSG_SET_MODE_BASE = 0x2000

TX_MSG_SET_IDLE_MODE            = TX_MSG_SET_MODE_BASE+0x00
TX_MSG_SET_MANUAL_MODE          = TX_MSG_SET_MODE_BASE+0x01
TX_MSG_SET_PID_MODE             = TX_MSG_SET_MODE_BASE+0x02
TX_MSG_SET_LQR_MODE             = TX_MSG_SET_MODE_BASE+0x03
TX_MSG_SET_AI_MODE              = TX_MSG_SET_MODE_BASE+0x04
TX_MSG_SET_FUZZY_LOGIC_MODE     = TX_MSG_SET_MODE_BASE+0x05
TX_MSG_SET_PENDULUM_PERIOD_MODE = TX_MSG_SET_MODE_BASE+0x06
TX_MSG_SET_PENDULUM_LENGTH_MODE = TX_MSG_SET_MODE_BASE+0x07
TX_MSG_SET_RAIL_LENGTH_MODE     = TX_MSG_SET_MODE_BASE+0x08
TX_MSG_SET_RAIL_CENTER_MODE     = TX_MSG_SET_MODE_BASE+0x09
TX_MSG_SET_WINDUP_MODE          = TX_MSG_SET_MODE_BASE+0x0a
TX_MSG_SET_COMM_TEST_MODE       = TX_MSG_SET_MODE_BASE+0x0b
TX_MSG_SET_STRESS_TEST_MODE     = TX_MSG_SET_MODE_BASE+0x0a

