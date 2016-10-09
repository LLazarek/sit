#!/bin/python3

# Author: Lukas Lazarek
# Date: 2016/10/09
# Purpose: Implement conversion of raw text into structured Test data
#          for use in module_3

from enum import Enum
import re

# class Fun: Stores function signature data
class Fun:
    def __init__(self, name="", arg_names=[], arg_types=[], output_type=""):
        self._name = name
        self._arg_names = arg_names
        self._arg_types = arg_types
        self._output_type = output_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def arg_names(self):
        return self._arg_names

    @arg_names.setter
    def arg_names(self, new_arg_names):
        self._arg_names = new_arg_names

    @property
    def arg_types(self):
        return self._arg_types

    @arg_types.setter
    def arg_types(self, new_arg_types):
        self._arg_types = new_arg_types

    @property
    def output_type(self):
        return self._output_type

    @output_type.setter
    def output_type(self, new_output_type):
        self._output_type = new_output_type

    def __eq__(self, other):
        return (self.name == other.name and self.arg_names == other.arg_names \
                and self.arg_types == other.arg_types and \
                self.output_type == other.output_type)


# class Test: Store test information relating to single test case
class Test:
    def __init__(self, Type, fun, inputs, output, setup):
        self._Type = Type
        self._fun = fun
        self._inputs = inputs
        self._output = output
        self._setup = setup

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, new_Type):
        self._Type = new_Type

    @property
    def fun(self):
        return self._fun

    @fun.setter
    def fun(self, new_fun):
        self._fun = new_fun

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, new_inputs):
        self._inputs = new_inputs

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_output):
        self._output = new_output

    @property
    def setup(self):
        return self._setup

    @setup.setter
    def setup(self, new_setup):
        self._setup = new_setup


# The five supported (or to-be-supported) test types
Test_Type = Enum("Test_Type",
                 "test test-exn test-input test-print test-interactive")





# string -> (tuple (listof string) (listof string))
# Converts a string representation of the arguments of a function
# as they appear in that function's signature into two lists:
# 1. The argument names
# 2. The argument types
#
# E.g:
# "int x, const double &b, float **p"
# ->
# ((list "x", "b", "p"), (list "int", "const double &", "float **"))
def parse_func_args_into_lists(func_args_str):
    arg_names = []
    arg_types = []
    # split on comma
    arguments = func_args_str.split(',')
    # for each argument
    for argument in arguments:
        # Search the string backwards because it's much easier to
        # find the end of a valid variable than the end of a valid type
        regex_result = re.search("([A-Za-z0-9_]+)([*& ].+)",
                                 argument[::-1])
        # Since we reversed the original string, must reverse result strings
        # AND the groupings (e.g: "x tni" -> 1:"x" 2:"tni")
        arg_types.append(regex_result.group(2)[::-1].strip())
        arg_names.append(regex_result.group(1)[::-1].strip())
        
    return (arg_names, arg_types)


# string -> Fun
# Parses the given string representation of a function signature into
# a Fun structure
def extract_function_info(fun_signature_str):
    regex_result = re.search("^\s*([^ ]+\s+)?([^ ]+)\s+([^ ]+)\(([^\)]*)\)",
                             fun_signature_str)
    return_type = regex_result.group(2).strip()
    func_name = regex_result.group(3).strip()
    func_args = regex_result.group(4).strip()
    func_args_pair = parse_func_args_into_lists(func_args)
    return Fun(func_name, func_args_pair[0], func_args_pair[1], return_type)


# string -> (listof string)
# Parses the given string of setup directives of the form "(...)"
# into a list of corresponding individual directives
#
# E.g:
# "(y = 2) (x = &y) (*x = 5)" -> (list "(y = 2)" "(x = &y)" "(*x = 5)")
#
# Uses a simple stack-based algorithm to keep track of balanced parenthesis
# and thereby extract directives
def parse_setup_str_to_list(setup_str):
    paren_stack = []
    expr_list = []
    pos = 0
    expr_start = 0;
    prev_char = ' '
    for char in setup_str:
        if prev_char != '\\':
            if char == '(':
                if len(paren_stack) == 0:
                    expr_start = pos
                paren_stack.append('(')
            else:
                if char == ')':
                    if len(paren_stack) == 0 or paren_stack.pop() != '(':
                        print("error, invalid expression: %s" % setup_str)
                        raise "error"
                    # check the length again, this time after popping the top
                    if len(paren_stack) == 0:
                        expr_list.append(setup_str[expr_start:(pos + 1)])
                    
        pos += 1
        prev_char = char

    return expr_list

# string -> (listof string)
# Converts the given string of expected output(s) into a list of individual
# output strings
#
# E.g:
# "std::string \"error message\"" -> (list "std::string" "\"error message\"")
def parse_output_str_to_list(output_str):
    # A bit of a workaround: this algorithm only detects the end of words on a
    # space, so a space must be at the end of the string
    output_str += " "

    # Let a string be a quoted/string output (which may contain spaces),
    # let a word be unquoted outputs seperated by spaces
    if '"' in output_str:
        outlist = []
        in_str = False
        in_word = False
        start_of_string = 0
        start_of_word = 0
        current_position = 0;
        prev_char = ' '
        for char in output_str:
            if char == '"' and prev_char != '\\':
                if not in_str:
                    in_str = True
                    start_of_string = current_position
                else:
                    outlist.append\
                        (output_str[start_of_string:(current_position + 1)])
                    in_str = False
            elif char != ' ' and not in_str and not in_word:
                in_word = True
                start_of_word = current_position
            elif char == ' ' and not in_str and in_word:
                outlist.append(output_str[start_of_word:current_position])
                in_word = False
            current_position += 1
            prev_char = char
        return outlist
    else:
        return output_str.split()


