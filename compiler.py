import sys, lexer, parser, cst

def main():
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    token_list = lexer.lex_program(program)
    parser.parse_program(token_list)
    tree = cst.generate_cst(token_list)
    cst.print_cst(tree, 0)
    print("Compilation successful!")

if __name__ == '__main__':
    main()
