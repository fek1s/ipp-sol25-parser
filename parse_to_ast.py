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
        # program: class_def*
        return ProgramNode(list(class_defs))
    
    def class_def(self, cname, pname, *methods):
        # class_def: "class" CID ":" CID "{" method* "}"
        return ClassNode(str(cname), str(pname), list(methods))
    
    def method(self, selector, block):
        # method: selector block
        return MethodNode(selector, block)