from sql_conn import solutionLookup

def puzzleSolver(puzzle):

    input_list = puzzle.split()[5:]
    input_value = "".join([input_decoder(n[1:]) for n in input_list])
    output_list = solution(input_value)
    formatted_output = format_output(output_list)
    return " ABCD {}".format(formatted_output)


def input_decoder(code):

    for character in ['<', '>', '=']:
        if character in code:
            ind = str(code).find(character)
            return '{}{}'.format(character, ind)


def solution(input_value):

    try:
        
        #attempt to pull solution from mysql table
        solution = solutionLookup(input_value)

    except:

        #in case mysql is down, pull from hardcoded solutions
        f = open('solutions.txt')
        for solution_line in f:
            question = solution_line.split()[0]
            if question == input_value:
                solution = solution_line.split()[1]
                break
        f.close()
        
    finally:

        if not solution:
            solution = ''

        solution_list = [solution[i:i+3] for i in range(0, len(solution), 3)]
        return solution_list


def format_output(output_list):

    equal_inserted_output_list = insert_equals(output_list)
    letter_inserted_output_list = insert_letter(equal_inserted_output_list)
    formatted_output = " ".join(letter_inserted_output_list)
    return formatted_output


def insert_equals(output_list):

    new_list = []
    for i, value in enumerate(output_list):
      new_list.append(value[:i] + "=" + value[i:])
    return new_list


def insert_letter(output_list):

    letters = "ABCD"
    new_list = []
    for i, value in enumerate(output_list):
        new_list.append(letters[i]+value)

    return new_list