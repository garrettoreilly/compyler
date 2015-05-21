import sys, Lexer

def parse_program(token_list, verbosity):
    if verbosity:
        print("Looking for program...")
    result = parse_block(token_list, verbosity)
    if result[0]["type"] == "EOF":
        print("Parse successful!")
    else:
        sys.exit("Error! Expected %s, received %s\nLine %d, position %d" 
                % (result[0]["value"], result[1]["type"], result[1]["line"], result[1]["position"]))

def parse_block(token_list, verbosity):
    if verbosity:
        print("Looking for block...")
    result = get_terminal(token_list, "OpenBrace", verbosity)
    if result[0]["type"] is "Error":
        return result
    result = parse_statement_list(result, verbosity)
    result = get_terminal(result, "CloseBrace", verbosity)
    return result

def parse_statement_list(token_list, verbosity):
    if verbosity:
        print("Looking for statement list...")
    if token_list[0]["type"] in ["CloseBrace", "Error"]:
        return token_list
    else:
        result = parse_statement(token_list, verbosity)
        if result[0]["type"] is "Error":
            return result
        result = parse_statement_list(result, verbosity)
        return result

def parse_statement(token_list, verbosity):
    if verbosity:
        print("Looking for statement...")
    if token_list[0]["type"] is "Error":
        return token_list
    result_list = [parse_print_statement(token_list, verbosity), 
            parse_assign_statement(token_list, verbosity), parse_var_decl(token_list, verbosity), 
            parse_while_statement(token_list, verbosity), parse_if_statement(token_list, verbosity), 
            parse_block(token_list, verbosity)]

    for result in result_list:
        if result[0]["type"] is not "Error":
            return result

    return [{"type": "Error", "value": "Statement"}] + token_list

def parse_print_statement(token_list, verbosity):
    if verbosity:
        print("Looking for print statement...")
    if token_list[0]["type"] is "Error":
        return result
    result = get_terminal(token_list, "Print", verbosity)
    if result[0]["type"] is "Error":
        return result
    result = get_terminal(result, "OpenParen", verbosity)
    result = parse_expr(result, verbosity)
    result = get_terminal(result, "CloseParen", verbosity)
    return result

def parse_assign_statement(token_list, verbosity):
    if verbosity:
        print("Looking for assignment statement...")
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "Id", verbosity)
    result = get_terminal(result, "AssignOp", verbosity)
    result = parse_expr(result, verbosity)
    return result

def parse_var_decl(token_list, verbosity):
    if verbosity:
        print("Looking for variable declaration...")
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "IdType", verbosity)
    result = get_terminal(result, "Id", verbosity)
    return result

def parse_while_statement(token_list, verbosity):
    if verbosity:
        print("Looking for while statement...")
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "While", verbosity)
    if result[0]["type"] is "Error":
        return result
    result = parse_bool_expr(result, verbosity)
    result = parse_block(result, verbosity)
    return result

def parse_if_statement(token_list, verbosity):
    if verbosity:
        print("Looking for if statement...")
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "If", verbosity)
    if result[0]["type"] is "Error":
        return result
    result = parse_bool_expr(result, verbosity)
    result = parse_block(result, verbosity)
    return result

def parse_expr(token_list, verbosity):
    if verbosity:
        print("Looking for expression...")
    if token_list[0]["type"] is "Error":
        return token_list
    result_list = [parse_int_expr(token_list, verbosity), parse_string_expr(token_list, verbosity),
            parse_bool_expr(token_list, verbosity), get_terminal(token_list, "Id", verbosity)]

    for result in result_list:
        if result[0]["type"] is not "Error":
            return result

    return [{"type": "Error", "value": "Expression"}] + token_list

def parse_int_expr(token_list, verbosity):
    if verbosity:
        print("Looking for integer expression...")
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "Digit", verbosity)
    if result[0]["type"] is "Error":
        return result
    result = get_terminal(result, "IntOp", verbosity)
    if result[0]["type"] is not "Error":
        result = parse_expr(result, verbosity)
    else:
        result = result[1:]
    return result

def parse_string_expr(token_list, verbosity):
    if verbosity:
        print("Looking for string expression...")
    if token_list[0]["type"] is "Error":
        return token_list
    elif token_list[0]["type"] is not "CharList":
        return [{"type": "Error", "value": "CharList"}] + token_list
    else:
        result = get_terminal(token_list, "CharList", verbosity)
        return result

def parse_bool_expr(token_list, verbosity):
    if verbosity:
        print("Looking for boolean expression...")
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "OpenParen", verbosity)
    if result[0]["type"] is not "Error":
        result = parse_expr(result, verbosity)
        result = get_terminal(result, "BoolOp", verbosity)
        result = parse_expr(result, verbosity)
        result = get_terminal(result, "CloseParen", verbosity)
        return result
    else:
        result = get_terminal(result[1:], "Boolean", verbosity)
        return result

def get_terminal(token_list, terminal_type, verbosity):
    if token_list[0]["type"] is terminal_type:
        if verbosity:
            print("Found", terminal_type, "!\n")
        return token_list[1:]
    elif token_list[0]["type"] is "Error":
        return token_list
    else:
        return [{"type": "Error", "value": terminal_type}] + token_list
