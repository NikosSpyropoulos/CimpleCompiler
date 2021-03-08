import sys

# keywords of the language
keyword_dict = {
    "program": "program_tk",
    "declare": "declare_tk",
    "function": "function_tk",
    "procedure": "procedure_tk",
    "in": "in_tk",
    "inout": "inout_tk",
    "if": "if_tk",
    "else": "else_tk",
    "while": "while_tk",
    "switchcase": "switchcase_tk",
    "case": "case_tk",
    "default": "default_tk",
    "forcase": "forcase_tk",
    "incase": "incase_tk",
    "return": "return_tk"
}
program_tk, declare_tk, function_tk, procedure_tk = "program", "declare", "function", "procedure"
in_tk, inout_tk, if_tk, else_tk, while_tk, switchcase_tk = "in", "inout", "if", "else", "while", "switchcase"
case_tk, default_tk, forcase_tk, incase_tk, return_tk = "case", "default", "forcase", "incase", "return"
call_tk, print_tk, input_tk, or_tk, and_tk, not_tk, id_tk = "call", "print", "input", "or", "and", "not", "id"
number_tk = "number"

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
keywords = ["program", "declare", "function", "procedure", "in", "inout", "if", "else", "while", "switchcase",
            "case", "default", "forcase", "incase", "return", "call", "print", "input", "or", "and", "not"]
EOF = ''
char = ""
token_type = ""
file = open(str(sys.argv[1]))
line = 1
token = ""


def check_forbidden_char():
    if char in forbidden_char:
        print("Forbidden character '%s'" % char)
        print("line:", line)
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
        if char == ".":
            char = file.read(1)
            if char == EOF and comments_closed:
                print("End of the program")
                sys.exit(0)
            elif char != EOF:
                print("Error EOF - No characters should exist after character '.' ")
                print("The char '.' symbolize the end of the program")
                print("line: ", line)
                sys.exit(0)
            # todo maybe it need if and not elif
            elif not comments_closed:
                print("Comments haven't closed")
                sys.exit(0)

        # start of the automata
        # being in start state
        # if state == ST_START and char == "\n":
        #     state = ST_START
        #     line += 1
        #     continue
        elif state == ST_START and (char.isspace() or char == "return" or char == "\t"):
            continue
        elif state == ST_START and char.isalpha():
            state = ST_LETTER
            alphanumeric = char
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
            while char.isdigit() or char.isalpha():
                alphanumeric = str(alphanumeric) + str(char)
                if len(alphanumeric) <= 30:
                    char = file.read(1)
                    # if char == "\n":
                    #     line += 1
                    continue
                else:
                    print("Invalid alphanumeric \n The length of an alphanumeric should be lower or equal of 30 ")
                    print("line: ", line)
                    sys.exit(0)
            if alphanumeric in keywords:
                token_type = alphanumeric
                return alphanumeric
            else:
                token_type = alphanumeric
                return id_tk

        # todo return to syntax analyzer
        # being in digit state
        elif state == ST_DIGIT and char.isdigit():
            while char.isdigit():
                number = int(str(number) + str(char))
                # todo maybe it need range +1 at the second
                if number in range(- pow(2, 32) - 1, pow(2, 32) - 1):
                    char = file.read(1)

                    # if char == "\n":
                    #     line += 1
                    #     continue
                else:
                    print("Invalid constant \n Constants should be in the range of –(2^32 − 1) to 2^32 − 1")
                    print("line: ", line)
                    sys.exit(0)
            # todo return to syntax analyzer
            if not char.isalpha():
                return number_tk  # return number
            else:
                print("Invalid character, letter after number")
                print("line: ", line)
                sys.exit(0)

        elif state == ST_DIGIT and char.isalpha():
            print("Invalid character, letter after number")
            print("line: ", line)
            sys.exit(0)
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
            print("line: ", line)
            sys.exit(0)

        # being in asgn state
        elif state == ST_ASGN and char == "=":
            token_type = assignment_tk
            return token_type
        elif state == ST_ASGN and char != "=":
            print("Invalid statement")
            print("line: ", line)
            sys.exit(0)


