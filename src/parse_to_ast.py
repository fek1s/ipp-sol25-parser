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
        """
        children může být:
        - ()  -> prázdný blok [|]
        - ( [AssignNode(...)...] ) -> jen statementy, [| a := 1.]
        - ( [param1,...], ) -> jen parametry, [ :x :y |]
        - ( [param1,...], [AssignNode(...), ...] ) -> param+statements
        """
        if len(children) == 0:
            # prázdný block => [|]
            return BlockNode(params=[], statements=[])

        elif len(children) == 1:
            # buď jen parametry NEBO jen statementy
            single = children[0]
            if not single:
                # je to prázdný list => [|]
                return BlockNode([], [])
            # Rozlišíme, zda v single jsou parametry nebo statementy
            # Např. pokud 'single' je list param. (podle Vašeho Transformeru: single může být ["x","y","z"]
            # NEBO list AssignNode
            if single and isinstance(single[0], str):
                # => parametry
                return BlockNode(params=single, statements=[])
            else:
                # => statementy
                return BlockNode(params=[], statements=single)

        elif len(children) == 2:
            # (param-list, statement-list)
            params_list, stat_list = children
            return BlockNode(params=params_list, statements=stat_list)

        else:
            # nečekaný případ
            return BlockNode([], [])
    
    def block_params(self, *params):
    # e.g. params = [VarNode("x"), VarNode("y"), VarNode("z")]
        out = []
        for p in params:
            if isinstance(p, VarNode):
                out.append(p.var)
            else:
                out.append(str(p)[:1]) # zahodit dvojtečku
        #print("block_params", out)
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

    def arg_expr(self, child):
        return child
    
    def arg_primary(self, child):
        return child
    
    def send_expr(self, primary, *messages):
        if not messages:
            return primary
        
        if len(messages) == 1:
            sel, args = messages[0]
            return SendNode(primary, sel, args)

        selector_parts = []
        full_args = []

        for sel, args in messages:
            selector_parts.append(sel)
            full_args.extend(args)
        
        full_selector = "".join(selector_parts)
        return SendNode(primary, full_selector, full_args)

    def msg_send(self, child):
        # msg_send: paramless_send | keyword_send
        return child
    
    def paramless_send(self, selector):
        if isinstance(selector, VarNode):
              return (selector.var, [])
        else:
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
        return LiteralNode("Integer", token.value)
    
    def STRING(self, token):
        # Např. "'hello'"
        raw = token.value
        val = raw[1:-1] # Remove quotes
        return LiteralNode("String", val)
    
    def NIL(self, _):
        return LiteralNode("Nil", None)
    
    def TRUE(self, _):
        return LiteralNode("True", True)
    
    def FALSE(self, _):
        return LiteralNode("False", False)
    
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