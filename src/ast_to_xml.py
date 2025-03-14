"""
    @file: ast_to_xml.py
    @brief: Modul pro prevod AST do XML
    @author: Jakub Fukala (xfukal01)
"""

import xml.etree.ElementTree as ET
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

def ast_to_xml(program_node, first_coment=None):
    '''Prevod AST do XML'''
    root = ET.Element("program", {"language": "SOL25"})    
    if first_coment:
        desc = first_coment.replace("\n", "&nbsp;")
        root.set("description", desc)

    for cls in program_node.classes:
        root.append(class_to_xml(cls))
    return root

def class_to_xml(class_node):
    '''Prevod tridy do XML'''
    class_elem = ET.Element("class", {
        "name": class_node.name,
        "parent": class_node.parent
    })

    for method in class_node.methods:
        method_elem = ET.SubElement(class_elem, "method", {
            "selector": method.selector
        })

        block_elem = block_to_xml(method.block)
        method_elem.append(block_elem)

    return class_elem

def block_to_xml(block_node):
    '''Prevod bloku do XML'''
    block_elem = ET.Element("block", {"arity": str(len(block_node.params))})

    # Parametry bloku
    for i, param in enumerate(block_node.params, start=1):
        ET.SubElement(block_elem, "parameter", {
            "order": str(i),
            "name": param
        })
    
    # Statementy bloku

    for i, statemnt in enumerate(block_node.statements, start=1):
        if isinstance(statemnt, AssignNode):
    
            assign_elem = ET.SubElement(block_elem, "assign", {
                "order": str(i)
            })

            var_el = ET.SubElement(assign_elem, "var", {
                "name": statemnt.var
            })

            expr_el = ET.SubElement(assign_elem, "expr")
            expr_to_xml(statemnt.expr, expr_el)
        else:
            # neznamy typ statementu
            pass
        
    return block_elem

def expr_to_xml(expr_node, parent_el):
    """
    Rekurzivně uloží výraz do parent_el (typicky <expr>).
    Podle druhu expr -> <literal>, <var>, <block> nebo <send>.
    """
    if isinstance(expr_node, LiteralNode):

        value = str(expr_node.value)
        if expr_node.type == "Nil":
            value = "nil"
        elif expr_node.type == "True":
            value = "true"
        elif expr_node.type == "False":
            value = "false"
        

        lit_el = ET.SubElement(parent_el, "literal", {
            "class": expr_node.type,  # e.g. "int","string","class","nil"...
            "value": value
        })

    elif isinstance(expr_node, VarNode):
        var_el = ET.SubElement(parent_el, "var", {"name": expr_node.var})
        
    elif isinstance(expr_node, BlockNode):
        # rekurzivně blok -> block_to_xml
        block_el = block_to_xml(expr_node)
        parent_el.append(block_el)
    elif isinstance(expr_node, SendNode):
        # <send selector="xxx">
        send_el = ET.SubElement(parent_el, "send", {"selector": expr_node.selector})
        # Příjemce => <expr> uvnitř
        recv_expr = ET.SubElement(send_el, "expr")
        expr_to_xml(expr_node.receiver, recv_expr)
        # argumenty => <arg order="N"><expr>...</expr></arg>
        for i, arg_expr in enumerate(expr_node.arguments, start=1):
            arg_el = ET.SubElement(send_el, "arg", {"order": str(i)})
            arg_expr_el = ET.SubElement(arg_el, "expr")
            expr_to_xml(arg_expr, arg_expr_el)
    else:
        # neznámý typ => do nothing or raise
        pass