# Lukas' module which defines the Test and Fun
import module_2

# (listof Tests) -> Nothing
# Writes testing code to an output file corresponding to the given
# Tests
def make_test_file(fun_file_name, test_list):
        # Remove .cpp from end of fun_file_name if it exists
        if fun_file_name.endswith('.cpp'):
                stripped_fun_file_name = fun_file_name[0:len(fun_file_name) - 4]
        else:
                stripped_fun_file_name = fun_file_name

        test_file_name = stripped_fun_file_name + '_tests.cpp'
        # If file already exists, overwrite it. Else, create the file
        test_file = open(test_file_name, 'w+')
        # Add the include directive to the file
        test_file.write('#include "' + fun_file_name + '"\n\n')
        test_file.write('#include <string>\n#include <vector>\n\n')

        # Overload the ostream operator for exceptions
        # We have to do this so that we can print arbitrary exception types
        # (e.g: std::string)
        test_file.write("std::ostream& operator<<(std::ostream &out, const " +
                        "std::exception &rhs){return out << rhs.what();}")

        # Write all code in a main function
        test_file.write("int main(int argc, char *argv[]){")
        # bool value that stores whether the test passed or failed
        test_file.write('bool result, test_suite_result = true;\n')
        test_file.write('std::vector<std::string> fail_vec;\n')
        test_file.write('bool has_message;\nstd::string exn_mess;\n\n')
        #test_file.write('#include <boost/test/unit_test.hpp>\n')
        #test_file.write('#include <boost/test/output_test_stream.hpp>\n\n')
        # Counter for number of tests ran
        test_num = 1
        # For each test, wrap in a try-catch for exceptions, then make function
        for test in test_list:
                # Create a string of the input arguments with correct commas
                input_string = ''
                for inarg in test.inputs:
                        input_string += inarg
                        # Add a comma and space if it's not the last input
                        if inarg != test.inputs[len(test.inputs) - 1]:
                                input_string += ', '
                # TEST
                if test.Type == module_2.Test_Type['test']:
                        expect_out = test.output[0]
                        # Try block
                        test_file.write('try\n')
                        test_file.write('{\n')
                        # Create variable of output type to store output
                        test_file.write('\t' + test.fun.output_type +
                                        ' output;\n')
                        # Function
                        test_file.write('\toutput =')
                        test_file.write(test.fun.name + '(' +
                                        input_string + ');\n')
                        test_file.write('\tif (output == ' + expect_out + ')\n')
                        test_file.write('\t\tresult = true;\n')
                        test_file.write('\telse\n')
                        test_file.write('\t\tresult = false;\n')
                        test_file.write('}\n')
                        # Catch block
                        test_file.write('catch (std::exception& e)\n')
                        test_file.write('{\n')
                        test_file.write('\tstd::cout << "Exception caught: "' +
                                        ' << e << std::endl;\n')
                        test_file.write('\tresult = false;\n')
                        test_file.write('}\n\n')
                        test_file.write('if (!result)\n')
                        test_file.write('{\n')
                        test_file.write('\ttest_suite_result = false;\n')
                        test_file.write('\tfail_vec.push_back("' +
                                        test.fun.name + '(' + input_string +
                                        ') == ' + expect_out + '");\n')
                        test_file.write('}\n\n')
                # TEST-EXN
                elif test.Type == module_2.Test_Type['test-exn']:
                        exn_type = test.output[0]
                        exn_message = 'Dummy value'
                        output_str = ""
                        test_file.write('has_message = true;\n')
                        if (len(test.output) == 2):
                                exn_message = test.output[1]
                                test_file.write('has_message = true;\n')
                        else:
                                test_file.write('has_message = false;\n')
                        test_file.write('exn_mess = ' +
                                        exn_message + ';\n')
                        test_file.write('try\n')
                        test_file.write('{\n')
                        # Function
                        test_file.write(test.fun.name + '(' +
                                        input_string + ');\n')
                        test_file.write('\tresult = false;\n')
                        output_str = "passed without exception"
                        test_file.write('}\n')
                        # Catch block
                        test_file.write('catch (' + exn_type + '& e)\n')
                        test_file.write('{\n')
                        test_file.write('\tif (has_message)\n')
                        test_file.write('\t\tif (exn_mess.compare(e) ' +
                                        '== 0)\n')
                        test_file.write('\t\t\tresult = true;\n')
                        test_file.write('\t\telse\n\t\t{\n')
                        test_file.write('\t\t\tstd::cout << ' +
                                        '"Exception caught: "' +
                                        ' << e << std::endl;\n')
                        test_file.write('\t\t\tresult = false;\n\t\t}\n')
                        output_str = "threw right exception but wrong message"
                        test_file.write('\telse\n')
                        test_file.write('\t\tresult = true;\n')
                        test_file.write('}\n')
                        # Catch block
                        test_file.write('catch (std::exception& e)\n')
                        test_file.write('{\n')
                        test_file.write('\tstd::cout << "Exception caught: "' +
                                        ' << e << std::endl;\n')
                        test_file.write('\tresult = false;\n')
                        output_str = "threw wrong exception"
                        test_file.write('}\n\n')
                        test_file.write('if (!result)\n')
                        test_file.write('{\n')
                        test_file.write('\ttest_suite_result = false;\n')
                        test_file.write('\tfail_vec.push_back("' +
                                        test.fun.name + '(' +
                                        input_string + ')  ' +
                                        output_str + '");\n')
                        test_file.write('}\n\n')
               # # TEST-PRINT
               # elif test.Type == module_2.Test_Type['test-print']
               #         expect_out = test.output[0]
               #         # Try block
               #         test_file.write('try\n')
               #         test_file.write('{\n')
               #         # For test-print, the function call needs to be before
               #         # the check
               #         test_file.write(test.fun.name + '(' + input_string\
               #                 + ');\n')
               #         # Function
               #         test_file.write('BOOST_CHECK(')
               #         test_file.write(out_test)
               #         test_file.write(' == ' expect_out + ');\n')
               #         test_file.write('}\n')
               #         # Catch block
               #         test_file.write('catch (std::exception& e)')
               #         test_file.write('{\n')
               #         test_file.write('std::cout << "Exception caught: "'\
               #                 + ' << e << std::endl;\n')
               #         test_file.write('}\n\n')
                # TEST-INPUT
                else:
                        # Try block
                        test_file.write('result = true;\n')
                        test_file.write('try\n')
                        test_file.write('{\n')
                        count = 0
                        # Argument declarations
                        for Type in test.fun.arg_types:
                                test_file.write(Type +
                                                test.fun.arg_names[count] +
                                                ';\n')
                                count += 1
                        # Setup
                        for setup_val in test.setup:
                                setup_no_paren = setup_val[1:-1]
                                test_file.write('\t' + setup_no_paren + ';\n')
                        # Function
                        test_file.write(test.fun.name + '(' +
                                        input_string + ');\n')
                        count = 0
                        for in_to_check in test.inputs:
                                test_file.write('\tif (' + in_to_check +
                                                ' != ' + test.output[count] +
                                                ')\n')
                                test_file.write('\t\tresult = false;\n')
                                count += 1
                        test_file.write('}\n')
                        # Catch block
                        test_file.write('catch (std::exception& e)\n')
                        test_file.write('{\n')
                        test_file.write('\tstd::cout << "Exception caught: "' +
                                        ' << e << std::endl;\n')
                        test_file.write('\tresult = false;\n')
                        test_file.write('}\n\n')
                        test_file.write('if (!result)\n')
                        test_file.write('{\n')
                        test_file.write('\ttest_suite_result = false;\n')
                        # Get lists of parameters, setups, expected mutations
                        arg_string = ""
                        setup_string = ""
                        output_string = ""
                        for arg in test.fun.arg_names:
                                arg_string += arg
                                if (arg != test.fun.arg_names[\
                                        len(test.fun.arg_names) - 1]):
                                        arg_string += ', '
                        for setup in test.setup:
                                setup_string += setup
                                if (setup != test.setup[\
                                        len(test.setup) - 1]):
                                        setup_string += ', '
                        for out in test.output:
                                output_string += out
                                if (out != test.output[\
                                        len(test.output) - 1]):
                                        output_string += ', '
                        test_file.write('\tfail_vec.push_back("' +
                                        test.fun.name + '(' + arg_string + ')' +
                                        'with setups ' + setup_string +
                                        'and expected outputs ' +
                                        output_string + '");\n')
                        test_file.write('}\n\n')
        # All cases done, write final result code
        test_file.write('if(test_suite_result)\n')
        test_file.write('\tstd::cout << "All tests passed." << std::endl;\n')
        test_file.write('else\n')
        test_file.write('{\n')
        test_file.write('\tstd::cout << fail_vec.length() << " tests failed."' +
                        '<< " The following tests did not pass:" ' +
                        '<< std::endl;\n')
        test_file.write('\tint i = 0;\n')
        test_file.write('\tfor (i; i < fail_vec.length(); ++i)\n\t{\n')
        test_file.write('\t\tstd::cout << fail_vec[i] << std::endl;\n\t}\n')
        test_file.write('}\n\n')

        test_file.write("return 0;}")