# syntax analyzer

'''
# " program " is the starting symbol
    program : program ID block .
'''


def program():
    global line, token
    token = lex()
    if token == program_tk:
        token = lex()
        if token == id_tk:
            block()
        else:
            print("program name expected \n line:", line)
            sys.exit(0)
    else:
        print("the keyword 'program' was expected\n line:", line)
        sys.exit(0)


'''
# a block with declarations , subprogram and statements
block : declarations subprograms statements
'''


def block():
    declarations()
    subprograms()
    statements()


'''
# declaration of variables , zero or more " declare " allowed
declarations : ( declare varlist ; )∗
'''


def declarations():
    global line, token
    while token == declare_tk:
        token = lex()
        varList()
        if token == semicolon_tk:
            token = lex()
        else:
            print("Syntax error: ';' was expected\n line:", line)
            sys.exit(0)


'''
# a list of variables following the declaration keyword
varlist : ID ( , ID )∗ | ε
'''


def varList():
    global token, line

    if token == id_tk:
        token = lex()
    # todo maybe the while here is wrong check it
    while token == comma_tk:
        token = lex()
        if token == id_tk:
            token = lex()
        else:
            print("Error: was expected variable\n line:", line)
            sys.exit(0)


'''
# zero or more subprograms allowed
subprograms : ( subprogram )∗
'''


def subprograms():
    subprogram()


'''
# a subprogram is a function or a procedure ,
# followed by parameters and block
subprogram : function ID ( formalparlist ) block
| procedure ID ( formalparlist ) block
'''


def subprogram():
    global token, line
    if token == function_tk or token == procedure_tk:
        token = lex()
        if token == id_tk:
            token = lex()
            if token == left_parenthesis_tk:
                formalparlist()
                if token == right_parenthesis_tk:
                    block()
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
        else:
            print("Error: was expected variable\n line:", line)
            sys.exit(0)


'''
# list of formal parameters
formalparlist : formalparitem ( , formalparitem )∗
| ε
'''


def formalparlist():
    global token
    formalparitem()
    while token == comma_tk:
        formalparitem()
        # todo check for errors "comma expected"


'''
# a formal parameter (" in ": by value , " inout " by reference )
formalparitem : in ID
| inout ID
'''


def formalparitem():
    global line, token
    if token == in_tk or inout_tk:
        token = lex()
        if token == id_tk:
            token = lex()
    else:
        print("Syntax error: 'in' or 'inout' was expected\n line:", line)
        sys.exit(0)


'''
# one or more statements
statements : statement ;
| { statement ( ; statement )∗
}
'''


def statements():
    global line, token
    # todo somehow i have to check if there is } but no { at the start
    if token == left_brace_tk:
        statement()
        while token == semicolon_tk:
            statement()
        if token == right_brace_tk:
            token = lex()
        print("Syntax error: '}' was expected\n line", line)
        sys.exit(0)
    else:
        statement()
        if token == semicolon_tk:
            token = lex()
        else:
            print("Syntax error: ';' was expected\n line:", line)
            sys.exit(0)


'''
# one statement
statement : assignStat
    | ifStat
    | whileStat
    | switchcaseStat
    | forcaseStat
    | incaseStat
    | callStat
    | returnStat
    | inputStat
    | printStat
    | ε
'''


def statement():
    assignStat()
    ifStat()
    whileStat()
    switchcaseStat()
    forcaseStat()
    incaseStat()
    callStat()
    returnStat()
    inputStat()
    printStat()


'''
# assignment statement
assignStat : ID := expression
'''


def assignStat():
    global token, line
    if token == id_tk:
        token = lex()
        if token == assignment_tk:
            token = lex()
            expression()
        else:
            print("Syntax error: ':=' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Error: was expected variable\n line:", line)
        sys.exit(0)


'''
# if statement
ifStat : if ( condition ) statements elsepart
'''


def ifStat():
    global token, line
    if token == left_parenthesis_tk:
        condition()
        if token == right_parenthesis_tk:
            statements()
            elsepart()
        else:
            print("Syntax error: ')' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: '(' was expected\n line:", line)
        sys.exit(0)


