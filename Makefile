Compile: example_code_tests.cpp
	g++ example_code_tests.cpp -o test

sit: sit.py
	python3 sit.py example_code.cpp 
	$(MAKE) Compile
