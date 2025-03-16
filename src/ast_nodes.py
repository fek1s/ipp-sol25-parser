"""
    @file: ast_nodes.py
    @brief: Soubor obsahující třídy pro AST strom
    @author: Jakub Fukala (xfukal01) 
"""

class ProgramNode:
    def __init__(self, classes):
        self.classes = classes # list of ClassNode

class ClassNode:
    def __init__(self, name, parent, methods):
        self.name = name # str
        self.parent = parent # str
        self.methods = methods # list of MethodNode

class MethodNode:
    def __init__(self, selector, block):
        self.selector = selector # str   
        self.block = block # BlockNode

class BlockNode:
    def __init__(self, params, statements):
        self.params = params # list of param names
        self.statements = statements # list of StatementNode

class AssignNode:
    def __init__(self, var, expr):
        self.var = var # str
        self.expr = expr # Union[LiteralNode, VarNode, SendNode]

class SendNode:
    def __init__(self, receiver, selector, arguments):
        self.receiver = receiver  # Union[LiteralNode, VarNode, SendNode]
        self.selector = selector  # str
        self.arguments = arguments  # list of Union[LiteralNode, VarNode, SendNode]

class LiteralNode:
    def __init__(self, type, value):
        self.type = type # str  `INT`, `STRING`, `NIL`, `TRUE`, `FALSE`
        self.value = value # '42', 'hello', None, True, False

class VarNode:
    def __init__(self, var):
        self.var = var # str


# Konec souboru ast_nodes.py (EOF)