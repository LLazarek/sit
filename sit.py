#!/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# The application: brings together all modules into a single application

import module_1
import module_2
import module_3

# Parse the code file to obtain the function/test pair list
filename_and_pair_list = module_1.parse_code()
# Convert the plaintext list into list of Tests
test_list = module_2.build_test_list(filename_and_pair_list[1])
# Use the list of Tests to generate test code
module_3.make_test_file(filename_and_pair_list[0], test_list)
