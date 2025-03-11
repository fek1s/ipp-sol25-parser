#parse_to_ast.py
# '''
#  @file parse_to_ast.py
#  @brief This file contains the transformer classes for the Lark parser
#  @author Jakub Fukala (xfukal01)
# '''

from lark import Transformer, v_args
from ast_nodes import (
    ProgramNode,
    ClassNode,
    MethodNode,
    BlockNode,
    AssignNode,
    SendNode,
    LiteralNode,
    VarNode,
)

@v_args(inline=True)
class Sol25Transformer(Transformer):
    """Tranforme pro stavbu AST stromu"""

    def program(self, *class_defs):
        # program: class_def*5
        return ProgramNode(list(class_defs))
    
    def class_def(self, cname, pname, *methods):
        # class_def: "class" CID ":" CID "{" method* "}"
        return ClassNode(str(cname), str(pname), list(methods))
    
    def method(self, selector, block):
        # method: selector block
        return MethodNode(selector, block)

    def selector(self, child):
        # selector: SINGLE_SELECTOR | multi_selector
        return child
    
    def single_selector(self, token):
        # single_selector: "run:"
        return str(token)
    
    def keyword_selector(self, token):
        # keyword_selector: "compute:and:and:"
        return str(token)
    
    def multi_selector(self, *selectors):
        # multi_selector: keyword_selector+
        return "".join(selectors) # Concatenate all selectors

    def block(self, *children):
        # block: "[" (block_params ("|" block_stat)? | block_stat)? "]"
        params = []
        statements = []
        if len(children) == 1:
            # maybe block_stat
            c = children[0]
            if isinstance(c, list):
                # block_stat
                statements = c
        elif len(children) == 2:
            # block_params ("|" block_stat)?
            params = children[0]
            statements = children[1]
        return BlockNode(params, statements)
    
    def block_params(self, *params):
        # block_params: (BLOCK_PARAM_ID)*
        # Každý param se vrací jako string "param" bez dvojtečky
        return list(params)
    
    def block_stat(self, *statements):
        # block_stat: statement ( "." statement )* "."?
        return list(statements)

    def statement(self, statement):
        # statement: var_assign
        return statement
    
    def var_assign(self, var,_assign, expr):
        # var_assign: ID ASSIGN expr
        return AssignNode(str(var), expr)
    
    def expr(self, expr):
        # expr: send_expr
        return expr
    
    def send_expr(self, primary, *messages):
        # send_expr: primary (msg_send)*
        current = primary
        for (sel, args) in messages:
            current = SendNode(current, sel, args)
        return current

    def msg_send(self, child):
        # msg_send: paramless_send | keyword_send
        return child
    
    def paramless_send(self, selector):
        # paramless_send: "print"
        return (str(selector), [])
    
    def keyword_send(self, *tokens):
        # gramatika: (ID ":" expr)+ 
        # Vrací tuple (selector, [args])
        sel_parts = []
        args = []
        i = 0
        while i < len(tokens):
            s = tokens[i] # ID
            i += 1
            e = tokens[i] # expr
            i += 1
            sel_parts.append(str(s) + ":")
            args.append(e)
        # Concatenate all selectors
        selector = "".join(sel_parts)
        return (selector, args)

    def primary(self, child):
        return child    
    
    def INT(self, token):
        # Např. "42"
        return LiteralNode("int", token.value)
    
    def STRING(self, token):
        # Např. "'hello'"
        raw = token.value
        val = raw[1:-1] # Remove quotes
        return LiteralNode("string", val)
    
    def NIL(self, _):
        return LiteralNode("nil", None)
    
    def TRUE(self, _):
        return LiteralNode("true", True)
    
    def FALSE(self, _):
        return LiteralNode("false", False)
    
    def SELF(self, _):
        return VarNode("self")
    
    def SUPER(self, _):
        return VarNode("super")
    
    def ID(self, token):
        # proměnná
        return str(token)
    
    def CID(self, token):
        # třída
        return str(token)
    
    def BLOCK_PARAM_ID(self, token):
        return token.value[1:] # Zahodit dvojtečku
    
