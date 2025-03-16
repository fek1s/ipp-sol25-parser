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
from src.ast_to_xml import ast_to_xml
import xml.etree.ElementTree as ET
import re


def call_help():
    print("Nápověda k programu parse.py")
    print("Použití např.: python3.11 parse.py < [input_file] > [output_file]")
    print("  --help: Vypíše tuto nápovědu")

def extract_comment(source_code):
    '''Extrakce komentáře z kódu'''
    match = re.search(r'"([^"]*)"', source_code, re.DOTALL)
    if match:
        return match.group(1)
    return None

def fix_coment_for_xml(comment):
    '''Nahradi \n'''
    return comment.replace('\\n', '&#10;')

def main():
    source_code = sys.stdin.read()
    desc = extract_comment(source_code)
    if desc:
        desc = fix_coment_for_xml(desc)
    else:
        desc = None

    try:
        sol25_parser = create_parser()
        tree = sol25_parser.parse(source_code)
        print(tree.pretty())
    # Semanticka chyba
    except UnexpectedToken as e:
        print(f"Unexpected token: {e}", file=sys.stderr)
        sys.exit(22)
    # Lexikalni chyba
    except UnexpectedCharacters as e:
        print(f"Unexpected characters: {e}", file=sys.stderr)
        sys.exit(21)
    
    # Převod na AST
    transformer = Sol25Transformer()
    ast_root = transformer.transform(tree)

    # Debugovací výpis AST stromu
    print_ast(ast_root)

    # Semanticka kontrola
    try:
        sem_checker = SemChecker(ast_root)
        sem_checker.check()
    except SystemExit as e:
        sys.exit(e.code)

    # Prevod AST do XML
    root = ast_to_xml(ast_root, desc)
    ET.indent(root, space="    ")
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode')
    sys.stdout.write(xml_str)

    #Konec funkce main




if __name__ == "__main__":
    """Vstupní bod programu"""

    args = sys.argv[1:] # Ignoruj první argument (název skriptu)
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
    