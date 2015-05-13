import sys, lexer

def main():
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    tokenList = lexer.lex_program(program)
    print("Compilation successful!")

if __name__ == '__main__':
    main()
