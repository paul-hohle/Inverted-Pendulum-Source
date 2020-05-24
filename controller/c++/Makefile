
LIBS=robotcontrol

ifeq (${shell uname -p},x86_64)

ARM=/home/paul/cross/armv7l
INC=${ARM}/usr/local/include

LROBOT_DIR=${ARM}/usr/local/lib
LINK_FLAGS= -lm -lrt -pthread -L $(LROBOT_DIR) -l:librobotcontrol.so.1

CC_FLAGS=-Wall -I$(INC) 
XCC=${ARM}/bin/arm-linux-gnueabihf-g++ 

else

LINK_FLAGS=
CC_FLAGS=-Wall 
XCC=g++

endif



controller : controller.o led.o button.o encoder.o stepper.o accelerometer.o net.o
	$(XCC) -o controller net.o controller.o led.o button.o encoder.o stepper.o accelerometer.o net.o ${LINK_FLAGS}

controller.o : controller.cpp
	$(XCC)  $(CC_FLAGS) -c controller.cpp

led.o : led.cpp
	$(XCC) $(CC_FLAGS) -c led.cpp

button.o : button.cpp
	$(XCC) $(CC_FLAGS) -c button.cpp

encoder.o : encoder.cpp
	$(XCC) $(CC_FLAGS) -c encoder.cpp

accelerometer.o : accelerometer.cpp
	$(XCC) $(CC_FLAGS) -c accelerometer.cpp

stepper.o : stepper.cpp
	$(XCC) $(CC_FLAGS) -c stepper.cpp

net.o	 : net.cpp
	$(XCC) $(CC_FLAGS) -c net.cpp

clean:
	rm -f *.o 
	rm -f controller

all:
