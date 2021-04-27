import sys

# todo nextquad() returns the number of the next quad
# todo genquad(op, x, y, z) create next quad
# todo newtemp() variables like T_1etc
# todo emptylist() create empty list of quads's tags
# todo makelist(x) create new list of quads' tags

# todo token_type variable in lex() check it

# todo the comments open closed flags dont need


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
number_tk, end_of_program_tk = "number", "."

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
symbols = ["+", "-", "*", "/", "=", ",", "[", "{", "(", "]", "}", ")"]
keywords = ["program", "declare", "function", "procedure", "in", "inout", "if", "else", "while", "switchcase",
            "case", "default", "forcase", "incase", "return", "call", "print", "input", "or", "and", "not"]
EOF = ''
char = ""
token_type = ""
file = open(str(sys.argv[1]))
line = 1
token = ""
previous_token = ""
next_char = False  # flag if the next char had already been ready or not
comments_closed = True
multiple_statements = True  # flag for multiple statements, we use this statement because the grammar between single
token_string = ""

next_quad_number = 0
quads = []
temp_var_number = 0
program_name = ''
subprogram_name = ''
procedures = []
functions = []
declare_variables = []


def check_forbidden_char():
    if char in forbidden_char:
        print("Forbidden character '%s'" % char)
        print("line:", line)
        sys.exit(0)


def avoid_white_spaces():
    global line, char, next_char
    if char == "\n":
        line += 1
        next_char = False
        return True
    if char == " " or char == "\t":
        next_char = False
        return True


# helpful functions for the middle code

def nextquad():
    global next_quad_number

    return str(next_quad_number)


def genquad(op, x, y, z):
    global next_quad_number

    number = next_quad_number
    next_quad_number = next_quad_number + 1
    temp = [str(number), op, x, y, z]
    quads.append(temp)


def newtemp():
    global temp_var_number

    t = "T_" + str(temp_var_number)
    declare_variables.append(t)
    temp_var_number = temp_var_number + 1

    return t


def emptylist():
    return []


def makelist(x):
    list = []
    list.append(x)
    return list


def mergelist(l1, l2):
    return l1 + l2


def backpatch(alist, z):
    global quads

    for list1 in quads:
        if list1[0] in alist:
            list1[4] = z
    # for quad in quads:
    #     # checking if the index of the quad is in
    #     if quads.index(quad) in alist:
    #         quad[3] = z


