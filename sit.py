#!/bin/python3

import module_1
import module_2
import module_3

# Parse the code file to obtain the function/test pair list
filename_and_pair_list = module_1.parse_code()
# Convert the plaintext list into list of Tests
test_list = module_2.build_test_list(filename_and_pair_list[1])
# Use the list of Tests to generate test code
module_3.make_test_file(filename_and_pair_list[0], test_list)
