'''
 @file parse.py
 @brief This is the main file of the project
 @author Jakub Fukala (xfukal01)
'''

import sys
from lark import Lark

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

selector: ID ( ":" ID )*


// ---------------------
// 5) Bloky podle 10-14
block: "[" (block_params ("|" block_stat)? | block_stat)? "]"

block_params: ( ":" ID)*

block_stat: statement ( "." statement )* "."?

statement: var_assign

// Prirazeni: "x := expr"
var_assign: ID ASSIGN expr

// ---------------------
// 6) Vyrazy

expr: expr_base expr_tail?

// expr_tail: bud bezparametricky selektor nebo parametricky selektor 
expr_tail: ID  -> paramless_selector
         | expr_sel 
         |          -> no_selector // epsilon

expr_sel: ID ":" expr_base expr_tail? // parametricky selektor typu "foo: 123"


expr_base: INT
         | STR
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

ID: /[a-z_][a-zA-Z0-9_]*/

INT: /[+\-]?\d+/

STRING: /'(\\[n'\\\\]|[^'\\])*'/

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
    print("Help is here")

def main():
    source_code = sys.stdin.read()
    print(source_code)
    parse_tree = sol25_parser.parse(source_code)
    print(parse_tree.pretty())


if __name__ == "__main__":
    if "--help" in sys.argv:
        call_help()
        sys.exit(0)
    main()

    #Konec souboru parse.py (EOF)
    