# lexical analyzer
def lex():
    global char, file, line, token_string, token_type, next_char, comments_closed
    state = ST_START
    number = 0
    alphanumeric = ""

    while True:

        if not next_char:  # if next char hasn't been read
            char = file.read(1)
        check_forbidden_char()

        # they cause issues if they r here
        # if char == "\n":
        #     line += 1
        #     next_char = False
        #     continue
        # if "" or char == "\t":
        #     next_char = False
        #     continue

        # start of the automata
        # being in start state
        # if state == ST_START and char == "\n":
        #     state = ST_START
        #     line += 1
        #     continue
        if state == ST_START and avoid_white_spaces():
            continue
        # todo is this really needed?
        if state == ST_START and char == "return":
            next_char = False
            continue
        elif state == ST_START and char.isalpha():
            next_char = False
            state = ST_LETTER
            alphanumeric = char
            continue
        elif state == ST_START and char.isdigit():
            next_char = False
            number = char
            state = ST_DIGIT
            continue
        elif state == ST_START and char == "<":
            next_char = False
            state = ST_LOWER
            continue
        elif state == ST_START and char == ">":
            next_char = False
            state = ST_GREATER
            continue
        elif state == ST_START and char == ":":
            next_char = False
            state = ST_ASGN
            continue
        elif state == ST_START and char == "#":
            next_char = False
            state = ST_COMMENT
            continue
            # char = file.read(1)
            # # todo this is wrong fix
            # # using this while loop because without this loop program is not counting the lines after every '\n'
            # while char != ".":
            #     if char == "#":
            #         break
            #     elif char == EOF:
            #         print("Comments haven't closed")
            #         sys.exit(0)
            #     avoid_white_spaces()
            #     char = file.read(1)
            # next_char = True
            # state = ST_START
            # comments_closed = not comments_closed
            # continue
        elif state == ST_START and char in symbols:
            next_char = False
            token_string = char
            token_type = char
            print(token_string)
            return token_type
        # todo is not needed probably
        elif state == ST_START and char == ";":
            next_char = False
            token_string = char
            token_type = char
            print(token_string)
            return char
        # being in letter state
        # todo is not needed probably, but i have to put ';' in symbols
        # elif state == ST_LETTER and char == ";":
        #     next_char = False
        #     token_type = char
        #     return char
        # check for alphanumerics
        elif state == ST_LETTER and (char.isalpha() or char.isdigit()):
            while char.isdigit() or char.isalpha():
                alphanumeric = str(alphanumeric) + str(char)
                if len(alphanumeric) <= 30:
                    char = file.read(1)
                    continue
                else:
                    print("Invalid alphanumeric \nThe length of an alphanumeric should be lower or equal of 30 ")
                    print("line: ", line)
                    sys.exit(0)

            next_char = True  # lex has read already a char that we haven't pass from our automata yet
            check_forbidden_char()  # todo not needed
            avoid_white_spaces()
            if alphanumeric in keywords:
                token_type = alphanumeric
                token_string = alphanumeric
                print(token_string)
                return token_type
            else:
                token_string = alphanumeric
                token_type = id_tk
                print(token_string)
                return token_type

        # check if there is only one character alpha
        elif state == ST_LETTER and not (char.isalpha() or char.isdigit()):
            next_char = True
            avoid_white_spaces()
            # next_char = True todo this is wrong if we have a white space and 1-letter word maybe it needs an if bcs there r bigger words
            if alphanumeric in keywords:
                token_string = alphanumeric
                token_type = alphanumeric
                print(token_string)
                return token_type
            else:
                token_string = alphanumeric
                token_type = id_tk
                print(token_string)
                return token_type

        # todo return to syntax analyzer
        # being in digit state
        elif state == ST_DIGIT and char.isdigit():
            while char.isdigit():
                number = int(str(number) + str(char))
                # todo maybe it need range +1 at the second
                if number in range(- pow(2, 32) - 1, pow(2, 32) - 1):
                    char = file.read(1)
                    continue
                    # if char == "\n":
                    #     line += 1
                    #     continue
                else:
                    print("Invalid constant \nConstants should be in the range of –(2^32 − 1) to 2^32 − 1")
                    print("line: ", line)
                    sys.exit(0)
            # todo return to syntax analyzer
            next_char = True
            avoid_white_spaces()
            if char.isalpha():
                print("Invalid character, letter after number")
                print("line: ", line)
                sys.exit(0)
            else:
                token_string = number
                token_type = number_tk
                print(token_string)
                return token_type  # return number

        elif state == ST_DIGIT and char.isalpha():
            print("Invalid character, letter after number")
            print("line: ", line)
            sys.exit(0)
        # check if there is only 1 number
        elif state == ST_DIGIT and not (char.isalpha() or char.isdigit()):
            next_char = True
            avoid_white_spaces()
            token_string = number
            token_type = number_tk
            print(token_string)
            return token_type
        # being in lower state

        elif state == ST_LOWER and char == "=":
            token_string = lower_equal_tk
            token_type = lower_equal_tk
            next_char = False
            print(token_string)
            return token_type
        elif state == ST_LOWER and char == ">":
            token_string = not_equal_tk
            token_type = not_equal_tk
            next_char = False
            print(token_string)
            return token_type
        elif state == ST_LOWER and char not in ["=", ">"]:
            token_string = lower_tk
            token_type = lower_tk
            next_char = True
            avoid_white_spaces()
            print(token_string)
            return token_type

        # being in greater state
        elif state == ST_GREATER and char == "=":
            token_string = greater_equal_tk
            token_type = greater_equal_tk
            next_char = False
            print(token_string)
            return token_type
        elif state == ST_GREATER and char not in ["=", "<"]:
            token_type = greater_tk
            token_string = greater_tk
            next_char = True
            avoid_white_spaces()
            print(token_string)
            return token_type
        elif state == ST_GREATER and char == "<":
            print("The >< is invalid")
            print("line: ", line)
            sys.exit(0)

        # being in asgn state
        elif state == ST_ASGN and char == "=":
            token_type = assignment_tk
            token_string = assignment_tk
            next_char = False
            print(token_string)
            return token_type
        elif state == ST_ASGN and char != "=":
            print("Syntax error: after ':' should always follow '='")
            print("line: ", line)
            sys.exit(0)
        elif state == ST_COMMENT:
            while 1:
                if char == "#":
                    break
                elif char == EOF or char == ".":
                    print("Comments haven't closed")
                    sys.exit(0)
                avoid_white_spaces()
                char = file.read(1)
            next_char = False
            state = ST_START
            # todo here its better to do return OR is it better bcs we want to ignore the comments?
            continue
        if char == ".":
            char = file.read(1)
            # if there are white characters after the . then ignore them
            while avoid_white_spaces():
                char = file.read(1)
            next_char = True
            print(token_string)
            return end_of_program_tk

            # return EOF
        elif char == EOF:
            next_char = False
            print(token_string)
            return EOF


