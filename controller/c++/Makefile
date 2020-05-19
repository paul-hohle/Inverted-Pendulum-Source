LIBS=robotcontrol
FLAGS=-Wall

controller : controller.o blink.o led.o
	g++ -o controller controller.o blink.o -l$(LIBS)

controller.o : controller.cpp
	g++ $(FLAGS) -c controller.cpp

blink.o : blink.c
	g++ $(FLAGS) -c blink.c

led.o : led.cpp
	g++ $(FLAGS) -c led.cpp


clean:
	rm -f *.o 
	rm -f controller
