class AbstractSyntaxTree(object):
    pass


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


class Var(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AbstractSyntaxTree):
    pass
