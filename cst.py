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
        cst = CST({"type": "Block"})
        cst.children += [CST(token_list.pop(0))]
        token_list = cst.parse_statement_list(token_list)
        # if result is not None:
        #     self.children += [result]
        cst.children += [CST(token_list.pop(0))]
        self.children += [cst]
        return token_list

    def parse_statement_list(self, token_list):
        cst = CST({"type": "Statement List"})
        if token_list[0]["type"] is "CloseBrace":
            return token_list
        token_list = cst.parse_statement(token_list)
        # self.children += [result]
        token_list = cst.parse_statement_list(token_list)
        # if result is not None:
        #     self.children += [result]
        self.children += [cst]
        return token_list

    def parse_statement(self, token_list):
        cst = CST({"type": "Statement"})
        if token_list[0]["type"] is "Print":
            token_list = cst.parse_print_statement(token_list)
        elif token_list[0]["type"] is "Id":
            token_list = cst.parse_assign_statement(token_list)
        elif token_list[0]["type"] is "IdType":
            token_list = cst.parse_var_decl(token_list)
        elif token_list[0]["type"] is "While":
            token_list = cst.parse_while_statement(token_list)
        elif token_list[0]["type"] is "If":
            token_list = cst.parse_if_statement(token_list)
        elif token_list[0]["type"] is "OpenBrace":
            token_list = cst.parse_block(token_list)
        self.children += [cst]
        return token_list

    def parse_print_statement(self, token_list):
        cst = CST({"type": "Print Statement"})
        cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
        token_list = cst.parse_expr(token_list)
        cst.children += [CST(token_list.pop(0))]
        self.children += [cst]
        return token_list

    def parse_assign_statement(self, token_list):
        cst = CST({"type": "Assignment Statement"})
        cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
        token_list = cst.parse_expr(token_list)
        self.children += [cst]
        return token_list

    def parse_var_decl(self, token_list):
        cst = CST({"type": "Variable Declaration"})
        cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
        self.children += [cst]
        return token_list

    def parse_while_statement(self, token_list):
        cst = CST({"type": "While Statement"})
        cst.children += [CST(token_list.pop(0))]
        token_list = cst.parse_bool_expr(token_list)
        token_list = cst.parse_block(token_list)
        self.children += [cst]
        return token_list

    def parse_if_statement(self, token_list):
        cst = CST({"type": "If Statement"})
        cst.children += [CST(token_list.pop(0))]
        token_list = cst.parse_bool_expr(token_list)
        token_list = cst.parse_block(token_list)
        self.children += [cst]
        return token_list

    def parse_expr(self, token_list):
        cst = CST({"type": "Expression"})
        if token_list[0]["type"] is "Digit":
            token_list = cst.parse_int_expr(token_list)
        elif token_list[0]["type"] is "CharList":
            token_list = cst.parse_string_expr(token_list)
        elif token_list[0]["type"] in ["OpenParen", "BoolVal"]:
            token_list = cst.parse_bool_expr(token_list)
        elif token_list[0]["type"] is "Id":
            cst.children += [CST(token_list.pop(0))]
        self.children += [cst]
        return token_list

    def parse_int_expr(self, token_list):
        cst = CST({"type": "Int Expression"})
        cst.children += [CST(token_list.pop(0))]
        if token_list[0]["type"] is "IntOp":
            cst.children += [CST(token_list.pop(0))]
            token_list = cst.parse_expr(token_list)
        self.children += [cst]
        return token_list

    def parse_string_expr(self, token_list):
        cst = CST({"type": "String Expression"})
        cst.children += [CST(token_list.pop(0))]
        self.children += [cst]
        return token_list

    def parse_bool_expr(self, token_list):
        cst = CST({"type": "Boolean Expression"})
        if token_list[0]["type"] is "OpenParen":
            cst.children += [CST(token_list.pop(0))]
            token_list = cst.parse_expr(token_list)
            cst.children += [CST(token_list.pop(0))]
            token_list = cst.parse_expr(token_list)
            cst.children += [CST(token_list.pop(0))]
        else:
            cst.children += [CST(token_list.pop(0))]
        self.children += [cst]
        return token_list