# syntax analyzer

'''
# " program " is the starting symbol
    program : program ID block .
'''


def program():
    global line, token, program_name, token_string
    token = lex()
    if token == program_tk:
        token = lex()
        if token == id_tk:
            program_name = token_string
            token = lex()
            block(program_name)
        else:
            print("program name expected \n line:", line)
            sys.exit(0)
    else:
        print("the keyword 'program' was expected\n line:", line)
        sys.exit(0)
    if token == end_of_program_tk:
        if char == EOF:
            # return end_of_program_tk
            print("End of the program")
            # sys.exit(0)
        elif char != EOF:
            print("Error EOF - No characters should exist after character '.' ")
            print("The char '.' symbolize the end of the program")
            print("line: ", line)
            sys.exit(0)
        # todo maybe it needs if and not elif
        # todo probably not needed
        # elif not comments_closed:
        #     print("Comments haven't closed")
        #     sys.exit(0)
    elif token == EOF:
        print("Error EOF - The program should finish by the char '.'")
        sys.exit(0)


'''
# a block with declarations , subprogram and statements
block : declarations subprograms statements
'''


def block(name):
    global program_name

    declarations()
    subprograms()

    if name == program_name:
        genquad("begin_block", name, "_", "_")
        statements()
        genquad("halt", "_", "_", "_")
        genquad("end_block", name, "_", "_")
    elif name == subprogram_name:
        genquad("begin_block", name, "_", "_")
        statements()
        genquad("end_block", name, "_", "_")


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
        declare_variables.append(token_string)
        token = lex()
        while token == comma_tk:
            token = lex()
            if token == id_tk:
                declare_variables.append(token_string)
                token = lex()
            else:
                print("Error: was expected variable\n line:", line)
                sys.exit(0)
    else:
        print("Error: was expected variable\n line:", line)


'''
# zero or more subprograms allowed
subprograms : ( subprogram )∗
'''


def subprograms():
    global token, line
    while token == function_tk or token == procedure_tk:
        # subprogram_type = token
        # token = lex()
        subprogram()


'''
# a subprogram is a function or a procedure ,
# followed by parameters and block
subprogram : function ID ( formalparlist ) block
| procedure ID ( formalparlist ) block
'''


def subprogram():
    global token, line, token_string
    # if token == function_tk or token == procedure_tk:
    #     token = lex()
    subprogram_type = token
    token = lex()
    if token == id_tk:
        # we need this info for the callstat later
        name = token_string
        if subprogram_type == function_tk:
            functions.append(name)
        elif subprogram_type == procedure_tk:
            procedures.append(name)
        token = lex()

        if token == left_parenthesis_tk:
            token = lex()
            formalparlist()
            if token == right_parenthesis_tk:
                token = lex()
                block(subprogram_name)
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

    if token == in_tk or token == inout_tk:
        # TODO i can do it like previously in the subprograms, lex() and delete the if in the formalparitem
        # todo ill do it like that
        formalparitem()
        while token == comma_tk:
            token = lex()
            formalparitem()


