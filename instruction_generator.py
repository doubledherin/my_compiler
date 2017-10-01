from node_visitor import NodeVisitor
import token_names as tokens
from code import Code

class InstructionGenerator(NodeVisitor):
    def __init__(self):
        self.code = Code()

    def __call__(self, tree):
        self.visit(tree)

    def visit_Program(self, node):
        # print "in visit_Program"
        self.visit(node.block)

    def visit_Block(self, node):
        # print "in visit_Block"
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Variable(self, node):
        # print "in visit_Variable"
        self.code.instructions.append(('LOOKUP_AND_PUSH_VALUE', node.value))

    def visit_VariableDeclaration(self, node):
        # print "in visit_VariableDeclaration"
        pass

    def visit_FunctionDeclaration(self, node):
        # print "in visit_FunctionDeclaration"
        pass

    def visit_UnaryOperator(self, node):
        # print "in visit_UnaryOperator"
        pass

    def visit_BinaryOperator(self, node):
        # print "in visit_BinaryOperator"
        if node.op.type == tokens.PLUS:
            self.code.instructions.append(('ADD_TWO_VALUES', None))
            self.visit(node.left)
            self.visit(node.right)
        elif node.op.type == tokens.MINUS:
            self.code.instructions.append(('SUBTRACT_TWO_VALUES', None))
            self.visit(node.left)
            self.visit(node.right)
        elif node.op.type == tokens.MULTIPLY:
            self.code.instructions.append(('MULTIPLY_TWO_VALUES', None))
            self.visit(node.left)
            self.visit(node.right)
        elif node.op.type == tokens.DIVIDE:
            self.code.instructions.append(('DIVIDE_TWO_VALUES', None))
            self.visit(node.left)
            self.visit(node.right)

    def visit_Number(self, node):
        # print "in visit_Number"
        index = len(self.code.number_stack)
        self.code.instructions.append(('PUSH_VALUE', index))
        self.code.number_stack.append(node.value)
        return node.value

    def visit_Compound(self, node):
        # print "in visit_Compound"
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        # print "in visit_NoOp"
        return self.code

    def visit_Assign(self, node):
        # print "in visit_Assign"
        self.visit(node.left)
        self.visit(node.right)
        index = len(self.code.name_stack)
        name = node.left.value
        self.code.instructions.append(('ASSIGN', index))
        self.code.name_stack.append(name)

    def visit_Print(self, node):
        # print "in visit_Print"
        self.code.instructions.append(('PRINT', None))
        self.visit(node.expr)
