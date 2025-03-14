"""
    @file parse_to_ast.py
    @brief Soubor pro transformaci AST stromu pomocí Lark
    @details Třída Sol25Transformer je potomek třídy Transformer z Lark.
    @author Jakub Fukala (xfukal01)
"""

from lark import Transformer, v_args
from src.ast_nodes import (
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
    """Tranformer pro stavbu AST stromu"""

    def start(self, program_node):
        # start: program
        return program_node

    def program(self, *class_defs):
        # program: class_def*5
        return ProgramNode(list(class_defs))
    
    def class_def(self, cname, pname, *methods):
        # class_def: "class" CID ":" CID "{" method* "}"
        if isinstance(cname, LiteralNode) and cname.type == "class":
            cname = cname.value
        if isinstance(pname, LiteralNode) and pname.type == "class":
            pname = pname.value
            
        return ClassNode(str(cname), str(pname), list(methods))
    
    def method(self, selector, block):
        # method: selector block
        return MethodNode(selector, block)
    
    def single_selector(self, token):
        # jednoslovný selekto   r
        # token je VarNode("run") nebo VarNode("asString") atd.
        if isinstance(token, VarNode):
            return token.var
        else:
            return str(token)
        
    def multi_selector(self, *parts):
    # parts např. (VarNode("compute"), ":", VarNode("and"), ":", VarNode("and"), ":")
        sel = ""
        i = 0
        while i < len(parts):
            node = parts[i]
            if isinstance(node, VarNode):
                sel += node.var + ":"
            else:
                sel += str(node) + ":"
            i += 2  # posun o 2 => ID, COLON
        return sel

    def selector(self, child):
       return child


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
    # e.g. params = [VarNode("x"), VarNode("y"), VarNode("z")]
        out = []
        for p in params:
            if isinstance(p, VarNode):
                out.append(p.var)
            else:
                out.append(str(p))
        return out
    
    def block_stat(self, *statements):
        # block_stat: statement ( "." statement )* "."?
        return list(statements)

    def statement(self, statement):
        # statement: var_assign
        return statement
    
    def var_assign(self, var,_assign, expr):
        # var_assign: ID ASSIGN expr
        #return AssignNode(str(var), expr)
        if isinstance(var, VarNode):
            var = var.var
        else:
            var = str(var)
        return AssignNode(var, expr)
    
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
        # tokens = [ ID, COLON, expr, ID, COLON, expr, ... ]
        sel_parts = []
        args = []
        i = 0
        while i < len(tokens):
            s = tokens[i]       # ID
            i += 1
            colon = tokens[i]   # COLON
            i += 1
            e = tokens[i]       # expr
            i += 1  

            # s je typicky VarNode("from") nebo "from"
            # e je výraz
            if isinstance(s, VarNode):
                sel_parts.append(s.var + ":")
            else:
                sel_parts.append(str(s) + ":")

            args.append(e)

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
        return VarNode(token.value)
    
    def CID(self, token):
        # třída
        return LiteralNode("class", token.value)
    
    def BLOCK_PARAM_ID(self, token):
        return token.value[1:] # Zahodit dvojtečku
    
# Konec souboru parse_to_ast.py (EOF)