'''
# a formal parameter (" in ": by value , " inout " by reference )
formalparitem : in ID
| inout ID
'''


def formalparitem():
    global line, token

    if token == in_tk or token == inout_tk:
        token = lex()
        if token == id_tk:
            token = lex()
        else:
            print("Error: Missing variable\nline:", line)
            sys.exit(0)
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
    global line, token, multiple_statements
    if token == left_brace_tk:
        token = lex()
        statement()
        while token == semicolon_tk:
            token = lex()
            statement()
        if token == right_brace_tk:
            token = lex()

        else:
            print("Syntax error: '}' was expected or ';' missing at the end of a statement\n line", line)
            sys.exit(0)
    else:
        statement()
        # this condition checks if we are in single statement. If we are then it checks if there is ';' at the end of
        # the statement. The flag multiple_statements change value inside the statement()
        if not multiple_statements:
            if token == semicolon_tk:
                token = lex()
            else:
                print("Syntax error: ';' was expected\n line:", line)
                sys.exit(0)
            multiple_statements = True


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
    global token, line, multiple_statements
    if token == id_tk:
        assignStat()
        multiple_statements = False
    elif token == if_tk:
        ifStat()
        multiple_statements = False
    elif token == while_tk:
        whileStat()
        multiple_statements = False
    elif token == switchcase_tk:
        switchcaseStat()
        multiple_statements = False
    elif token == forcase_tk:
        forcaseStat()
        multiple_statements = False
    elif token == incase_tk:
        incaseStat()
        multiple_statements = False
    elif token == call_tk:
        callStat()
        multiple_statements = False
    elif token == return_tk:
        returnStat()
        multiple_statements = False
    elif token == input_tk:
        inputStat()
        multiple_statements = False
    elif token == print_tk:
        printStat()
        multiple_statements = False


'''
# assignment statement
assignStat : ID := expression
'''


def assignStat():
    global token, line, previous_token, token_string

    if token == id_tk:
        id_string = token_string
        token = lex()
        if token == assignment_tk:
            token = lex()
            e_place = expression()
            genquad(assignment_tk, e_place, "_", id_string)
        else:
            print("Syntax error: ':=' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Error: Missing variable\n line:", line)
        sys.exit(0)


'''
# if statement
ifStat : if ( condition ) statements elsepart
'''


def ifStat():
    global token, line
    condition_true = []
    condition_false = []
    if token == if_tk:
        token = lex()
        if token == left_parenthesis_tk:
            token = lex()
            condition_true, condition_false = condition()
            # condition()
            if token == right_parenthesis_tk:
                token = lex()

                backpatch(condition_true, nextquad())

                statements()

                if_list = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                backpatch(condition_false, nextquad())

                elsepart()

                backpatch(if_list, nextquad())

            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '(' was expected\n line:", line)
            sys.exit(0)
    # else:
    #     print("Syntax error: 'if' was expected\nline: ", line)
    #     sys.exit(0)


'''
elsepart : else statements
| ε
'''


def elsepart():
    global token, line
    if token == else_tk:
        token = lex()
        statements()


'''
# while statement
whileStat : while ( condition ) statements
'''


