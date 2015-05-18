import sys, Lexer

def parse_program(token_list):
    result = parse_block(token_list)
    if result[0]["type"] == "EOF":
        print("Parse successful!")
    else:
        sys.exit("Error! Expected %s, received %s\nLine %d, position %d" 
                % (result[0]["value"], result[1]["type"], result[1]["line"], result[1]["position"]))

def parse_block(token_list):
    result = get_terminal(token_list, "OpenBrace")
    if result[0]["type"] is "Error":
        return result
    result = parse_statement_list(result)
    result = get_terminal(result, "CloseBrace")
    return result

def parse_statement_list(token_list):
    if token_list[0]["type"] in ["CloseBrace", "Error"]:
        return token_list
    else:
        result = parse_statement(token_list)
        if result[0]["type"] is "Error":
            return result
        result = parse_statement_list(result)
        return result

def parse_statement(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result_list = [parse_print_statement(token_list), parse_assign_statement(token_list),
            parse_var_decl(token_list), parse_while_statement(token_list),
            parse_if_statement(token_list), parse_block(token_list)]

    for result in result_list:
        if result[0]["type"] is not "Error":
            return result

    return [{"type": "Error", "value": "Statement"}] + token_list

def parse_print_statement(token_list):
    if token_list[0]["type"] is "Error":
        return result
    result = get_terminal(token_list, "Print")
    if result[0]["type"] is "Error":
        return result
    result = get_terminal(result, "OpenParen")
    result = parse_expr(result)
    result = get_terminal(result, "CloseParen")
    return result

def parse_assign_statement(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "Id")
    result = get_terminal(result, "AssignOp")
    result = parse_expr(result)
    return result

def parse_var_decl(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "IdType")
    result = get_terminal(result, "Id")
    return result

def parse_while_statement(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "While")
    if result[0]["type"] is "Error":
        return result
    result = parse_bool_expr(result)
    result = parse_block(result)
    return result

def parse_if_statement(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "If")
    if result[0]["type"] is "Error":
        return result
    result = parse_bool_expr(result)
    result = parse_block(result)
    return result

def parse_expr(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result_list = [parse_int_expr(token_list), parse_string_expr(token_list),
            parse_bool_expr(token_list), get_terminal(token_list, "Id")]

    for result in result_list:
        if result[0]["type"] is not "Error":
            return result

    return [{"type": "Error", "value": "Expression"}] + token_list

def parse_int_expr(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "Digit")
    if result[0]["type"] is "Error":
        return result
    result = get_terminal(result, "IntOp")
    if result[0]["type"] is not "Error":
        result = parse_expr(result)
    else:
        result = result[1:]
    return result

def parse_string_expr(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    elif token_list[0]["type"] is not "CharList":
        return [{"type": "Error", "value": "CharList"}] + token_list
    else:
        result = get_terminal(token_list, "CharList")
        return result

def parse_bool_expr(token_list):
    if token_list[0]["type"] is "Error":
        return token_list
    result = get_terminal(token_list, "OpenParen")
    if result[0]["type"] is not "Error":
        result = parse_expr(result)
        result = get_terminal(result, "BoolOp")
        result = parse_expr(result)
        result = get_terminal(result, "CloseParen")
        return result
    else:
        result = get_terminal(result[1:], "BoolVal")
        return result

def get_terminal(token_list, terminal_type):
    if token_list[0]["type"] is terminal_type:
        return token_list[1:]
    elif token_list[0]["type"] is "Error":
        return token_list
    else:
        return [{"type": "Error", "value": terminal_type}] + token_list
