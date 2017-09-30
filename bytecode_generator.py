from node_visitor import NodeVisitor
import token_names as tokens
from code import Code


class BaseGenerator(NodeVisitor):
    def __init__(self):
        self.code_object = Code()

    def __call__(self, tree):
        self.visit(tree)
        return self.code_object

    def _visit_children(self, node):
        for child in node.children:
            print "visiting child", child
            self.visit(child)

class BytecodeGenerator(BaseGenerator):

    def visit_Program(self, node):
        print "in visit_Program"
        self.visit(node.block)

    def visit_Block(self, node):
        print "in visit_Block"
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Variable(self, node):
        print "in visit_Variable"
        pass

    def visit_VariableDeclaration(self, node):
        print "in visit_VariableDeclaration"
        pass

    def visit_FunctionDeclaration(self, node):
        print "in visit_FunctionDeclaration"
        pass

    def visit_UnaryOperator(self, node):
        print "in visit_UnaryOperator"
        pass

    def visit_BinaryOperator(self, node):
        print "in visit_BinaryOperator"
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
        self.code_object.code.append(('LOAD_VALUE', node.value))
        return node.value

    def visit_Compound(self, node):
        print "in visit_Compound"
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        print "in visit_NoOp"
        pass

    def visit_Assign(self, node):
        print "in visit_Assign"
        self.visit(node.left)
        self.visit(node.right)
        variable_name = node.left.value
        self.code_object.code.append(('STORE_NAME', variable_name))
        print self.code_object.code
