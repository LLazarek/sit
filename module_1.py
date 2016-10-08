#!/bin/python3   
#   parse-grab.txt
#   This file looks for the SIT pattern in a comment above a function
#   @Author Owen McCormack
#   @Date 10/8/16 12:13AM

import sys
import re

# Check for only one input file
if((len(sys.argv) < 2) or (len(sys.argv) > 2)):
    print("Invalid input file")

# Create tuple for pair list
pair_list = [];

# string to hold function signature
funct_sign = ""
# list for each test string
funct_tests = []

# Save filename for a later import
filename = sys.argv[1]

# Open file from command line for reading to parse
with open(filename,"r") as p_file:
    lines = p_file.readlines()

# variable notifies if a test was found
found_test = 0

# iterate over each line for regex
for line in lines:

    # Regex to grab each test
    test_grab = re.search('>>> test(-[^: ]*)?: [\-\w\. ]* @ .*',line)
    inter_grab = re.search('>>> test-interactive',line) 
    input_grab = re.search('>>> test-input: [^@]* @ .*',line)

    # check regex for a function signature, if none keep moving down
    if found_test is 1:
        func_grab = re.search("(([a-zA-Z_]*)? *[a-zA-Z0-9_]+ +[a-zA-Z0-9_]+\(.*\))", line)

        # when the function signature is reached append to tuple list with all tests
        if func_grab is not None:
            funct_sign = func_grab.group(1)
            found_test = 0
            pair_list.append((funct_sign, funct_tests))
            funct_tests[:] = []

    # when a test is found start looking for function signature
    if test_grab is not None:
        funct_tests.append(test_grab.group(0))
        found_test = 1

    # grab interactive test seperately
    if inter_grab is not None:
        funct_tests.append(inter_grab.group(0))
        found_test = 1

    # grab input test seperately
    if input_grab is not None:
        funct_tests.append(input_grab.group(0))
        found_test = 1
print(pair_list)