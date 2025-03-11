"""
    @file: debug_print.py
    @brief: Debugovací výpis AST stromu
    @author: Jakub Fukala (xfukal01) 
"""

from src.ast_nodes import *

def print_ast(node, indent=0):
    prefix = "  " * indent
    # Rozlišíte typ uzlu
    if isinstance(node, ProgramNode):
        print(f"{prefix}ProgramNode:")
        for cls in node.classes:
            print_ast(cls, indent+1)

    elif isinstance(node, ClassNode):
        print(f"{prefix}ClassNode name={node.name} parent={node.parent}")
        for meth in node.methods:
            print_ast(meth, indent+1)

    elif isinstance(node, MethodNode):
        print(f"{prefix}MethodNode selector={node.selector}")
        print_ast(node.block, indent+1)

    elif isinstance(node, BlockNode):
        print(f"{prefix}BlockNode params={node.params}")
        for st in node.statements:
            print_ast(st, indent+1)

    elif isinstance(node, AssignNode):
        print(f"{prefix}AssignNode var={node.var}")
        print_ast(node.expr, indent+1)

    elif isinstance(node, SendNode):
        print(f"{prefix}SendNode selector={node.selector}")
        print(f"{prefix}  receiver:")
        print_ast(node.receiver, indent+2)
        print(f"{prefix}  arguments:")
        for arg in node.arguments:
            print_ast(arg, indent+2)

    elif isinstance(node, LiteralNode):
        print(f"{prefix}LiteralNode type={node.type} value={node.value}")

    elif isinstance(node, VarNode):
        print(f"{prefix}VarNode name={node.var}")

    else:
        print(f"{prefix}Unknown node type: {node}")
