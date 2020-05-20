LIBS=robotcontrol
FLAGS=-Wall

controller : controller.o led.o button.o
	g++ -o controller controller.o led.o button.o -l$(LIBS)

controller.o : controller.cpp
	g++ $(FLAGS) -c controller.cpp

led.o : led.cpp
	g++ $(FLAGS) -c led.cpp

button.o : button.cpp
	g++ $(FLAGS) -c button.cpp


clean:
	rm -f *.o 
	rm -f controller
