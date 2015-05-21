import Semantics

class ExecEnv:
    def __init__(self, ast, symbol_table):
        self.code = []
        self.static_table = []
        self.jump_table = []
        self.temp_location = 0
        self.heap = []
        self.generate_code(ast, symbol_table)
        self.code += ["00"]
        self.back_patch()
        self.zeros = 256 - (len(self.code) + len(self.heap))
        self.code = " ".join(self.code)
        self.code += " 00" * self.zeros
        self.code += " " + " ".join(self.heap)
        print(self.code)

    def generate_code(self, ast, symbol_table):
        scope = 0
        for i in ast.children:
            if i.token["type"] == "Variable Declaration":
                self.static_table += [{"temp": "T" + str(self.temp_location), 
                    "var": i.children[1].token["value"], "scope": symbol_table.scope_id}]
                self.code += ["A9", "00", "8D", "T" + str(self.temp_location), "XX"]
                self.temp_location += 1
            elif i.token["type"] == "AssignOp":
                temp_scope = symbol_table.check_symbol({"name": i.children[0].token["value"]})
                for x in self.static_table:
                    if x["var"] == i.children[0].token["value"] and x["scope"] == temp_scope.scope_id:
                        (expr_type, expr_value) = symbol_table.evaluate_expr(i.children[1])
                        if expr_type == "Id":
                            for y in self.static_table:
                                if y["var"] == expr_type:
                                    self.code += ["AD", y["temp"], "8D", x["temp"]]
                                    break
                        elif expr_type == "int":
                            self.code += ["A9", "{:02X}".format(int(expr_value)), "8D", x["temp"], "XX"]
                            break
                        elif expr_type == "boolean":
                            bool_val = "01" if expr_value == "true" else "00"
                            self.code += ["A9", bool_val, "8D", x["temp"], "XX"]
                        elif expr_type == "string":
                            expr_value = expr_value.strip("\"")
                            hex_string = ["{:02X}".format(ord(x)) for x in expr_value] + ["00"]
                            self.heap = hex_string + self.heap
                            print(self.heap)
            elif i.token["type"] == "Block":
                self.generate_code(i, symbol_table.children[scope])
                scope+=1

    def back_patch(self):
        append_length = 0
        for i in self.static_table:
            address = len(self.code) + append_length
            for x in range(len(self.code)):
                if self.code[x] == i["temp"]:
                    self.code[x] = "{:02X}".format(address)
                elif self.code[x] == "XX":
                    self.code[x] = "00"
            append_length+=1
