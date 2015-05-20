import sys

class Scope:
    def __init__(self, scope_id = 0, parent = None):
        self.scope_id = scope_id
        self.parent = parent
        self.children = []
        self.symbols = []

    def print_table(self, tabs):
        indent = "  " * tabs
        print("%sScope ID: %d" % (indent, self.scope_id))
        for a in self.symbols:
            print(a)
        for i in self.children:
            if i.children is not []:
                i.print_table(tabs+1)

    def generate_table(self, ast):
        i = 0
        while i < len(ast.children):
            if ast.children[i].token["type"] in ["Print Statement", "AssignOp", "Variable Declaration", 
                    "If Statement", "While Statement", "IntOp", "BoolOp"]:
                self.generate_table(ast.children[i])
            elif ast.children[i].token["type"] is "IdType":
                new_symbol = {"type": ast.children[i].token["value"], "name": ast.children[i+1].token["value"], 
                        "line": ast.children[i+1].token["line"], "position": ast.children[i+1].token["position"]}
                if new_symbol["name"] in [x["name"] for x in self.children]:
                    sys.exit("Error! Variable %s already declared in this scope!" % new_symbol["name"])
                else:
                    self.symbols += [new_symbol]
                i+=2
            elif ast.children[i].token["type"] is "Id":
                new_symbol = {"name": ast.children[i].token["value"], "line": ast.children[i].token["line"], 
                        "position": ast.children[i].token["position"]}
                parent_search = self.check_symbol(new_symbol)
                print("Line 42:", parent_search.scope_id)
                if parent_search is None:
                    sys.exit("Error! Undeclared identifier %s!\nLine: %d, Position %d" 
                            % (new_symbol["name"], new_symbol["line"], new_symbol["position"]))
                else:
                    print("Line 42: Line %d, Position %d" % (ast.children[i].token["line"], ast.children[i].token["position"]))
                    (new_symbol["type"], new_symbol["value"]) = self.evaluate_expr(ast.children[i+1])
                for x in parent_search.symbols:
                    if x["name"] is new_symbol["name"]:
                        if x["type"] is new_symbol["type"]:
                            x["value"] = new_symbol["value"]
                            break
                        else:
                            sys.exit("Error! Type mismatch on ID %s!\nLine %d, Position %d" 
                                    % (new_symbol["name"], new_symbol["line"], new_symbol["position"]))
            elif ast.children[i].token["type"] is "Block":
                print("Creating new scope...")
                self.create_child_scope(ast.children[i])
            i+=1

    def create_child_scope(self, ast):
        new_scope_id = self.scope_id + self.calculate_scope_id()
        new_scope = Scope(new_scope_id, self)
        self.children += [new_scope]
        new_scope.generate_table(ast)

    def check_symbol(self, symbol):
        if symbol["name"] in [x["name"] for x in self.symbols]:
            return self
        elif self.parent is not None:
            return check_symbol(self.parent, symbol)
        else:
            return None

    def evaluate_expr(self, ast):
        if ast.token["type"] is "Digit":
            return ("int", ast.token["value"])
        elif ast.token["type"] is "CharList":
            return ("string", ast.token["value"])
        elif ast.token["type"] is "BoolVal":
            return ("boolean", ast.token["value"])
        elif ast.token["type"] is "IntOp":
            int_op_children = []
            for i in ast.children:
                int_op_children += [self.evaluate_expr(i)]
            if all([x is "int" for x in [y[0] for y in int_op_children]]):
                return ("int", sum([int(j[1]) for j in int_op_children]))
        elif ast.token["type"] is "BoolOp":
            bool_op_children = []
            for i in ast.children:
                bool_op_children += self.evalue_expr(i)
            if bool_op_children[0][1] is bool_op_children[1][1]:
                return ("boolean", "true")
            else:
                return ("boolean", "false")

    def calculate_scope_id(self):
        new_id = 0
        if self.children is []:
            return 1
        else:
            for i in self.children:
                new_id += i.calculate_scope_id(i)
            return new_id
