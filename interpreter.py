import token_names as tokens
from node_visitor import NodeVisitor

class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_UnaryOp(self, node):
        if node.op.type == tokens.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == tokens.MINUS:
            return -self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == tokens.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == tokens.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == tokens.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == tokens.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        print self.GLOBAL_SCOPE
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
