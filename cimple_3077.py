import sys

# keywords of the language
keyword_dict = {
    "program_tk": "program",
    "declare_tk": "declare",
    "function_tk": "function",
    "procedure_tk": "procedure"
                    ""
}
program_tk, declare_tk, function_tk, procedure_tk = "program", "declare", "function", "procedure"
in_tk, inout_tk, if_tk, else_tk, while_tk, switchcase_tk = "in", "inout", "if", "else", "while", "switchcase"
case_tk, default_tk, forcase_tk, incase_tk, return_tk = "case", "default", "forcase", "incase", "return"
call_tk, print_tk, input_tk, or_tk, and_tk = "call", "print", "input", "or", "and", "not"

# symbols of the languages
add_tk, minus_tk, multiple_tk, divide_tk = "+", "-", "*", "/"
# "add", "minus", "multiple", "divide"
lower_tk, greater_tk, equal_tk, lower_equal_tk, greater_equal_tk, not_equal_tk = "<", ">", "=", "<=", ">=", "<>"
# "lower", "greater", "equal", "lower_equal", "comma"
comma_tk, assignment_tk, semicolon_tk = ",", ":=", ";"
# "greater_equal", "not_equal", "assignment", "semicolon"
left_bracket_tk, left_brace_tk, left_parenthesis_tk = "[", "{", "("
# "left_bracket", "left_brace", "left_parenthesis"
right_bracket_tk, right_brace_tk, right_parenthesis_tk = "]", "}", ")"
# "right_bracket", "right_brace", "right_parenthesis"


# states of lexical analyzer automata
ST_START, ST_LETTER, ST_DIGIT, ST_LOWER, ST_GREATER, ST_ASGN, ST_COMMENT = 0, 1, 2, 3, 4, 5, 6

forbidden_char = ["!", "@", "$", "%", "^", "&", "_", "|", "'", "~", "`", "¨"]
symbols = ["+", "-", "*", "/", "=", ",", ";", "[", "{", "(", "]", "}", ")"]

char = ""
token_type = ""
file = open(str(sys.argv[1]))
line = 0


def check_forbidden_char():
    if char in forbidden_char:
        print("Forbidden character %s" % (char))
        sys.exit(0)


def read_next():
    global char, row, fd
    char = fd.read(1)
    # Checks if the file has one of the forbidden_char characters.If it has then exit.
    if char in forbidden_char:
        print("Forbidden character %s" % char)
        sys.exit(0)
    if char == "\n":
        row = row + 1
    return char


# lexical analyzer
def lex():
    global char, file, line, token_type
    state = ST_START
    number = 0
    alphanumeric = ""
    comments_closed = True
    while True:
        char = file.read(1)
        check_forbidden_char()
        if char == "\n":
            line += 1
            continue
        elif char == ".":
            char = file.read(1)
            if char == "EOF" and comments_closed:
                print("End of the program")
                break
            elif char != "EOF":
                print("Error EOF - No characters should exist after character . \n character . shows EOF")
            # todo maybe it need if and not elif
            elif not comments_closed:
                print("Comments haven't closed")

        # start of the automata
        # being in start state
        if state == ST_START and char == "\n":
            state = ST_START
            line += 1
            continue
        elif state == ST_START and (char.isspace() or char == "return" or char == "\t"):
            continue
        elif state == ST_START and char.isalpha():
            state = ST_LETTER
            continue
        elif state == ST_START and char.isdigit():
            number = char
            state = ST_DIGIT
            continue
        elif state == ST_START and char == "<":
            state = ST_LOWER
            continue
        elif state == ST_START and char == ">":
            state = ST_GREATER
            continue
        elif state == ST_START and char == ":":
            state = ST_ASGN
            continue
        elif state == ST_START and char == "#":
            state = ST_START
            comments_closed = not comments_closed
            continue
        elif state == ST_START and (char in symbols):
            token_type = char
            return token_type

        # being in letter state
        elif state == ST_LETTER and char.isalpha():
            return

        # being in digit state
        elif state == ST_LOWER and char.isdigit():
            while char.isdigit():
                number = int(str(number) + str(char))
                # todo maybe it need range +1 at the second
                if number in range(- pow(2, 32) - 1, pow(2, 32) - 1):
                    char = file.read(1)
                else:
                    print("Invalid constant \n Constants should be in the range of –(2^32 − 1) to 2^32 − 1")
            # todo return to syntax analyzer
            continue
        # being in lower state
        elif state == ST_LOWER and char == "=":
            token_type = lower_equal_tk
            return token_type
        elif state == ST_LOWER and char == ">":
            token_type = not_equal_tk
            return token_type
        elif state == ST_LOWER and char not in ["=", ">"]:
            token_type = lower_tk
            return token_type

        # being in greater state
        elif state == ST_GREATER and char == "=":
            token_type = greater_equal_tk
            return token_type
        elif state == ST_GREATER and char not in ["=", "<"]:
            token_type = greater_tk
            return token_type
        elif state == ST_GREATER and char == "<":
            print("The >< is invalid")

        # being in asgn state
        elif state == ST_ASGN and char == "=":
            token_type = assignment_tk
            return token_type
        elif state == ST_ASGN and char != "=":
            print("Invalid statement")
