#!/bin/python3

from enum import Enum
import re

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

    @name.setter
    def arg_names(self, new_arg_names):
        self._arg_names = new_arg_names

    @property
    def arg_types(self):
        return self._arg_types

    @name.setter
    def arg_types(self, new_arg_types):
        self._arg_types = new_arg_types

    @property
    def output_type(self):
        return self._output_type

    @name.setter
    def output_type(self, new_output_type):
        self._output_type = new_output_type


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

Test_Type = Enum("Test_Type",
                 "test test-exn test-input test-print test-interactive")

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
        regex_result = re.search("(.*[^A-Za-z])([A-Za-z0-9_][A-Za-z0-9_]*)",
                                 argument)
        arg_types.append(regex_result.group(1).lstrip())
        arg_names.append(regex_result.group(2))
        
    return (arg_names, arg_types)

def extract_function_info(fun_signature_str):
    regex_result = re.search("([^ ]*  *)?([^ ][^ ]*)  *([^ ][^ ]*)\(([^\)]*)\)",
                             fun_signature_str)
    return_type = regex_result.group(2)
    func_name = regex_result.group(3)
    func_args = regex_result.group(4)
    func_args_pair = parse_func_args_into_lists(func_args)
    return Fun(func_name, func_args_pair[0], func_args_pair[1], return_type)



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
                    if paren_stack.pop() != '(':
                        print("error")
                        break
                    if len(paren_stack) == 0:
                        expr_list.append(setup_str[expr_start:(pos + 1)])
                    
        pos += 1
        prev_char = char

    return expr_list

def parse_output_str_to_list(output_str):
    output_str += " " # mega hack, had to put it in because my algorithm only
    # detects the end of words on a space: so if a word ends at the end of a str
    # it is never detected
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
                    # finish the string
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



def extract_test_type(test_str):
    return Test_Type[re.search("test(-[^: ]*)?", test_str).group(0)]

def extract_test_inputs(test_str):
    return re.search(">>> test(-[^: ]*)?: " +
                     "([^@][^@]*)@(([^@]*@ )?)([^@]*)", test_str)\
             .group(2)[:-1]\
             .split()

def extract_test_setup_code(test_str):
    search_results = re.search(">>> test(-[^: ]*)?: " +
                               "([^@][^@]*)@(([^@]*@ )?)([^@]*)",
                               test_str)
    if search_results is not None and search_results.group(4) is not None:
        return parse_setup_str_to_list(search_results.group(4)[1:-3])
    else:
        return []

def extract_test_output(test_str):
    result_str = re.search(">>> test(-[^: ]*)?: " +
                           "([^@][^@]*)@(([^@]*@ )?)([^@]*)",
                           test_str).group(5)
    if result_str.startswith(" "):
        return parse_output_str_to_list(result_str[1:])
    else:
        return parse_output_str_to_list(result_str)



# Have:
# (list of tuples)
#   Each maps function signature (string) to list of function tests (strings)

list_of_functions = [("int fac(int x)", ["// >>> test: 0 @ 1",
                                         "// >>> test: 1 @ 1",
                                         "// >>> test: 2 @ 2"]),
                     ("int fac-iter(int n)", ["// >>> test: 0 @ 1",
                                              "// >>> test: 1 @ 1",
                                              "// >>> test: 2 @ 2"])]

list_of_functions_in_data_structure = []


for function in list_of_functions:
    fun_info = extract_function_info(function[0])
    list_of_tests = []
    for test_str in function[1]:
        test_type = extract_test_type(test_str)
        if test_type is Test_Type["test-interactive"]:
            list_of_tests.append(Test(test_type,
                                      fun_info,
                                      [], # input
                                      [], # output
                                      [])) # setup
        if test_type is Test_Type["test-exn"]:
            list_of_tests.append(Test(test_type,
                                      fun_info,
                                      extract_test_inputs(test_str), # input
                                      [], # output
                                      extract_test_setup_code(test_str))) #setup
        else:
            list_of_tests.append(Test(test_type,
                                      fun_info, 
                                      extract_test_inputs(test_str), # input
                                      extract_test_output(test_str), #output
                                      extract_test_setup_code(test_str))) #setup
            list_of_functions_in_data_structure.append((fun_info,
                                                        list_of_tests))


############################## Testing ##############################
TEST = True
if TEST:
    def test(test_expr, expected_result):
        if test_expr == expected_result:
            print("Test PASS")
        else:
            print("Test FAIL")
            assert False
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
    test(extract_test_inputs("// >>> test: 1 2 3 @ 11 12 13"), ["1", "2", "3"])
    test(extract_test_inputs("// >>> test-exn: 1 2 @ std::string \"error\""),
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
    test(extract_test_output("// >>> test-exn: 2 @ std::string \"err msg\""),
         ["std::string", "\"err msg\""])

