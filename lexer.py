import sys, string

class Token:
    def __init__(self, kind, value, line=None, position=None):
        self.kind = kind
        self.value = value
        self.line = line
        self.position = position

def lexProgram(program):
    tokenList = []
    line = 1
    position = 0
    str = False
    keyword_cache = ""
    i = 0
    while i < len(program):
        if str: 
            str = validateString(program[i])
        elif program[i] in "(){}+": 
            tokenList.append(singleCharTokens(program[i]))
            tokenList[-1].line = line
            tokenList[-1].position = position
        elif i+1 < len(program) and program[i]+program[i+1] == "!=": 
            tokenList.append(Token("BoolOp", "!=", line, position))
            i+=1
        elif i+1 < len(program) and program[i]+program[i+1] == "==": 
            tokenList.append(Token("BoolOp", "==", line, position))
            i+=1
        elif program[i] == "=": 
            tokenList.append(Token("AssignOp", "=", line, position))
        elif program[i] == "\"": 
            str = True
        elif program[i] in "0123456789": 
            tokenList.append(Token("Digit", program[i], line, position))
        elif program[i] in string.ascii_lowercase:
            if i+1 < len(program) and program[i+1] not in string.ascii_lowercase:
                tokenList.append(check_keyword(keyword_cache))
                tokenList[-1].line = line
                tokenList[-1].position = position
            else: keyword_cache+=program[i]
        elif program[i] == " ":
            pass
        elif program[i] == "\n":
            line+=1
            position = 1
        elif program[i] == "$":
            tokenList.append(Token("EOF", "$", line, position))
            if i != len(program) - 1 and program[i+1] != '\n':
                print("Warning! EOF out of nowhere!");
        position+=1
        i+=1
    return tokenList

def validateString(c):
    if c == "\"":
        return False
    elif c not in string.ascii_lowercase:
        sys.exit("Error!", c, "is not a valid string character!")
    else:
        return true

def singleCharTokens(c):
    if c == "(": return Token("OpenParen", "(")
    if c == ")": return Token("CloseParen", ")")
    if c == "{": return Token("OpenBrace", "{")
    if c == "}": return Token("CloseBrace", "}")
    if c == "+": return Token("IntOp", "+")

def check_keyword(cache):
    if cache in ["boolean", "string", "int"]: kind = "IdType"
    elif cache in ["true", "false"]: kind = "Boolean"
    elif cache == "if": kind = "If"
    elif cache == "while": kind = "While"
    elif cache == "print": kind = "Print"
    elif len(cache) == 1: kind = "Id"
    else: sys.exit("Error! Not a valid keyword!")
    return Token(kind, cache)