def whileStat():
    global token, line

    if token == while_tk:
        token = lex()
        if token == left_parenthesis_tk:
            token = lex()
            bquad = nextquad()
            b_true, b_false = condition()
            backpatch(b_true, nextquad())
            if token == right_parenthesis_tk:
                token = lex()
                statements()
                genquad("jump", "_", "_", bquad)
                backpatch(b_false, nextquad())
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
        exitlist = emptylist()
        while token == case_tk:
            token = lex()
            if token == left_parenthesis_tk:
                token = lex()
                cond_true, cond_false = condition()
                if token == right_parenthesis_tk:
                    token = lex()
                    backpatch(cond_true, nextquad())
                    statements()
                    e = makelist(nextquad())
                    genquad('jump', '_', '_', '_')
                    exitlist = mergelist(exitlist, e)
                    backpatch(cond_false, nextquad())
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)

        if token == default_tk:
            token = lex()
            statements()
            backpatch(exitlist, nextquad())
        else:
            print("Syntax error: 'default' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: 'switchcase' was expected\n line:", line)
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
        p1Quad = nextquad()
        exitlist = emptylist()

        while token == case_tk:
            token = lex()
            if token == left_parenthesis_tk:
                token = lex()
                cond_true, cond_false = condition()
                if token == right_parenthesis_tk:
                    token = lex()
                    backpatch(cond_true, nextquad())
                    statements()
                    e = makelist(nextquad())
                    exitlist = mergelist(exitlist, e)
                    genquad('jump', '_', '_', '_')
                    backpatch(cond_false, nextquad())
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)

        if token == default_tk:
            token = lex()
            statements()
            genquad("jump", "_", "_", p1Quad)
            backpatch(exitlist, nextquad())
        else:
            print("Syntax error: 'default' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: 'forcase' was expected\n line:", line)
        sys.exit(0)


'''
# incase statement
incaseStat : incase
( case ( condition ) statements )∗
'''


def incaseStat():
    global token, line
    if token == incase_tk:
        token = lex()
        w = newtemp()
        p1Quad = nextquad()
        genquad(assignment_tk, 1, "_", w)
        while token == case_tk:
            token = lex()
            if token == left_parenthesis_tk:
                token = lex()
                cond_true, cond_false = condition()
                if token == right_parenthesis_tk:
                    token = lex()
                    backpatch(cond_true, nextquad())
                    genquad(assignment_tk, 0, "_", w)
                    statements()
                    backpatch(cond_false, nextquad())
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)
        genquad("=", w, 0, p1Quad)
    else:
        print("Syntax error: 'incaseStat' was expected\n line:", line)
        sys.exit(0)


'''
# return statement
returnStat : return( expression )
'''


def returnStat():
    global token, line
    if token == return_tk:
        token = lex()
        if token == left_parenthesis_tk:
            token = lex()
            e_place = expression()
            genquad("retv", e_place, "_", "_")
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
            call_name = token_string

            token = lex()
            if token == left_parenthesis_tk:
                token = lex()
                actualparlist()
                if token == right_parenthesis_tk:
                    token = lex()

                    # checking if the subprogram is function or procedure
                    for name in functions:
                        if call_name == name:
                            w = newtemp()
                            genquad("par", w, "RET", "_")
                            genquad("call", call_name, "_", "_")
                    for name in procedures:
                        if call_name == name:
                            genquad("call", call_name, "_", "_")
                else:
                    print("Syntax error: ')' was expected\n line:", line)
                    sys.exit(0)
            else:
                print("Syntax error: '(' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: Missing variable\n line:", line)
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
            token = lex()
            e_place = expression()
            genquad("out", e_place, "_", "_")
            if token == right_parenthesis_tk:
                token = lex()
            else:
                print("Syntax error: ')' was expected\n line:", line)
                sys.exit(0)
        else:
            print("Syntax error: '(' was expected\n line:", line)
            sys.exit(0)
    else:
        print("Syntax error: 'print' was expected\n line:", line)
        sys.exit(0)


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
                id_place = token_string
                token = lex()
                genquad("inp", id_place, "_", "_")
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

    if token == in_tk or token == inout_tk:
        actualparitem()
        while token == comma_tk:
            token = lex()
            actualparitem()
    elif token == id_tk:
        print("Syntax error: 'in' or 'inout' was expected\n line:", line)
        sys.exit(0)


'''
# an actual parameter (" in ": by value , " inout " by reference )
actualparitem : in expression
            | inout ID
'''


