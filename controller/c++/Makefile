LIBS=robotcontrol
FLAGS=-Wall

controller : controller.o led.o button.o encoder.o
	g++ -o controller controller.o led.o button.o encoder.o -l$(LIBS)

controller.o : controller.cpp
	g++ $(FLAGS) -c controller.cpp

led.o : led.cpp
	g++ $(FLAGS) -c led.cpp

button.o : button.cpp
	g++ $(FLAGS) -c button.cpp

encoder.o : encoder.cpp
	g++ $(FLAGS) -c encoder.cpp


clean:
	rm -f *.o 
	rm -f controller



