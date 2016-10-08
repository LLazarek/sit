# Lukas' module which defines the Test and Fun
import module_2.py

def MakeTestFile(fun_file_name, test_list = [])
        # Remove .cpp from end of fun_file_name if it exists
        if endswith('.cpp')
                stripped_fun_file_name = fun_file_name[0:len(fun_file_name) - 3]
        else
                stripped_fun_file_name = fun_file_name

        test_file_name = stripped_fun_file_name + '_tests.cpp'
        # If file already exists, overwrite it. Else, create the file
        test_file = open(test_file_name, 'w+')
        # Add the include directives to the file
        test_file.write('#include "' + fun_file_name + '"\n')
        test_file.write('#include ""\n\n')
        # For each test, wrap in a try-catch for exceptions, then make function
        for Test in test_list
                # Try block
                test_file.write('try\n')
                test_file.write('{\n')
                # Add functions here
                test_file.write('}\n')
                # Catch block
                test_file.write('catch (std::exception& e)')
                test_file.write('{\n')
                test_file.write('std::cout << "Exception caught: " << e.what()'\
                        + ' << std::endl;\n')
                test_file.write('}\n\n')
