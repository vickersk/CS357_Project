'''
CS 357 Programming Project

Description:
Given two input DFAs or NFAs for languages A and B, the program will construct and
return the NFA that accepts the concatenation AB.

Author: Kai Vickers
Last Modified: 11/22/2021
'''

import sys
import getopt
import json

def read_fa_from_file(file_name):
    '''
    read_fa_from_file

    Tries tp reads a JSON object from an input file and returns the
    converted dictionary. If the file doesn't exist an error message
    is printed and None is returned.

    Parameters:
        file_name - the name of the file to be opened

    Returns:
        A dictionary of the converted JSON or None if the file doesn't exist
    '''

    if file_name == '':
        print('ERROR: No input file provided')
        return None

    # Attempts to open the file
    try:
        with open(file_name) as file:

            # Loads the json from the file into a dictionary
            try:
                fa_dict = json.load(file)
                return fa_dict

            # If the file can't be converted to JSON, an error is pritned
            except:
                print('ERROR: The file \'' + file_name + '\' could not be converted to JSON')
                return None

    # If the file doesn't exist, an error is printed
    except FileNotFoundError:
        print('ERROR: The file \'' + file_name + '\'does not exist in the directory')
        return None

def is_list_of_strings(lst):
    '''
    is_list_of_strings

    Checks if the specified list is a list of strings.

    Code from the following post on stackoverflow:
    https://stackoverflow.com/questions/18495098/python-check-if-an-object-is-a-list-of-strings

    Parameters:
        lst - list of objects

    Returns:
        True if the list is a list of strings, False otherwise.
    '''

    # First checks if the list is not empty. Then checks if lst is a list.
    # Finally checks if all the elements in the list are strings
    return bool(lst) and isinstance(lst, list) and all(isinstance(elem, str) for elem in lst)

def transitions_valid(transitions):
    '''
    transitions_valid

    Checks if the specified list of transitions is valid by
    checking if the transitions are a list. If so, it next
    checks each transition in the list by checking if the
    transition is a list of strings of length 3.

    Parameters:
        transitions - list of transitions for a finite automata

    Returns:
        True if the transitions are valid, False otherwise.
    '''

    # Checks if transitions is a list type.
    # Returns False if not a list
    if not isinstance(transitions, list):
        print('ERROR: Transistions is not a list')
        return False
    
    # Checks each transition in the transitions list
    else:
        for transition in transitions:
            
            # Checks that there are 3 elements for the two
            # states and the character. If not, returns False
            if len(transition) != 3:
                print('ERROR: A transition does not have exactly 3 elements')
                return False

            # Checks if the transition is a list of strings
            if not is_list_of_strings(transition):
                print('ERROR: A transition is not a list of strings')
                return False

    return True

def concatenate(fa):
    '''
    concatenate

    Concatenates two finite automatas (DFAs or NFAs) into a new NFA,
    as follows:
        - Q = QA U QB
        - sigma = sigmaA U sigmaB
        - delta = {
            deltaA(q, a) | q in QA, q not in FA,
            deltaA(q, a) U q0B | q in QA, q in FA,
            deltaB(q, a) | q in QB
        }
        - q0 = q0A
        - F = FB

    Parameters:
        fas - dictionary containing two finite automatas

    Returns:
        A dictionary of the resulting NFA 
    '''

    fa_fields = list(fa.keys())

    # Fields for the two FAs in the proper order
    fields = [
        'fa_a',
        'fa_b'
    ]

    # Checks if there are exactly two finite automata formatted properly
    if fa_fields == fields:

        # Extracts the two FA
        a = fa['fa_a']
        b = fa['fa_b']

    else:
        print('ERROR: There are not exactly two finite automata')
        return None

    # Extracts the fields (keys) of each disctionary for the two FA
    a_fields = list(a.keys())
    b_fields = list(b.keys())

    # Formal definition fields in the proper order
    def_fields = [
        'states',
        'alphabet',
        'transitions',
        'start_state',
        'accepting_states'
    ]

    # Checks if the formal definition fields of FA A and FA B are
    # in the proper order
    if a_fields != def_fields:
        print('ERROR: Fields for FA A are not properly formatted')
        return None

    if b_fields != def_fields:
        print('ERROR: Fields for FA B are not properly formatted')
        return None

    # Check if each field is the proper type
    for field in def_fields:

        # Checks if the transition list is properly formatted
        if field == 'transitions':
            if not transitions_valid(a['transitions']):
                print('ERROR: Transitions for FA A are not properly formatted')
                return None

            if not transitions_valid(b['transitions']):
                print('ERROR: Transitions for FA B are not properly formatted')
                return None            

        # Checks if the start state is a string
        elif field == 'start_state':
            if not isinstance(a[field], str):
                print('ERROR: \'' + field + '\' field for FA A is not properly formatted')
                return None

            if not isinstance(b[field], str):
                print('ERROR: \'' + field + '\' field for FA B is not properly formatted')
                return None

        # Checks if the other fields are lists of strings
        else:
            if not is_list_of_strings(a[field]):
                print('ERROR: \'' + field + '\' field for FA A is not properly formatted')
                return None

            if not is_list_of_strings(b[field]):
                print('ERROR: \'' + field + '\' field for FA B is not properly formatted')
                return None

    # Combines the transitions of both FAs
    new_transitions = a['transitions'] + b['transitions']

    # Adds the epsilon transitions
    for state in a['accepting_states']:
        new_transitions.append([state, b['start_state'], '&'])
    
    # Creates the new NFA
    nfa = {
        # Combines the states of both FAs
        'states': a['states'] + b['states'],

        # Combines the states of both FAs and
        # removes duplicate characters
        'alphabet': list(set(a['alphabet'] + b['alphabet'])),
        'transitions': new_transitions,

        # Makes the start state the one of FA 'A'
        'start_state': a['start_state'],

        # Makes the final states the ones of FA 'B'
        'accepting_states': b['accepting_states']
    }

    return nfa

