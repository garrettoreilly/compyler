import sys, string

def lex_program(program):
    token_list = []
    line = 1
    position = 1
    char_list = False
    cl_start = 0
    i = 0
    while i < len(program):
        if char_list: 
            char_list = validate_string(program[i])
            if not char_list:
                token_list.append({"type": "CharList", "value": program[cl_start:i+1],
                        "line": line, "position": position - (i+1 - cl_start)})
        elif program[i] in "(){}+": 
            token_list.append(single_char_tokens(program[i]))
            token_list[-1]["line"] = line
            token_list[-1]["position"] = position
        elif i+1 < len(program) and program[i]+program[i+1] == "!=": 
            token_list.append({"type": "BoolOp", "value": "!=", "line": line, "position": position})
            i+=1
        elif i+1 < len(program) and program[i]+program[i+1] == "==": 
            token_list.append({"type": "BoolOp", "value": "==", "line": line, "position": position})
            i+=1
        elif program[i] == "=": 
            token_list.append({"type": "AssignOp", "value": "=", "line": line, "position": position})
        elif program[i] == "\"": 
            char_list = True
            cl_start = i
        elif program[i] in "0123456789": 
            token_list.append({"type": "Digit", "value": program[i], "line": line,
                "position": position})
        elif program[i] in string.ascii_lowercase:
            new_token = check_keyword(program[i:])
            new_token["line"] = line
            new_token["position"] = position
            token_list.append(new_token)
            i+=(len(new_token["value"])-1)
        elif program[i] == " ":
            pass
        elif program[i] == "\n":
            line+=1
            position = 0
        elif program[i] == "$":
            token_list.append({"type": "EOF", "value": "$", "line": line, "position": position})
            if program[i+1:] != [] and program[i+1:] != "\n":
                print("Warning! EOF out of nowhere!");
            return token_list
        else:
            sys.exit("Error! Invalid token at line %d, position %d: %c" % (line, position,
                program[i]))
        position+=1
        i+=1

    if token_list[-1]["value"] != "$":
        print("Warning! No EOF in file!")
        token_list.append({"type": "EOF", "value": "$", "line": line, "position": position})

    return token_list

def validate_string(c):
    if c == "\"":
        return False
    elif c not in string.ascii_lowercase and c != " ":
        sys.exit("Error!", c, "is not a valid string character!")
    else:
        return True

def single_char_tokens(c):
    if c == "(": 
        return {"type": "OpenParen", "value": "("}
    if c == ")": 
        return {"type": "CloseParen", "value": ")"}
    if c == "{": 
        return {"type": "OpenBrace", "value": "{"}
    if c == "}": 
        return {"type": "CloseBrace", "value": "}"}
    if c == "+": 
        return {"type": "IntOp", "value": "+"}

def check_keyword(program):
    if program[:7] == "boolean":
        return {"type": "IdType", "value": "boolean"}
    elif program[:6] == "string":
        return {"type": "IdType", "value": "string"}
    elif program[:5] == "while":
        return {"type": "While", "value":"while"}
    elif program[:5] == "print":
        return {"type": "Print", "value": "print"}
    elif program[:5] == "false":
        return {"type": "BoolVal", "value": "false"}
    elif program[:4] == "true":
        return {"type": "BoolVal", "value": "true"}
    elif program[:3] == "int":
        return {"type": "IdType", "value": "int"}
    elif program[:2] == "if":
        return {"type": "If", "value": "if"}
    else:
        return {"type": "Id", "value": program[0]}
