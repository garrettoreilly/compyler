class Tree:
    def __init__(self, token):
        self.token = token
        self.children = []

    def print_tree(self, tabs):
        parent_indent = "  " * (tabs - 1)
        child_indent = "  " * tabs
        try:
            print("%s%s, %s" % (parent_indent, self.token["type"], self.token["value"]))
        except:
            print("%s%s" % (parent_indent, self.token["type"]))
        for i in self.children:
            if i.children is not []:
                i.print_tree(tabs+1)

    def generate_ast(self, cst):
        i = 0
        while i < len(cst.children):
            if i < len(cst.children)-2 and cst.children[i+1].token["type"] in ["BoolOp", "IntOp", "AssignOp"]:
                cst.children[i+1].children += [cst.children.pop(i), cst.children.pop(i+1)] 
                i-=1
            elif cst.children[i].token["type"] in ["Print Statement", "AssignOp", "Variable Declaration", "If Statement", 
                    "While Statement", "Block", "IdType", "Id", "Digit",  "CharList", "BoolVal", "IntOp", "BoolOp"]:
                self.children += [Tree(cst.children[i].token)]
                self.children[-1].generate_ast(cst.children[i])
            else:
                self.generate_ast(cst.children[i])
            i+=1
                
    def generate_cst(self, token_list):
        token_list = self.parse_block(token_list)
        self.children += [Tree(token_list.pop(0))]

    def parse_block(self, token_list):
        node = Tree({"type": "Block"})
        node.children += [Tree(token_list.pop(0))]
        token_list = node.parse_statement_list(token_list)
        node.children += [Tree(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_statement_list(self, token_list):
        node = Tree({"type": "Statement List"})
        if token_list[0]["type"] is "CloseBrace":
            return token_list
        token_list = node.parse_statement(token_list)
        token_list = node.parse_statement_list(token_list)
        self.children += [node]
        return token_list

    def parse_statement(self, token_list):
        node = Tree({"type": "Statement"})
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
        node = Tree({"type": "Print Statement"})
        node.children += [Tree(token_list.pop(0)), Tree(token_list.pop(0))]
        token_list = node.parse_expr(token_list)
        node.children += [Tree(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_assign_statement(self, token_list):
        node = Tree({"type": "Assignment Statement"})
        node.children += [Tree(token_list.pop(0)), Tree(token_list.pop(0))]
        token_list = node.parse_expr(token_list)
        self.children += [node]
        return token_list

    def parse_var_decl(self, token_list):
        node = Tree({"type": "Variable Declaration"})
        node.children += [Tree(token_list.pop(0)), Tree(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_while_statement(self, token_list):
        node = Tree({"type": "While Statement"})
        node.children += [Tree(token_list.pop(0))]
        token_list = node.parse_bool_expr(token_list)
        token_list = node.parse_block(token_list)
        self.children += [node]
        return token_list

    def parse_if_statement(self, token_list):
        node = Tree({"type": "If Statement"})
        node.children += [Tree(token_list.pop(0))]
        token_list = node.parse_bool_expr(token_list)
        token_list = node.parse_block(token_list)
        self.children += [node]
        return token_list

    def parse_expr(self, token_list):
        node = Tree({"type": "Expression"})
        if token_list[0]["type"] is "Digit":
            token_list = node.parse_int_expr(token_list)
        elif token_list[0]["type"] is "CharList":
            token_list = node.parse_string_expr(token_list)
        elif token_list[0]["type"] in ["OpenParen", "BoolVal"]:
            token_list = node.parse_bool_expr(token_list)
        elif token_list[0]["type"] is "Id":
            node.children += [Tree(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_int_expr(self, token_list):
        node = Tree({"type": "Int Expression"})
        node.children += [Tree(token_list.pop(0))]
        if token_list[0]["type"] is "IntOp":
            node.children += [Tree(token_list.pop(0))]
            token_list = node.parse_expr(token_list)
        self.children += [node]
        return token_list

    def parse_string_expr(self, token_list):
        node = Tree({"type": "String Expression"})
        node.children += [Tree(token_list.pop(0))]
        self.children += [node]
        return token_list

    def parse_bool_expr(self, token_list):
        node = Tree({"type": "Boolean Expression"})
        if token_list[0]["type"] is "OpenParen":
            node.children += [Tree(token_list.pop(0))]
            token_list = node.parse_expr(token_list)
            node.children += [Tree(token_list.pop(0))]
            token_list = node.parse_expr(token_list)
            node.children += [Tree(token_list.pop(0))]
        else:
            node.children += [Tree(token_list.pop(0))]
        self.children += [node]
        return token_list
