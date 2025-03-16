"""
    @file: grammar.py
    @brief: Definice gramatiky pro jazyk Sol25 pomocí Lark
    @author: Jakub Fukala (xfukal01)
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

COLON: ":"

selector: single_selector
        | multi_selector

// (3) single_selector = jednoslovný ID (bez dvojtečky)
single_selector: ID

// (4) multi_selector = jeden či více "ID :"

multi_selector: (ID COLON)+


// ---------------------
// 5) Bloky podle 10-14

BLOCK_PARAM_ID: /:(?!self|super|true|false|nil|class)[a-z_][a-zA-Z0-9_]*/

block: "[" block_params? "|" block_stat? "]"

block_params: (BLOCK_PARAM_ID)*

block_stat: (statement ".")+

statement: var_assign

// Prirazeni: "x := expr"
var_assign: ID ASSIGN expr

// ---------------------
// 6) Vyrazy

?expr: send_expr

send_expr: primary (msg_send)*

msg_send: paramless_send | keyword_send

paramless_send: ID

keyword_send: (ID COLON arg_expr)+

?arg_expr: arg_primary
         | "(" expr ")"

         
?arg_primary: INT
            | STRING
            | NIL
            | TRUE
            | FALSE
            | SELF
            | SUPER
            | ID
            | CID
            | block

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

// Comments
%ignore /"[^"]*"/

// Whitespace
%import common.WS
%ignore WS

"""

def create_parser():
    return Lark(sol25_grammar, start='start', parser='lalr')

# Konec souboru grammar.py (EOF)