'''
elsepart : else statements
| ε
'''


def elsepart():
    global token, line
    if token == else_tk:
        statements()
    else:
        print("Syntax error: 'else' was expected\n line:", line)
        sys.exit(0)


'''
# while statement
whileStat : while ( condition ) statements
'''


def whileStat():
    global token, line
    if token == while_tk:
        token = lex()
        if token == left_parenthesis_tk:
            condition()
            if token == right_parenthesis_tk:
                statements()
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '(' was expected\n line:", line)
            sys.exit(0)
    else:
        # todo probably this is not right (check if to understand)
        print("Syntax error: 'while' was expected\n line:", line)
        sys.exit(0)


'''
# switch statement
switchcaseStat: switchcase
( case ( condition ) statements )∗
default statements
'''


def switchcaseStat():
    global token, line
    if token == switchcase_tk:
        token = lex()
        while token == case_tk:
            if token == left_parenthesis_tk:
                condition()
                if token == right_parenthesis_tk:
                    statements()
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)
        # todo somehow i have to check "error - case"
        if token == default_tk:
            statements()
        else:
            print("Syntax error: 'default' was expected\n line:", line)
            sys.exit(0)


'''
# forcase statement
forcaseStat : forcase
( case ( condition ) statements )∗
default statements
'''


def forcaseStat():
    global token, line
    if token == forcase_tk:
        token = lex()
        while token == case_tk:
            if token == left_parenthesis_tk:
                condition()
                if token == right_parenthesis_tk:
                    statements()
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)
        # todo somehow i have to check "error - case", i realised that the format is same with the switchcase
        if token == default_tk:
            statements()
        else:
            print("Syntax error: 'default' was expected\n line:", line)
            sys.exit(0)


'''
# incase statement
incaseStat : incase
( case ( condition ) statements )∗
'''


def incaseStat():
    global token, line
    if token == incaseStat():
        token = lex()
        while token == case_tk:
            if token == left_parenthesis_tk:
                condition()
                if token == right_parenthesis_tk:
                    statements()
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)
        # todo somehow i have to check "error - case", i realised that the format is same with the switchcase


'''
# return statement
returnStat : return( expression )
'''


def returnStat():
    global token, line
    if token == return_tk:
        token = lex()
        if token == left_parenthesis_tk:
            expression()
            if token == right_parenthesis_tk:
                token = lex()
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '(' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: 'return' was expected\n line:", line)
        sys.exit(0)


'''
# call statement
callStat : call ID( actualparlist )
'''


def callStat():
    global token, line
    if token == call_tk:
        token = lex()
        if token == id_tk:
            token = lex()
            if token == left_parenthesis_tk:
                actualparlist()
                if token == right_parenthesis_tk:
                    token = lex()
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)
    else:
        print("Syntax error: 'call' was expected\n line:", line)
        sys.exit(0)


'''
# print statement
printStat : print( expression )
'''


def printStat():
    global token, line
    if token == print_tk:
        token = lex()
        if token == left_parenthesis_tk:
            expression()
            if token == right_parenthesis_tk:
                token = lex()
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '(' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: '(' was expected\n line:", line)
        sys.exit(0)


# todo i think i have to change the ID and INTEGER, i have to make methods for them

'''
# input statement
inputStat : input( ID )
'''


def inputStat():
    global token, line
    if token == input_tk:
        token = lex()
        if token == left_parenthesis_tk:
            token = lex()
            if token == id_tk:
                token = lex()
                if token == right_parenthesis_tk:
                    token = lex()
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Error: was expected variable\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '(' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: 'input' was expected\n line:", line)
        sys.exit(0)


'''
# list of actual parameters
actualparlist : actualparitem ( , actualparitem )∗
| ε
'''


def actualparlist():
    global token, line
    actualparitem()
    while token == left_parenthesis_tk:
        token = lex()
        if token == comma_tk:
            token = lex()
            actualparitem()
            if token == right_parenthesis_tk:
                token = lex()
                continue
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: ',' was expected\n line:", line)
            sys.exit(0)


