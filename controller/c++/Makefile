ifeq (${shell uname -p},x86_64)

ARM=/home/paul/cross/armv7l
INC=${ARM}/usr/local/include

LROBOT=-l:librobotcontrol.so.1
LROBOT_DIR=${ARM}/usr/local/lib
LFLAGS= -lnng -lm -lrt -pthread -L $(LROBOT_DIR) ${LROBOT}

INC=/home/paul/cross/armv7l/usr/local/include
LIB_PATH=/home/paul/cross/armv7l/usr/local/lib
CC_FLAGS=-Wall -I$(INC) 
LINK_FLAGS=-L$(LIB_PATH) -l$(LIBS)
XCC=arm-g++
CFLAGS=-Wall -I$(INC) 
XCC=${ARM}/bin/arm-linux-gnueabihf-g++ 

else

LFLAGS= -lnng -lm -pthread
CFLAGS=-Wall 
XCC=g++

endif

#**********************************************************************************************************************


controller : controller.o led.o button.o encoder.o stepper.o accelerometer.o net.o
	$(XCC) -o controller net.o controller.o led.o button.o encoder.o stepper.o accelerometer.o ${LFLAGS}

ifeq (${shell uname -p},x86_64)
	cp controller ~/mnt/bb
endif

controller.o : controller.cpp
	$(XCC)  $(CFLAGS) -c controller.cpp

led.o : led.cpp
	$(XCC) $(CFLAGS) -c led.cpp

button.o : button.cpp
	$(XCC) $(CFLAGS) -c button.cpp

encoder.o : encoder.cpp
	$(XCC) $(CFLAGS) -c encoder.cpp

accelerometer.o : accelerometer.cpp
	$(XCC) $(CFLAGS) -c accelerometer.cpp

stepper.o : stepper.cpp
	$(XCC) $(CFLAGS) -c stepper.cpp

net.o	 : net.cpp
	$(XCC) $(CFLAGS) -c net.cpp

ifeq (${shell uname -p},x86_64)

upload-all:
	cp * ~/mnt/bb/build/Inverted-Pendulum-Source/controller/c++

upload-bin:
	cp controller ~/mnt/bb/build/Inverted-Pendulum-Source/controller/c++

endif


clean:
	rm -f *.o 
	rm -f controller

all:
