CC = g++

Compile: example_code.cpp
	$(CC) example_code.cpp -o test

Sit: sit.py
	python3 sit.py example_code.cpp 
	$(MAKE) Compile

clean:
	rm -f *.o *~ test