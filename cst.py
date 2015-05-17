class CST:
    def __init__(self, token):
        self.token = token
        self.children = []

    def print_cst(self, tabs):
        parent_indent = "  " * (tabs - 1)
        child_indent = "  " * tabs
        try:
            print("%s%s, %s" % (parent_indent, self.token["type"], self.token["value"]))
        except:
            print("%s%s" % (parent_indent, self.token["type"]))
        for i in self.children:
            if i.children is not []:
                i.print_cst(tabs+1)

    def generate_cst(self, token_list):
        token_list = self.parse_block(token_list)
        self.children += [CST(token_list.pop(0))]
        self.print_cst(1)

    def parse_block(self, token_list):
        node = CST({"type": "Block"})
        node.children += [CST(token_list.pop(0))]
        token_list = node.parse_statement_list(token_list)
        node.children += [CST(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_statement_list(self, token_list):
        node = CST({"type": "Statement List"})
        if token_list[0]["type"] is "CloseBrace":
            return token_list
        token_list = node.parse_statement(token_list)
        token_list = node.parse_statement_list(token_list)
        self.children += [node]
        return token_list

    def parse_statement(self, token_list):
        node = CST({"type": "Statement"})
        if token_list[0]["type"] is "Print":
            token_list = node.parse_print_statement(token_list)
        elif token_list[0]["type"] is "Id":
            token_list = node.parse_assign_statement(token_list)
        elif token_list[0]["type"] is "IdType":
            token_list = node.parse_var_decl(token_list)
        elif token_list[0]["type"] is "While":
            token_list = node.parse_while_statement(token_list)
        elif token_list[0]["type"] is "If":
            token_list = node.parse_if_statement(token_list)
        elif token_list[0]["type"] is "OpenBrace":
            token_list = node.parse_block(token_list)
        self.children += [node]
        return token_list

    def parse_print_statement(self, token_list):
        node = CST({"type": "Print Statement"})
        node.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
        token_list = node.parse_expr(token_list)
        node.children += [CST(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_assign_statement(self, token_list):
        node = CST({"type": "Assignment Statement"})
        node.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
        token_list = node.parse_expr(token_list)
        self.children += [node]
        return token_list

    def parse_var_decl(self, token_list):
        node = CST({"type": "Variable Declaration"})
        node.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_while_statement(self, token_list):
        node = CST({"type": "While Statement"})
        node.children += [CST(token_list.pop(0))]
        token_list = node.parse_bool_expr(token_list)
        token_list = node.parse_block(token_list)
        self.children += [node]
        return token_list

    def parse_if_statement(self, token_list):
        node = CST({"type": "If Statement"})
        node.children += [CST(token_list.pop(0))]
        token_list = node.parse_bool_expr(token_list)
        token_list = node.parse_block(token_list)
        self.children += [node]
        return token_list

    def parse_expr(self, token_list):
        node = CST({"type": "Expression"})
        if token_list[0]["type"] is "Digit":
            token_list = node.parse_int_expr(token_list)
        elif token_list[0]["type"] is "CharList":
            token_list = node.parse_string_expr(token_list)
        elif token_list[0]["type"] in ["OpenParen", "BoolVal"]:
            token_list = node.parse_bool_expr(token_list)
        elif token_list[0]["type"] is "Id":
            node.children += [CST(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_int_expr(self, token_list):
        node = CST({"type": "Int Expression"})
        node.children += [CST(token_list.pop(0))]
        if token_list[0]["type"] is "IntOp":
            node.children += [CST(token_list.pop(0))]
            token_list = node.parse_expr(token_list)
        self.children += [node]
        return token_list

    def parse_string_expr(self, token_list):
        node = CST({"type": "String Expression"})
        node.children += [CST(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_bool_expr(self, token_list):
        node = CST({"type": "Boolean Expression"})
        if token_list[0]["type"] is "OpenParen":
            node.children += [CST(token_list.pop(0))]
            token_list = node.parse_expr(token_list)
            node.children += [CST(token_list.pop(0))]
            token_list = node.parse_expr(token_list)
            node.children += [CST(token_list.pop(0))]
        else:
            node.children += [CST(token_list.pop(0))]
        self.children += [node]
        return token_list
