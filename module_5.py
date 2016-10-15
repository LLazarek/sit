#!/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Module 5: Property-based testing
# Author: Lukas Lazarek

NUM_TEST = 100
MAX_TRY = 10000

# alternative idea is to have custom functions written in C++ to generate
# inputs
rand_int_fun = "rand()"

prop_str = "fib_iter(n) == fib_iter(n-2) + fib_iter(n-1)"
prop_vars = [("n", "int")]
prop_constraints = ["n > 0", "n < 1000"]

test_code = "int cnt = 0;\nint i = 0;"
test_code += "for(; " + \
             "i < %s && cnt < %s; ++cnt){\n" % (NUM_TEST, MAX_TRY)

for var in prop_vars:
    test_code += var[1] + " " + var[0] + " = " + rand_int_fun + ";\n"
    test_code += "if(cnt%2 == 0) " + var[0] + " *= -1;\n"

for constraint in prop_constraints:
    if '<' in constraint:
        test_code += constraint.replace("<", "%=") + ";\n"
    else:
        # skip generated input that doesn't fit this constraint
        test_code += "if(!(" + constraint + ")) continue;\n"

test_code += "if(!(" + prop_str + ")){\n"
test_code += "std::cout << \"Test failed: property [" + prop_str + \
             "] does not hold for value:\\n\"";

for var in prop_vars:
    test_code += "\n<< \"> %s = \" << %s << std::endl" %(var[0], var[0])

test_code += ";\nreturn 1;\n}\nelse ++i;\n}\n\n"

test_code += "std::cout << \"Passed \" << i << \" tests.\" << std::endl;\n"

print(test_code)
