import sys, lexer, parser

def main():
    verbosity = False
    args = sys.argv
    if len(args) == 3 and sys.argv[1] in ["-v", "--verbose"]:
        verbosity = True
        args.pop(1)
    f = open(args[1], 'r')
    program = f.read()
    f.close()
    token_list = lexer.lex_program(program)
    if verbosity:
        print("Token list:\n", [x["type"] for x in token_list])
    parser.parse_program(token_list)
    print("Compilation successful!")

if __name__ == '__main__':
    main()
