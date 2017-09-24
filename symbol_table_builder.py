from node_visitor import NodeVisitor
from symbol_table import SymbolTable
from variable_symbol import VariableSymbol

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_BinaryOperator(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Number(self, node):
        pass

    def visit_UnaryOperator(self, node):
        self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        variable_name = node.left.value
        type_symbol = node.left
        variable_symbol = VariableSymbol(variable_name, type_symbol)
        self.symbol_table.insert(variable_symbol)

    def visit_VariableDeclaration(self, node):
        type_name = node.type.value
        type_symbol = self.symbol_table.lookup(type_name)
        variable_name = node.variable.value
        variable_symbol = VariableSymbol(variable_name, type_symbol)
        self.symbol_table.insert(variable_symbol)

    def visit_FunctionDeclaration(self, node):
        pass
