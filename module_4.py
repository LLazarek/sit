#!/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Gordon Wu
# sit Interactive Testing 

################################################################

#   All Viable Inputs:

# 	INT: 
# 	INT_MAX
# 	INT_MIN
# 	-1
# 	0
# 	1

# 	FLOAT:
# 	FLOAT_MAX
# 	FLOAT_MIN
# 	-1.0
# 	0.0
# 	1.0	

# 	DOUBLE:
# 	DOUBLE_MAX
# 	DOUBLE_MIN
# 	-1.00
# 	0.00
# 	1.00	

# 	CHAR:
# 	BLANK_CHAR (space)
#	CHAR_ALPHA (a,b,c, ...)
#	CHAR_NUM (1,2, ... )
# 	CHAR_CAP_ALPHA (A, B, C, ...)
#	CHAR_ETC ('!', '<', '>', '!', '@', '#', ','' , etc. )

#	STRING: 
#  	BLANK_STRING (empty null ternminated space)
#	- make the user input the random strings

# 	BOOL: 
# 	TRUE 
# 	FALSE 

################################################################

#	interactive: called when >>>test-interactive
#	compares function type with parameter types to let the user 
#	determine values of edge-cases and creates random variables
#	in compliance with the min and max that the user created

import module_1
import sys 
import random

#retrieve the function type and types for params to determine which to use

class int_(type):
	print "Input the values for edge cases and a few random variables: \n"
	INT_MAX = input("Value for INT_MAX: ") 
	INT_MIN = input("Value for INT_MIN: ")
	EDGE_NEG = input("Value for Negative Edge Case: ")
	EDGE_ZERO = input("Value for Edge Case for Zero: ")
	EDGE_ONE = input("Value for Edge Case for One: ")

	#generate some random values within the params of MAX and MIN for user to input
	count = 0 
	while(count < 4):
		RAND_INT = random.randint(INT_MIN,INT_MAX)
		VAL_RAND = input("Value for %d: ") % (RAND_INT)
		list_output[count] = VAL_RAND
		count += 1 

class float_(type):
	print "Input the values for edge cases and a few random variables: \n"
	FLOAT_MAX = input("Value for LOAT_MAX: ") 
	FLOAT_MIN = input("Value for FLOAT_MIN: ")
	EDGE_NEG = input("Value for Negative Edge Case: ")
	EDGE_ZERO = input("Value for Edge Case for Zero: ")
	EDGE_ONE = input("Value for Edge Case for One: ")

	#generate some random values within the params of MAX and MIN for user to input
	count = 0 
	while(count < 4):
		RAND_FLOAT = random.uniform(INT_MIN,INT_MAX)
		VAL_RAND = input("Value for %g: ") % (RAND_FLOAT)
		list_output[count] = VAL_RAND
		count += 1 

class double_(type):
	print "Input the values for edge cases and a few random variables: \n"
	DOUBLE_MAX = input("Value for DOUBLE_MAX: ") 
	DOUBLE_MIN = input("Value for DOUBLE_MIN: ")
	EDGE_NEG = input("Value for Negative Edge Case: ")
	EDGE_ZERO = input("Value for Edge Case for Zero: ")
	EDGE_ONE = input("Value for Edge Case for One: ")

	#generate some random values within the params of MAX and MIN for user to input
	count = 0 
	while(count < 4):
		RAND_DOUBLE = random.randint(INT_MIN,INT_MAX)
		VAL_RAND = input("Value for %s: ") % (RAND_DOUBLE)
		list_output[count] = VAL_RAND
		count += 1 

class char_(type):
	print "Input the values for the cases: \n"
	BLANK_CHAR = input("Value for BLANK_CHAR: ") 
	CHAR_ALPHA = input("Value for CHAR_ALPHA: ") 
	CHAR_CAP_ALPHA = input("Value for CAPS_CHAR_ALPHA: ") 
	CHAR_NUM = input("Value for CHAR_NUM  ") 
	CHAR_ETC = input("Value for CHAR_ETC: ") 

class string_(type): 
	print "Input the values for the cases: \n"
	BLANK_STRING = input("Value for BLANK_STRING: ")

	#let the user input a bunch of random strings 
	count = 0
	while(count < 4):
		USER_STRING  = input("Enter a String: ") 
		list_output[count] = VAL_RAND
		count += 1

class bool_(type):
	print "Input the values for the cases: \n"
	VALUE_TRUE = input("Value for TRUE: ")
	VALUE_FALSE = input("Value for FALSE: ")
