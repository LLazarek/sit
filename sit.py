#!/bin/python3

import module_1
import module_2
import module_3

filename_and_pair_list = module_1.parse_code()
test_list = module_2.build_test_tree(filename_and_pair_list[1])
module_3.make_test_file(filename_and_pair_list[0], test_list)
