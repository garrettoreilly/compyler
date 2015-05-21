import sys

class Scope:
    def __init__(self, ast, parent = None):
        self.scope_id = 0
        self.parent = parent
        self.children = []
        self.symbols = []
        self.create_scope(ast)

    def print_table(self, tabs):
        indent = "    " * tabs
        print("\nScope ID: %d" % self.scope_id)
        for a in self.symbols:
            print(a["type"], a["name"])
        for i in self.children:
            i.print_table(tabs+1)

    def generate_table(self, ast):
        i = 0
        while i < len(ast.children):
            if ast.children[i].token["type"] in ["IntOp", "BoolOp"]:
                valid = self.evaluate_expr(ast.children[i])
            elif ast.children[i].token["type"] == "Variable Declaration":
                tokens = ast.children[i].children
                new_symbol = {"type": tokens[0].token["value"], "name": tokens[1].token["value"], 
                        "line": tokens[1].token["line"], "position": tokens[1].token["position"]}
                if new_symbol["name"] in [x["name"] for x in self.symbols]:
                    sys.exit("Error! Variable %s already declared in this scope!" % new_symbol["name"])
                else:
                    self.symbols += [new_symbol]
            elif ast.children[i].token["type"] == "AssignOp":
                tokens = ast.children[i].children
                new_symbol = {"name": tokens[0].token["value"], "line": tokens[0].token["line"], 
                        "position": ast.children[i].token["position"]}
                parent_search = self.check_symbol(new_symbol)
                if parent_search == None:
                    sys.exit("Error! Undeclared identifier %s!\nLine: %d, Position %d" 
                            % (new_symbol["name"], new_symbol["line"], new_symbol["position"]))
                else:
                    (new_symbol["type"], new_symbol["value"]) = self.evaluate_expr(tokens[1])
                for x in parent_search.symbols:
                    if x["name"] == new_symbol["name"]:
                        if x["type"] == new_symbol["type"]:
                            x["value"] = new_symbol["value"]
                            break
                        else:
                            sys.exit("Error! Type mismatch on ID %s!\nLine %d, Position %d" 
                                    % (new_symbol["name"], new_symbol["line"], new_symbol["position"]))
            elif ast.children[i].token["type"] == "Print Statement":
                valid = self.evaluate_expr(ast.children[i].children[0])
            elif ast.children[i].token["type"] in ["If Statement", "While Statement"]:
                valid = self.evaluate_expr(ast.children[i].children[0])
                self.children += [Scope(ast.children[i].children[1], self)]
            elif ast.children[i].token["type"] == "Block":
                self.children += [Scope(ast.children[i], self)]
            i+=1

    def create_scope(self, ast):
        if self.parent != None:
            self.scope_id = self.parent.scope_id + self.parent.calculate_scope_id()
        self.generate_table(ast)
        for i in self.symbols:
            try:
                temp = i["value"]
            except:
                print("Warning! Declared ID %s is not used!\nLine %d, Position %d" 
                        % (i["name"], i["line"], i["position"]))

    def check_symbol(self, symbol):
        if symbol["name"] in [x["name"] for x in self.symbols]:
            return self
        elif self.parent != None:
            return self.parent.check_symbol(symbol)
        else:
            return None

    def evaluate_expr(self, ast):
        if ast.token["type"] == "Digit":
            return ("int", ast.token["value"])
        elif ast.token["type"] == "CharList":
            return ("string", ast.token["value"])
        elif ast.token["type"] == "BoolVal":
            return ("boolean", ast.token["value"])
        elif ast.token["type"] == "Id":
            new_symbol = {"name": ast.token["value"], "line": ast.token["line"], 
                    "position": ast.token["position"]}
            id_scope = self.check_symbol(new_symbol)
            for i in id_scope.symbols:
                if i["name"] == new_symbol["name"]:
                    try:
                        return (i["type"], i["value"])
                    except:
                        print("Warning! Use of uninitialized ID %s!\nLine %d, Position %d" 
                                % (new_symbol["name"], new_symbol["line"], new_symbol["position"]))
                        if i["type"] == "int":
                            return ("int", 0)
                        elif i["type"] == "string":
                            return ("string", "")
                        elif i["type"] == "boolean":
                            return ("boolean", "false")
        elif ast.token["type"] == "IntOp":
            int_op_children = []
            for i in ast.children:
                int_op_children += [self.evaluate_expr(i)]
            if all([x == "int" for x in [y[0] for y in int_op_children]]):
                return ("int", sum([int(j[1]) for j in int_op_children]))
        elif ast.token["type"] == "BoolOp":
            bool_op_children = []
            for i in ast.children:
                bool_op_children += [self.evaluate_expr(i)]
            if bool_op_children[0][1] == bool_op_children[1][1]:
                if ast.token["value"] == "==":
                    return ("boolean", "true")
                else:
                    return ("boolean", "false")
            else:
                if ast.token["value"] == "==":
                    return ("boolean", "false")
                else:
                    return ("boolean", "true")

    def calculate_scope_id(self):
        new_id = 1
        if self.children == []:
            return new_id
        else:
            for i in self.children:
                new_id += i.calculate_scope_id()
            return new_id
