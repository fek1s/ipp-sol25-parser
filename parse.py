'''
 @file parse.py
 @brief This is the main file of the project
 @author Jakub Fukala (xfukal01)
'''

import sys
from lark import Lark, UnexpectedToken, UnexpectedCharacters
from parse_to_ast import Sol25Transformer


sol25_grammar = r"""
// 0) Start pravidlo

start: program

// ---------------------
// 1) Program 

program: class_def*

// ---------------------
// 2) Definice tridy

class_def: "class" CID ":" CID "{" method* "}"

// ---------------------
// 3) Method definition

method: selector block

// ---------------------
// 4) Selektory 
// - Jednoslovny selektor: "run"
// - Viceslovny selektor: "compute:and:and:"

single_selector: /[a-z_][a-zA-Z0-9_]*/
keyword_selector: /[a-z_][a-zA-Z0-9_]*:/

selector: single_selector | multi_selector
multi_selector: keyword_selector+

// ---------------------
// 5) Bloky podle 10-14
block: "[" (block_params ("|" block_stat)? | block_stat)? "]"

block_params: (BLOCK_PARAM_ID)*

block_stat: statement ( "." statement )* "."?

statement: var_assign

// Prirazeni: "x := expr"
var_assign: ID ASSIGN expr

// ---------------------
// 6) Vyrazy

?expr: send_expr

send_expr: primary (msg_send)*

msg_send: paramless_send | keyword_send

paramless_send: ID

keyword_send: (ID ":" expr)+


?primary: INT
         | STRING
         | NIL
         | TRUE
         | FALSE
         | SELF
         | SUPER
         | ID
         | CID
         | block
         | "(" expr ")"

// ---------------------

// Keywords
CLASS: "class"
NIL: "nil"
TRUE: "true"
FALSE: "false"
SELF: "self"
SUPER: "super"

// Operators
ASSIGN: ":="



CID: /[A-Z][a-zA-Z0-9_]*/

ID: /(?!class|nil|true|false|self|super)[a-z_][a-zA-Z0-9_]*/

INT: /[+\-]?\d+/

STRING: /'(\\[n'\\\\]|[^'\\])*'/

BLOCK_PARAM_ID: /:[a-z_][a-zA-Z0-9_]*/


%ignore /"[^"]*"/

// Whitespace
%import common.WS
%ignore WS

"""

sol25_parser = Lark(
    sol25_grammar,
    start="start", 
    parser="lalr",
)

def call_help():
    print("Nápověda k programu parse.py")
    print("Použití např.: python3.11 parse.py < [input_file] > [output_file]")
    print("  --help: Vypíše tuto nápovědu")

def main():
    source_code = sys.stdin.read()
    #print(source_code)

    # Lex + Syntax analysis
    try:
        tree = sol25_parser.parse(source_code)
        print(tree.pretty())
    except UnexpectedToken as e:
        print(f"Unexpected token: {e}", file=sys.stderr)
        sys.exit(22)
    except UnexpectedCharacters as e:
        print(f"Unexpected characters: {e}", file=sys.stderr)
        sys.exit(21)
    
    # AST transformation
    transformer = Sol25Transformer()
    ast_root = transformer.transform(tree)

    # Print AST
    print(ast_root)




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
    