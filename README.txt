###############################################################################################
CS 357 Programming Project

GitHub Link: https://github.com/vickersk/CS357_Project

Author: Kai Vickers
Last Modified: 11/23/2021
###############################################################################################
Overview:

Given two input DFAs or NFAs for languages A and B, the program will construct and
return the NFA that accepts the concatenation AB.

The project contains the main file concat.py, that when run will take in a file called 
input.json that has two formal FA descriptions in JSON format and generates an output file 
called output.json containing the resulting NFA's formal description. 

The files, input.json and output.json exist in the main project directory along with concat.py. 
There are also two folders containing test cases, with test_cases_successes containing input 
files that generate the appropriate output and their corresponding output file, and 
test_cases_failures containing input files that produce an error in the program due a problem 
with the input file.

When it comes to limitations, the program doesn't differentitate between whether two DFAs or 
two NFAs are being used as inputs into the program. It only checks whether the fromal defintion
of both FAs is in the correct format.

###############################################################################################
How to compile and run the program:

To compile and run the program, python3 is required. The program can be run as follows:
python3 concat.py. The program will use input.json as the input file and generate output.json.

Additionally, there are options to run specific input files and generate specific output 
files. To specify an input file the -i or --input flags can be used followed by the file path. 
To specify an output file the -o or --output flags can be used followed by the file path. To 
see program usage and the builtin arguments, the -h or --help flags can be used to display 
the infomration in this section.

    Execution examples:
    python3 concat.py
    python3 concat.py -i in.json
    python3 concat.py -o out.json
    python3 concat.py -i in.json -o out.json
    python3 concat.py -h

###############################################################################################
File formats:

The input JSON file must contain two main name/value pairs for the FAs for the languages A and
B respectively. Each value contains an object with name/value pairs for each field of the
formal for its FA. The fields are paired in the following order:

    - "states" is paired with a list of strings of the states
    - "alphabet" is paried with a list of strings of characters
        (Each character should be its own string)
    - "transitions" is paired with a list containing lists of strings. Each sub-list represents a
        transition in the FA. For a transition, the first string is the current state, the
        second string is the resulting state, and the third string is the character the
        transition occured on. 
        Example transition:
            [
                "Q0",
                "Q1",
                "a"
            ]
    - "start_state" is paired with a single string for the starting state
    - "accepting_states" is paried with a list of strings containing all the accepting states

The FA objects are paired with "fa_a" and "fa_b" as follows:
    {
        "fa_a": {
            . . .
        },
        "fa_b": {
            . . .
        }
    }

Example input files can be found in the case input files in the test_cases_successes folder.

The following caveats should be noted about the program:
    - It's assumed that each state has a unique name to avoid confusion between the two FAs. The
      program doesn't check if there are duplicate state names.
    - When creating a NFA, the epsilon character is represented as an ampersand, "&".

The output file is similarly formatted to the input file, with the same name/value pairs for
each field of the formal definition.
###############################################################################################
