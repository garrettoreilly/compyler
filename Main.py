import sys, Lexer, Parser, Tree, Semantics

def main():
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    token_list = Lexer.lex_program(program)
    Parser.parse_program(token_list)
    cst_root = Tree.Tree({"type": "Program"})
    cst_root.generate_cst(token_list)
    cst_root.print_tree(1)
    ast_root = Tree.Tree({"type": "Block"})
    ast_root.generate_ast(cst_root.children[0])
    ast_root.print_tree(1)
    symbol_table = Semantics.Scope()
    symbol_table.generate_table(ast_root)
    symbol_table.print_table(0)
    print("Compilation successful!")

if __name__ == '__main__':
    main()