def write_nfa_to_file(file_name, nfa):
    '''
    write_fa_to_file

    Writes the finite automata to the output file in JSON format,
    if the file exists. If the file doesn't exist, it is created
    and the JSON string is written to it.

    Parameters:
        file_name - the name of the file to be opened and written to
        nfa - the finite automata to be written to file
    '''

    # Converts the NFA to a JSON string
    try:
        output_json = json.dumps(nfa, indent=4)
        print('Resulting NFA for A and B:\n')
        print(output_json, "\n")

    # Prints an error if the 
    except:
        error_msg = 'ERROR: Unable serialize resulting NFA to JSON'
        print(error_msg)
        return

    # Writes the JSON string to the output file if it exists.
    # Otherwise, it creates the file and writes to it.
    with open(file_name, 'w') as file:
        file.write(output_json)

def main(argv):
    '''
    main

    Reads the input file for the two finite automata and
    creates an NFA for the concatentation of the two languages.
    The output is then printed to the terminal and written to
    the output file.

    Command arguments code modified from the code at the following links:
    - https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    - https://www.geeksforgeeks.org/command-line-arguments-in-python/

    Parameters:
        argv - list of command arguments
    '''

    # Stores the input and output files
    input_file = ''
    output_file = ''

    # Characters for the command options
    options = 'dhi:o:'

    # Strings for the command long options
    long_options = ['help', 'input', 'output', 'default']

    # Tries to parse thecommand for arguments and options
    try:
        opts, arg = getopt.getopt(argv, options, long_options)
    
    # Prints the usage pattern if an argument occurs
    except getopt.GetoptError:
        print('USAGE: concat.py [-h/d] [-i input] [-o output]\n')
        sys.exit(2)

    # Goes through each argument and option in the command
    for opt, arg in opts:

        # Uses the default input and output files
        if opt in ('-d', '--default'):
            input_file = 'input.json'
            output_file = 'output.json'
            print('Setting input and output files to default.\n')

        # Displays summaries of the builtin commands for the program
        elif opt in ('-h', '--help'):
            print('USAGE: concat.py [-h/d] [-i input] [-o output]\n')
            print('Displays brief summaries of builtin commands.\n')
            print('Options:')
            print('  -d,  --default         reads the default input and output files (input.json and output.json)')
            print('  -h,  --help            prints this help')
            print('  -i,  --input=FILE      reads the specified file as input (if not output file is provided, writes to output.json)')
            print('  -o,  --output=FILE     writes the output to the specified file\n')
            sys.exit()
        
        # Specifies an input file to read from
        elif opt in ('-i', '--input'):
            input_file = arg
            output_file = 'output.json'
        
        # Specifies an output file to write to
        elif opt in ('-o', '--output'):
            output_file = arg

    # Prints the input and output files if the command has arguments
    if len(argv) != 0:        
        print('Input file: \'' + input_file + '\'\n')
        print('Output file: \'' + output_file + '\'\n')
    else:
        print('USAGE: concat.py [-h/d] [-i input] [-o output]')
        sys.exit(2)

    # Reads the input file to a dictionary
    fa_dict = read_fa_from_file(input_file)

    # If the file read was successful, it proceeds
    if fa_dict != None:

        # Concatenates A and B in the dictionary input
        concat_nfa = concatenate(fa_dict)

        # Checks if A and B were concatenated
        if concat_nfa != None:
            # Writes the resulting NFA to the output file
            write_nfa_to_file(output_file, concat_nfa)

        # Otherwise, prints an error
        else:
            print('ERROR: The finite automata are not in the proper format')

if __name__ == '__main__':
    main(sys.argv[1:])