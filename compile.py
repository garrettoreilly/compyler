import sys, lex

def main():
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    tokenList = lex.lexProgram(program)
    for i in tokenList:
        print(i.kind);

if __name__ == '__main__':
    main()
