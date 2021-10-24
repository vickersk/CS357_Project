import json

# Constants for file names
INPUT_FILE = 'input.json'
OUTPUT_FILE = "output.json"

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

    # Attempts to open the file
    try:
        with open(file_name) as file:

            # Loads the json from the file into a dictionary
            fa_dict = json.load(file)
            return fa_dict

    # If the file doesn't exist, an error is printed
    except FileNotFoundError:
        error_msg = "ERROR: The file '"+ file_name + "' does not exist in the directory"
        print(error_msg)
        return None

def concatenate(fas):
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

    # Extracts the two FA
    a = fas["fa_a"]
    b = fas["fa_b"]

    # Combines the transitions of both FAs
    new_transitions = a["transitions"] + b["transitions"]

    # Adds the epsilon transitions
    for state in a["accepting_states"]:
        new_transitions.append([state, b["start_state"], "&"])
    

    new_fa = {
        # Combines the states of both FAs
        "states": a["states"] + b["states"],

        # Combines the states of both FAs and
        # removes duplicate characters
        "alphabet": list(set(a["alphabet"] + b["alphabet"])),
        "transitions": new_transitions,

        # Makes the start state the one of FA 'A'
        "start_state": a["start_state"],

        # Makes the final states the ones of FA 'B'
        "accepting_states": b["accepting_states"]
    }

    return new_fa

def write_fa_to_file(file_name, fa):
    '''
    write_fa_to_file

    Writes the finite automata to the output file in JSON format,
    if the file exists. If the file doesn't exist, it is created
    and the JSON string is written to it.

    Parameters:
        file_name - the name of the file to be opened and written to
        fa - the finite automata to be written to file
    '''

    # Converts the finite automata to a JSON string
    output_json = json.dumps(fa, indent=4)

    # Writes the JSON string to the output file if it exists.
    # Otherwise, it creates the file and writes to it.
    with open(file_name, "w") as file:
        file.write(output_json)

# Reads the input file to a dictionary
fa_dict = read_fa_from_file(INPUT_FILE)

# If the file read was successful, it proceeds
if fa_dict != None:

    # Concatenates A and B in the dictionary input
    concat_nfa = concatenate(fa_dict)

    # Writes the resulting NFA to the output file
    write_fa_to_file(OUTPUT_FILE, concat_nfa)

# Otherwise, prints an error
else:
    print("ERROR: Input file read incorrectly")