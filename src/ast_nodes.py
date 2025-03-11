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
        self.selector = selector    
        self.block = block

class BlockNode:
    def __init__(self, params, statements):
        self.params = params # list of param names
        self.statements = statements # list of StatementNode

class AssignNode:
    def __init__(self, var, expr):
        self.var = var # str
        self.expr = expr # ExprNode

class SendNode:
    def __init__(self, receiver, selector, arguments):
        self.receiver = receiver
        self.selector = selector
        self.arguments = arguments

class LiteralNode:
    def __init__(self, type, value):
        self.type = type # 'int', 'string', 'nil', 'true', 'false'
        self.value = value # '42', 'hello', None, True, False

class VarNode:
    def __init__(self, var):
        self.var = var # str