from node_visitor import NodeVisitor
from symbol_table import SymbolTable

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_VariableDeclaration(self, node):
        pass
