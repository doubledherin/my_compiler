import token_names as tokens
from node_visitor import NodeVisitor

class Interpreter(NodeVisitor):

    def __init__(self, tree):
        self.tree = tree

    def visit_Program(self, node):
        print "in visit_Program"
        self.visit(node.block)

    def visit_Block(self, node):
        print "in visit_Block"
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Variable(self, node):
        pass

    def visit_VariableDeclaration(self, node):
        pass

    def visit_FunctionDeclaration(self, node):
        pass

    def visit_UnaryOperator(self, node):
        if node.op.type == tokens.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == tokens.MINUS:
            return -self.visit(node.expr)

    def visit_BinaryOperator(self, node):
        print "in visit BinaryOperator"
        if node.op.type == tokens.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == tokens.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == tokens.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == tokens.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        print "in visit_Number"
        return node.value

    def visit_Compound(self, node):
        print "in visit_Compound"
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        print "in visit_Assign"
        self.visit(node.left)
        self.visit(node.right)

    def interpret(self):
        return self.visit(self.tree)
