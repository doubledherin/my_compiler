import json

class AbstractSyntaxTree(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class Program(AbstractSyntaxTree):
    def __init__(self, program_name, block):
        self.program_name = program_name
        self.block = block


class Block(AbstractSyntaxTree):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class FunctionDeclaration(AbstractSyntaxTree):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Type(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class VariableDeclaration(AbstractSyntaxTree):
    def __init__(self, variable, type):
        self.variable = variable
        self.type = type


class FunctionDeclaration(AbstractSyntaxTree):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Variable(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOperator(AbstractSyntaxTree):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BinaryOperator(AbstractSyntaxTree):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Number(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Compound(AbstractSyntaxTree):
    """Represents a '{ }' block"""
    def __init__(self):
        self.children = []


class Assign(AbstractSyntaxTree):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class NoOp(AbstractSyntaxTree):
    pass
