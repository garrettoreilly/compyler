class CST:
    def __init__(self, token):
        self.token = token
    children = []

def print_cst(cst, tabs):
    parent_indent = "    " * (tabs - 1)
    child_indent = "    " * tabs
    print("%s%s" % (parent_indent, cst.token["type"]))
    for i in cst.children:
        if i.children is []:
            print("%s%s" % (child_indent, i.token["type"]))
        else:
            print_cst(i, tabs + 1)

def generate_cst(token_list):
    cst = CST({"type": "Program"})
    (result, rest) = parse_block(token_list)
    cst.children += [result, CST(rest.pop(0))]
    return cst

def parse_block(token_list):
    cst = CST({"type": "Block"})
    cst.children += [CST(token_list.pop(0))]
    (result, rest) = parse_statement_list(token_list)
    if result is not None:
        cst.children += [result]
    cst.children += [CST(rest.pop(0))]
    return (cst, rest)

def parse_statement_list(token_list):
    print(token_list)
    cst = CST({"type": "Statement List"})
    if token_list[0]["type"] is "CloseBrace":
        return (None, token_list)
    (result, rest) = parse_statement(token_list)
    cst.children += [result]
    (result, rest) = parse_statement_list(rest)
    if result is not None:
        cst.children += [result]
    return (cst, rest)

def parse_statement(token_list):
    cst = CST({"type": "Statement"})
    result = None
    if token_list[0]["type"] is "Print":
        (result, rest) = parse_print_statement(token_list)
    elif token_list[0]["type"] is "Id":
        (result, rest) = parse_assign_statement(token_list)
    elif token_list[0]["type"] is "IdType":
        (result, rest) = parse_var_decl(token_list)
    elif token_list[0]["type"] is "While":
        (result, rest) = parse_while_statement(token_list)
    elif token_list[0]["type"] is "If":
        (result, rest) = parse_if_statement(token_list)
    elif token_list[0]["type"] is "OpenBrace":
        (result, rest) = parse_block(token_list)
    cst.children += [result]
    return (cst, rest)

def parse_print_statement(token_list):
    cst = CST({"type": "Print Statement"})
    cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
    (result, rest) = parse_expr(token_list)
    cst.children += [result, rest.pop(0)]
    return (cst, rest)

def parse_assign_statement(token_list):
    cst = CST({"type": "Assignment Statement"})
    cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
    (result, rest) = parse_expr(token_list)
    cst.children += [result]
    return (cst, rest)

def parse_var_decl(token_list):
    cst = CST({"type": "Variable Declaration"})
    cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
    return (cst, token_list)

def parse_while_statement(token_list):
    cst = CST({"type": "While Statement"})
    cst.children += [CST(token_list.pop(0))]
    (result, rest) = parse_bool_expr(token_list)
    cst.children += [result]
    (result, rest) = parse_block(rest)
    cst.children += [result]
    return (cst, rest)

def parse_if_statement(token_list):
    cst = CST({"type": "If Statement"})
    cst.children += [CST(token_list.pop(0))]
    (result, rest) = parse_bool_expr(token_list)
    cst.children += [result]
    (result, rest) = parse_block(rest)
    cst.children += [result]
    return (cst, rest)

def parse_expr(token_list):
    cst = CST({"type": "Expression"})
    if token_list[0]["type"] is "Digit":
        (result, rest) = parse_int_expr(token_list)
    elif token_list[0]["type"] is "CharList":
        (result, rest) = parse_string_expr(token_list)
    elif token_list[0]["type"] is "OpenParen":
        (result, rest) = parse_bool_expr(token_list)
    elif token_list[0]["type"] is "Id":
        (result, rest) = (token_list.pop(0), token_list)
    cst.children += [result]
    return (cst, rest)

def parse_int_expr(token_list):
    cst = CST({"type": "Int Expression"})
    cst.children += [CST(token_list.pop(0))]
    rest = None
    if token_list[0]["type"] is "IntOp":
        cst.children += [CST(token_list.pop(0))]
        (result, rest) = parse_expr(token_list)
        cst.children += [result]
    return (cst, rest)

def parse_string_expr(token_list):
    cst = CST({"type": "String Expression"})
    cst.children += [CST(token_list.pop(0))]
    return (cst, token_list)

def parse_bool_expr(token_list):
    cst = CST({"type": "Boolean Expression"})
    rest = token_list
    if rest[0]["type"] is "OpenParen":
        cst.children += [CST(rest.pop(0))]
        (result, rest) = parse_expr(rest)
        cst.children += [result, CST(rest.pop(0))]
        (result, rest) = parse_expr(rest)
        cst.children += [result, CST(rest.pop(0))]
        return (cst, rest)
    else:
        cst.children += [CST(rest.pop(0))]
        return (cst, rest)
