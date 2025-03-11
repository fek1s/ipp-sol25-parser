"""
    grammar.py
    Definice gramatiky pro jazyk Sol25 pomocí Lark
    Jakub Fukala (xfukal01)
"""

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

def create_parser():
    return Lark(sol25_grammar, start='start', parser='lalr')