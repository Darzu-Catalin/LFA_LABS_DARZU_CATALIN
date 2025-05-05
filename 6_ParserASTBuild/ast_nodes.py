# src/ast_nodes.py

class ASTNode:
    """Base class for all AST nodes."""
    pass

class Number(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class Variable(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"

class BinaryOp(ASTNode):
    def __init__(self, op: str, left: ASTNode, right: ASTNode):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"

class UnaryOp(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnOp({self.op}, {self.operand})"

class FuncCall(ASTNode):
    def __init__(self, name: str, argument: ASTNode):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return f"FuncCall({self.name}, {self.argument})"