# string -> Test_Type
# Determine the Test_Type of the test represented by the given string
def extract_test_type(test_str):
    return Test_Type[re.search("test(-[^: ]*)?", test_str).group(0)]


# string -> (listof string)
# Extract the individual inputs represented by the given test string
def extract_test_inputs(test_str):
    return re.search(">>> test(-[^: ]*)?: " +
                     "([^@][^@]*)@(([^@]*@ )?)([^@]*)", test_str)\
             .group(2)[:-1]\
             .split()


# string -> (listof string)
# Extract the individual setup directives from the given test string
def extract_test_setup_code(test_str):
    search_results = re.search(">>> test(-[^: ]*)?: " +
                               "([^@][^@]*)@(([^@]*@ )?)([^@]*)",
                               test_str)
    if search_results is not None and search_results.group(4) is not None:
        return parse_setup_str_to_list(search_results.group(4)[1:-3])
    else:
        return []


# string -> (listof string)
# Extract the individual expected outputs from the given test string
def extract_test_output(test_str):
    result_str = re.search(">>> test(-[^: ]*)?: " +
                           "([^@][^@]*)@(([^@]*@ )?)([^@]*)",
                           test_str).group(5)
    if result_str.startswith(" "):
        return parse_output_str_to_list(result_str[1:])
    else:
        return parse_output_str_to_list(result_str)



# (listof (tuple string (listof string))) -> (listof Test)
# Takes a list of function signature strings mapped to lists of
# function test strings and produces a corresponding list of
# Tests
def build_test_list(list_of_functions):
    list_of_all_tests = []

    for function in list_of_functions:
        fun_info = extract_function_info(function[0])
        function_tests = []
        for test_str in function[1]:
            test_type = extract_test_type(test_str)
            if test_type is Test_Type["test-interactive"]:
                test = Test(test_type,
                            fun_info,
                            [], # input
                            [], # output
                            []) # setup
                function_tests.append(test) 
            elif test_type is Test_Type["test-exn"]:
                test = Test(test_type,
                            fun_info,
                            extract_test_inputs(test_str), # input
                            extract_test_output(test_str), #output
                            extract_test_setup_code(test_str)) #setup
                function_tests.append(test)
            else:
                test = Test(test_type,
                            fun_info, 
                            extract_test_inputs(test_str), # input
                            extract_test_output(test_str), #output
                            extract_test_setup_code(test_str)) # setup
                function_tests.append(test)
                
        list_of_all_tests.extend(function_tests)
        
    return list_of_all_tests


############################## Testing ##############################
if __name__ == '__main__':
    TEST = True
    if TEST:
        def test(test_expr, expected_result):
            assert test_expr == expected_result
            print("Test PASS")

        print("======== test type extraction =========")
        test(extract_test_type("// >>> test: fijodsijf"),
             Test_Type["test"])
        test(extract_test_type("// >>> test-exn: sdoifjsidojf"),
             Test_Type["test-exn"])
        test(extract_test_type("// >>> test-input: sfdhudfihg"),
             Test_Type["test-input"])
        test(extract_test_type("// >>> test-print: dsiojfosidj"),
             Test_Type["test-print"])
        test(extract_test_type("// >>> test-interactive"),
             Test_Type["test-interactive"])

        print("======== test extract test inputs ==========")
        test(extract_test_inputs("// >>> test: 1 @ 11"), ["1"])
        test(extract_test_inputs("// >>> test: 1 2 3 @ 11 12 13"),
             ["1", "2", "3"])
        test(extract_test_inputs("// >>> test-exn: 1 2 @ " + 
                                 "std::string \"error\""),
             ["1", "2"])
        test(extract_test_inputs("// >>> test-input: *x **p " +
                                 "@ (y = 5) (*x = &y) (**p = 0) @ 5 0"),
             ["*x", "**p"])

        print("============ test extract setup code ===========")
        test(extract_test_setup_code("// >>> test-input: *x **p " +
                                     "@ (y = 5) (*x = &y) (**p = 0) @ 5 0"),
             ["(y = 5)", "(*x = &y)", "(**p = 0)"])
        test(extract_test_setup_code("// >>> test: 1 @ 2"), [])
        test(extract_test_setup_code("// >>> test: 1 @ (x = 5) @ 2"),
             ["(x = 5)"])


        print("========== test extract output ==========")
        test(extract_test_output("// >>> test: 1 @ 2"), ["2"])
        test(extract_test_output("// >>> test: 1 2 3 @ 4"), ["4"])
        test(extract_test_output("// >>> test-input: **x, *x, p " +
                                 "@ (x = 5) (y + 5) (**p = &x) @ 5 2 3"),
             ["5", "2", "3"])
        test(extract_test_output("// >>> test-print: 2 @ (some setup) " +
                                 "@ \"yo\" std::string"),
             ["\"yo\"", "std::string"])
        test(extract_test_output("// >>> test-exn: 2 @ std::string "
                                 "\"err msg\""),
             ["std::string", "\"err msg\""])


        print("========== test extract function info ==========")
        test(extract_function_info("int fac_iter(int n){"),
             Fun("fac_iter",
                 ["n"],
                 ["int"],
                 "int"))
        test(extract_function_info("int fac_iter1(int res, int n){"),
             Fun("fac_iter1",
                 ["res", "n"],
                 ["int", "int"],
                 "int"))

        test(extract_function_info("int fac_iter1(int res1, int n1_res){"),
             Fun("fac_iter1",
                 ["res1", "n1_res"],
                 ["int", "int"],
                 "int"))

        test(extract_function_info("int fac(int n){"),
             Fun(name="fac",
                arg_names=["n"],
                arg_types=["int"],
                output_type="int"))
