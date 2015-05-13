import sys, string

def lex_program(program):
    token_list = []
    line = 1
    position = 0
    str = False
    i = 0
    while i < len(program):
        if str: 
            str = validate_string(program[i])
        elif program[i] in "(){}+": 
            token_list.append(single_char_tokens(program[i]))
            token_list[-1] += (line, position)
        elif i+1 < len(program) and program[i]+program[i+1] == "!=": 
            token_list.append(("BoolOp", "!=", line, position))
            i+=1
        elif i+1 < len(program) and program[i]+program[i+1] == "==": 
            token_list.append(("BoolOp", "==", line, position))
            i+=1
        elif program[i] == "=": 
            token_list.append(("AssignOp", "=", line, position))
        elif program[i] == "\"": 
            str = True
        elif program[i] in "0123456789": 
            token_list.append(("Digit", program[i], line, position))
        elif program[i] in string.ascii_lowercase:
            new_token = check_keyword(program[i:])
            new_token += (line, position)
            token_list.append(new_token)
            i+=(len(new_token[1])-1)
        elif program[i] == " ":
            pass
        elif program[i] == "\n":
            line+=1
            position = 1
        elif program[i] == "$":
            token_list.append(("EOF", "$", line, position))
            if program[i+1:] != [] and program[i+1:] != "\n":
                print("Warning! EOF out of nowhere!");
            return token_list
        position+=1
        i+=1

    if token_list[-1][1] != "$":
        print("Warning! No EOF in file!")
        token_list.append(("EOF", "$", line, position))

    return token_list

def validate_string(c):
    if c == "\"":
        return False
    elif c not in string.ascii_lowercase:
        sys.exit("Error!", c, "is not a valid string character!")
    else:
        return True

def single_char_tokens(c):
    if c == "(": 
        return ("OpenParen", "(")
    if c == ")": 
        return ("CloseParen", ")")
    if c == "{": 
        return ("OpenBrace", "{")
    if c == "}": 
        return ("CloseBrace", "}")
    if c == "+": 
        return ("IntOp", "+")

def check_keyword(program):
    if program[:7] == "boolean":
        return ("IdType", "boolean")
    elif program[:6] == "string":
        return ("IdType", "string")
    elif program[:5] == "while":
        return ("While", "while")
    elif program[:5] == "print":
        return ("Print", "print")
    elif program[:5] == "false":
        return ("Boolean", "false")
    elif program[:4] == "true":
        return ("Boolean", "ture")
    elif program[:3] == "int":
        return ("IdType", "int")
    elif program[:2] == "if":
        return ("If", "if")
    else:
        return ("Id", program[0])
