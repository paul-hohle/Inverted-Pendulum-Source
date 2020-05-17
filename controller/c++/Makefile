LIBS=robotcontrol
FLAGS=-Wall

controller : controller.o blink.o
	g++ -o controller controller.o blink.o -l$(LIBS)

controller.o : controller.cpp
	g++ $(FLAGS) -c controller.cpp

blink.o : blink.c
	g++ $(FLAGS) -c blink.c


clean:
	rm -f *.o 
	rm -f controller
