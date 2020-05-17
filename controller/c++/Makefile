LIBS=robotcontrol

controller : controller.o blink.o
	g++ -o controller controller.o blink.o -l$(LIBS)

controller.o : controller.cpp
	g++ -c controller.cpp

blink.o : blink.c
	g++ -c blink.c


clean:
	rm -f *.o 
	rm -f controller
