'''
 @file: parse.py
 @brief: Toto je hlavní soubor pro spuštění programu parse.py
 @details: Tento soubor obsahuje hlavní funkci main, která zpracovává vstupní soubor a vytváří AST strom.
 @author: Jakub Fukala (xfukal01)
'''

import sys
from lark import UnexpectedToken, UnexpectedCharacters
from src.parse_to_ast import Sol25Transformer
from src.debug_print import print_ast
from src.grammar import create_parser
from src.sem_checker import SemChecker


def call_help():
    print("Nápověda k programu parse.py")
    print("Použití např.: python3.11 parse.py < [input_file] > [output_file]")
    print("  --help: Vypíše tuto nápovědu")

def main():
    source_code = sys.stdin.read()

    try:
        sol25_parser = create_parser()
        tree = sol25_parser.parse(source_code)
    # Semanticka chyba
    except UnexpectedToken as e:
        print(f"Unexpected token: {e}", file=sys.stderr)
        sys.exit(22)
    # Lexikalni chyba
    except UnexpectedCharacters as e:
        print(f"Unexpected characters: {e}", file=sys.stderr)
        sys.exit(21)
    
    # AST transformation
    transformer = Sol25Transformer()
    ast_root = transformer.transform(tree)

    # Debug print
    #print_ast(ast_root)

    # Semanticka kontrola

    try:
        sem_checker = SemChecker(ast_root)
        sem_checker.check()
    except SystemExit as e:
        sys.exit(e.code)




if __name__ == "__main__":
    args = sys.argv[1:] # Skip the first argument (name of the script)
    if "--help" in args or "-h" in args:
        if len(args) > 1:
            print("Invalid arguments", file=sys.stderr)
            sys.exit(10)
        call_help()
        sys.exit(0)
    if args:
        print("Invalid arguments", file=sys.stderr)
        sys.exit(10)
    main()

    
#Konec souboru parse.py (EOF)
    