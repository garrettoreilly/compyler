import lexer

def parse_program(token_list):
    result = parse_block(token_list)
    if result[0]["type"] == "EOF":
        print("Parse successful!")
    else:
        sys.exit("Error! Invalid token at line", result[0]["line"], ", position",
                result[0]["position"])

def parse_block(token_list):
    result = get_open_brace(token_list)
    result = parse_statement_list(result)
    result = get_close_brace(result)
    return result

def parse_statement_list(token_list):
    if token_list[0]["type"] == "OpenBrace":
        return token_list
    else:
        result = parse_statement(token_list)
        result = parse_statement_list(result)
        return result

def parse_statement(token_list):
    result_list = [parse_print_statement(token_list), parse_assign_statement(token_list),
            parse_var_decl(token_list), parse_while_statement(token_list),
            parse_if_statement(token_list), parse_block(token_list)]

    for result in result_list:
        if result["type"] is not "Error":
            return result

    return [{"type": "Error"}] + token_list

def parse_print_statement(token_list):
    result = get_print(token_list)
    result = get_open_brace(result)
    result = parse_expr(result)
    result = get_close_brace(result)
    return result

def parse_assign_statement(token_list):
    result = get_id(token_list)
    result = get_assign_op(result)
    result = parse_expr(result)
    return result

def parse_var_decl(token_list):
    result = get_type(token_list)
    result = get_id(result)
    return result

def parse_while_statement(token_list):
    result = get_while(token_list)
    result = parse_bool_expr(result)
    result = parse_block(result)
    return result

def parse_if_statement(token_list):
    result = get_if(token_list)
    result = parse_bool_expr(result)
    result = parse_block(result)
    return result

def parse_expr(token_list):
    result_list = [parse_int_expr(token_list), parse_string_expr(token_list),
            parse_bool_expr(token_list), get_id(token_list)]

    for result in result_list:
        if result[0]["type"] is not "Error":
            return result

    return [{"type": "Error"}] + token_list

def parse_int_expr(token_list):
    result = get_digit(token_list)
    result = get_int_op(result)
    if result[0]["type"] is not "Error":
        result = parse_expr(result)
    else:
        result = result[1:]
    return result

def parse_string_expr(token_list):
    if token_list[0]["type"] is not "CharList":
        return token_list
    else:
        result = get_char_list(token_list)
        return result

def parse_bool_expr(token_list):
    result = get_open_paren(token_list)
    if result[0]["type"] is not "Error":
        result = parse_expr(result)
        result = get_bool_op(result)
        result = parse_expr(result)
        result = get_close_paren(result)
        return result
    else:
        result = get_bool_val(result[1:])
        return result

def get_id(token_list):
    if token_list[0]["type"] is "Id":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_bool_val(token_list):
    if token_list[0]["type"] is "Boolean":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_bool_op(token_list):
    if token_list[0]["type"] is "BoolOp":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_char_list(token_list):
    if token_list[0]["type"] is "CharList":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_int_op(token_list):
    if token_list[0]["type"] is "IntOp":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_digit(token_list):
    if token_list[0]["type"] is "Digit":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_if(token_list):
    if token_list[0]["type"] is "If":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_while(token_list):
    if token_list[0]["type"] is "While":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_type(token_list):
    if token_list[0]["type"] is "IdType":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_assign_op(token_list):
    if token_list[0]["type"] is "AssignOp":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_print(token_list):
    if token_list[0]["type"] is "Print":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_close_paren(token_list):
    if token_list[0]["type"] is "CloseBrace":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_open_paren(token_list):
    if token_list[0]["type"] is "OpenBrace":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_close_brace(token_list):
    if token_list[0]["type"] is "CloseBrace":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list

def get_open_brace(token_list):
    if token_list[0]["type"] is "OpenBrace":
        return token_list[1:]
    else:
        return [{"type": "Error"}] + token_list