'''
# an actual parameter (" in ": by value , " inout " by reference )
actualparitem : in expression
            | inout ID
'''


def actualparitem():
    global token, line
    if token == in_tk:
        expression()
    elif token == inout_tk:
        token = lex()
        if token == id_tk:
            token = lex()
        else:
            print("Error: was expected variable\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: 'in' or 'inout' was expected\n line:", line)
        sys.exit(0)


'''
# boolean expression
condition : boolterm ( or boolterm )∗
'''


def condition():
    global token, line
    boolterm()
    while token == left_parenthesis_tk:
        token = lex()
        if token == or_tk:
            boolterm()
            if token == right_parenthesis_tk:
                token = lex()
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Error: was expected variable\n line:", line)
            sys.exit(0)


'''
# term in boolean expression
boolterm : boolfactor ( and boolfactor )∗
'''


def boolterm():
    global token, line
    boolfactor()
    while token == left_parenthesis_tk:
        token = lex()
        if token == and_tk:
            boolterm()
            if token == right_parenthesis_tk:
                token = lex()
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Error: was expected variable\n line:", line)
            sys.exit(0)


'''
# factor in boolean expression
boolfactor : not [ condition ]
            | [ condition ]
            | expression REL_OP expression
'''


def boolfactor():
    global token, line
    if token == not_tk:
        if token == left_bracket_tk:
            token = lex()
            condition()
            if token == right_bracket_tk:
                token = lex()
            else:
                print("Syntax error: ']' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '[' was expected\n line:", line)
            sys.exit(0)
    elif token == left_bracket_tk:
        token = lex()
        condition()
        if token == right_bracket_tk:
            token = lex()
        else:
            print("Syntax error: ']' was expected\n line:", line)
            sys.exit(0)
    else:
        expression()
        rel_op()
        expression()


'''
# arithmetic expression
expression : optionalSign term ( ADD_OP term )∗
'''


def expression():
    optionalSign()
    term()
    while add_op():
        term()


'''
# term in arithmetic expression
term : factor ( MUL_OP factor )∗
'''


def term():
    factor()
    while mull_op():
        factor()


'''
# factor in arithmetic expression
factor : INTEGER
        | ( expression )
        | ID idtail
'''


def factor():
    global token, line
    if token == number_tk:
        token = lex()
    elif token == left_parenthesis_tk:
        expression()
        if token == right_parenthesis_tk:
            token = lex()
        else:
            print("Syntax error: ')' was expected\n line:", line)
            sys.exit(0)
    elif token == id_tk:
        idtail()
    else:
        print("Error: the code is not following the 'factor' grammar\nline", line)


'''
# follows a function of procedure ( parethnesis and parameters )
idtail : ( actualparlist )
        | ε
'''


def idtail():
    global token, line
    if token == left_parenthesis_tk:
        actualparlist()
        if token == right_parenthesis_tk:
            token = lex()
        else:
            print("Syntax error: ')' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: ')' was expected\n line:", line)
        sys.exit(0)


'''
# sumbols "+" and " -" ( are optional )
optionalSign : ADD_OP
            | ε
'''


def optionalSign():
    add_op()


'''
REL_OP : = | <= | >= | > | < | <>
'''


def rel_op():
    global token, line
    if token == equal_tk or token == lower_equal_tk or token == greater_equal_tk:
        token == lex()
    elif token == greater_tk or token == lower_tk or token == not_equal_tk:
        token == lex()
    else:
        print("Syntax error: a relational operator was expected\nline", line)


'''
ADD_OP : + | -
'''


def add_op():
    global token, line
    if token == add_tk or token == minus_tk:
        token = lex()
    else:
        print("Syntax error: '+' or '-' operator was expected\nline", line)


'''
MUL_OP : * | /
'''


def mull_op():
    global token, line
    if token == multiple_tk or token == divide_tk:
        token = lex()
    else:
        print("Syntax error: '*' or '/' operator was expected\nline", line)


if __name__ == '__main__':
    program()
