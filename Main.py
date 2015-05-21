import sys, Lexer, Parser, Tree, Semantics

def main():
    verbosity = False
    args = sys.argv
    if len(args) == 3 and sys.argv[1] in ["-v", "--verbose"]:
        verbosity = True
        args.pop(1)
    f = open(args[1], 'r')
    program = f.read()
    f.close()
    token_list = Lexer.lex_program(program)
    if verbosity:
        print("Token list:\n", [x["type"] for x in token_list])
    Parser.parse_program(token_list)
    cst_root = Tree.Tree({"type": "Program"})
    cst_root.generate_cst(token_list)
    if verbosity:
        print("CST:")
        cst_root.print_tree(1)
        print()
    ast_root = Tree.Tree({"type": "Block"})
    ast_root.generate_ast(cst_root.children[0])
    if verbosity:
        print("AST:")
        ast_root.print_tree(1)
        print()
    symbol_table = Semantics.Scope(ast_root)
    if verbosity:
        symbol_table.print_table(0)
    print("\nCompilation successful!")

if __name__ == '__main__':
    main()