def actualparitem():
    global token, line
    if token == in_tk:
        token = lex()
        ex1 = expression()
        genquad("par", ex1, "CV", "_")
    elif token == inout_tk:
        token = lex()
        if token == id_tk:
            id_name = token_string
            genquad("par", id_name, "REF", "_")
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
    # boolterm()
    boolterm1_true, boolterm1_false = boolterm()
    condition_true, condition_false = boolterm1_true, boolterm1_false
    while token == or_tk:
        backpatch(condition_false, nextquad())  # If you find or and its is false go to the next one

        token = lex()

        boolterm2_true, boolterm2_false = boolterm()
        condition_true = mergelist(condition_true, boolterm2_true)
        condition_false = boolterm2_false  # Get the false list from the last boolterm

        # boolterm()
    return condition_true, condition_false


'''
# term in boolean expression
boolterm : boolfactor ( and boolfactor )∗
'''


def boolterm():
    global token, line

    boolfactor1_true, boolfactor1_false = boolfactor()
    boolterm_true, boolterm_false = boolfactor1_true, boolfactor1_false

    # boolfactor()
    while token == and_tk:
        backpatch(boolterm_true, nextquad())
        token = lex()
        boolfactor2_true, boolfactor2_false = boolfactor()
        boolterm_false = mergelist(boolterm_false, boolfactor2_false)
        boolterm_true = boolfactor2_true
    return boolterm_true, boolterm_false
    # token = lex()
    # boolfactor()


'''
# factor in boolean expression
boolfactor : not [ condition ]
            | [ condition ]
            | expression REL_OP expression
'''


def boolfactor():
    global token, line

    boolfactor_true = []
    boolfactor_false = []

    if token == not_tk:
        token = lex()
        if token == left_bracket_tk:
            token = lex()
            boolfactor_false, boolfactor_true = condition()
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
        boolfactor_false, boolfactor_true = condition()
        # condition()
        if token == right_bracket_tk:
            token = lex()
        else:
            print("Syntax error: ']' was expected\n line:", line)
            sys.exit(0)
    else:
        ex1 = expression()
        relop = token_string
        rel_op()
        ex2 = expression()
        boolfactor_true = makelist(nextquad())
        genquad(relop, ex1, ex2, "_")
        boolfactor_false = makelist(nextquad())
        genquad("jump", "_", "_", "_")
        # expression()
        # rel_op()
        # expression()
    return boolfactor_true, boolfactor_false


'''
# arithmetic expression
expression : optionalSign term ( ADD_OP term )∗
'''


def expression():
    global token
    optionalSign()
    t1_place = term()

    while token == add_tk or token == minus_tk:
        math_symbol = token
        w = newtemp()
        add_op()
        t2_place = term()
        # if previous_token == add_tk:
        #     genquad("+", t1_place, t2_place, w)  # var = t1 + t2
        # else:
        #     genquad("-", t1_place, t2_place, w)
        genquad(math_symbol, t1_place, t2_place, w)
        t1_place = w

    return t1_place


'''
# term in arithmetic expression
term : factor ( MUL_OP factor )∗
'''


def term():
    t1_place = factor()
    while token == multiple_tk or token == divide_tk:
        math_symbol = token
        w = newtemp()
        mull_op()
        t2_place = factor()
        genquad(math_symbol, t1_place, t2_place, w)
        t1_place = w
    return t1_place


'''
# factor in arithmetic expression
factor : INTEGER
        | ( expression )
        | ID idtail
'''


def factor():
    global token, line, previous_token, token_string

    factor_value = " "
    if token == number_tk:
        factor_value = token_string
        token = lex()
        # previous_token = token
    elif token == left_parenthesis_tk:
        token = lex()
        factor_value = expression()
        if token == right_parenthesis_tk:
            token = lex()
        else:
            print("Syntax error: ')' was expected\n line:", line)
            sys.exit(0)
    elif token == id_tk:
        factor_value = token_string
        token = lex()
        # previous_token = token
        idtail()
    else:
        print("Error: the code is not following the 'factor' grammar\nfactor : INTEGER | ( expression ) | ID idtail")
        print("line", line)
        sys.exit(0)
    return factor_value


