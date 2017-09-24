from node_visitor import NodeVisitor
from symbol_table import SymbolTable
from built_in_symbol import BuiltInSymbol
from variable_symbol import VariableSymbol

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
        type_name = node.type.value
        type_symbol = self.symbol_table.lookup(type_name)
        variable_name = node.variable.value
        variable_symbol = VariableSymbol(variable_name, type_symbol)
        if self.symbol_table.lookup(variable_name) is not None:
            raise Exception(
                'Duplicate declaration for variable %s found' % variable_name
        )
        self.symbol_table.insert(variable_symbol)

    def visit_Variable(self, node):
        variable_name = node.value
        variable_symbol = self.symbol_table.lookup(variable_name)
        if not variable_symbol:
            raise Exception(
                "Error: variable %s is undeclared" % variable_name
        )

    def visit_Assign(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinaryOperator(self, node):
        self.visit(node.left)
        self.visit(node.right)
