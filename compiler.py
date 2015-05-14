import sys, lexer, parser

def main():
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    token_list = lexer.lex_program(program)
    parser.parse_program(token_list)
    print("Compilation successful!")

if __name__ == '__main__':
    main()