'''
# follows a function of procedure ( parethnesis and parameters )
idtail : ( actualparlist )
        | ε
'''


def idtail():
    global token, line
    if token == left_parenthesis_tk:
        token = lex()
        actualparlist()
        if token == right_parenthesis_tk:
            token = lex()
        else:
            print("Syntax error: ')' was expected\n line:", line)
            sys.exit(0)


'''
# sumbols "+" and " -" ( are optional )
optionalSign : ADD_OP
            | ε
'''


def optionalSign():
    if token == add_tk or token == minus_tk:
        add_op()


'''
REL_OP : = | <= | >= | > | < | <>
'''


def rel_op():
    global token, line
    if token == equal_tk or token == lower_equal_tk or token == greater_equal_tk:
        token = lex()
    elif token == greater_tk or token == lower_tk or token == not_equal_tk:
        token = lex()
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
        sys.exit(0)


'''
MUL_OP : * | /
'''


def mull_op():
    global token, line
    if token == multiple_tk or token == divide_tk:
        token = lex()
    else:
        print("Syntax error: '*' or '/' operator was expected\nline", line)


def comments_c(quad, c_file):
    c_file.write(" // (")
    for string in quad[1:]:
        c_file.write(string + "\t")
    c_file.write(")")


def convert_c_code(c_file):
    # intFile.write(str(quads.index(quad)) + " ")
    c_file.write("int main()" + "\n{\n")

    # declare variables
    c_file.write("int ")
    c_file.write(declare_variables[0])
    for variable in declare_variables[1:]:
        c_file.write(", " + variable)
    c_file.write(";\n")

    for quad in quads:
        c_file.write("L_" + quad[0] + ": ")

        if quad[1] == "begin_block":
            c_file.write("\n")
            continue
        elif quad[1] == "end_block":
            c_file.write("\n")
            continue
        elif quad[1] == "halt":
            c_file.write("return 0")
        elif quad[1] == "jump":
            c_file.write("goto L_" + quad[4])
        elif quad[1] in ["+", "/", "-", "*"]:
            c_file.write(quad[4] + " = " + quad[2] + quad[1] + quad[3])
        elif quad[1] == assignment_tk:
            c_file.write(quad[4] + " = " + quad[2])
        elif quad[1] in ["<", ">", "<=", ">="]:
            c_file.write("if( " + quad[2] + quad[1] + quad[3] + " ) " + "goto L_" + quad[4])
        elif quad[1] == equal_tk:
            c_file.write("if( " + quad[2] + quad[1] + quad[1] + quad[3] + " ) " + "goto L_" + quad[4])
        elif quad[1] == not_equal_tk:
            c_file.write("if( " + quad[2] + "!=" + quad[3] + " ) " + "goto L_" + quad[4])
        elif quad[1] == "retv":
            c_file.write(return_tk + " " + quad[2])
        elif quad[1] == "out":
            if quad[2] in declare_variables:
                c_file.write("printf( '%d', " + quad[2] + " )")
            else:
                c_file.write("printf( " + quad[2] + " )")
        elif quad[1] == "inp":
            c_file.write("scanf( '%d', " + quad[2] + ")")
        else:
            continue
        comments_c(quad, c_file)
        c_file.write("\n")
    c_file.write("}")
    c_file.close()


if __name__ == '__main__':
    program()

    print("The array of the intermediate code is:")
    for quad in quads:
        print("%-5s %-15s %-10s %-10s %s" % (quads.index(quad), quad[0], quad[1], quad[2], quad[3]))
        # create_declarelist(l)

    # Create the int file
    intFile = open("test.int", "w")
    for l1 in quads:
        # intFile.write(str(quads.index(l1)) + " ")
        for string in l1:
            intFile.write(str(string) + " ")
        intFile.write("\n")
    intFile.close()

    # create the c file
    c_file = open("test.c", "w")
    convert_c_code(c_file)
