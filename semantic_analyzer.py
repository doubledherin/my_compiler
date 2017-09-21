from node_visitor import NodeVisitor
from symbol_table import SymbolTable

class SemanticAnalyzer(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable
        self.GLOBAL_SCOPE = OrderedDict()

    def visit_UnaryOperator(self, node):
        if node.op.type == tokens.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == tokens.MINUS:
            return -self.visit(node.expr)

    def visit_BinaryOperator(self, node):
        if node.op.type == tokens.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == tokens.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == tokens.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == tokens.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
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
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)






    def __init__(self):
        self.table = SymbolTable()

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
        type_symbol = BuiltInSymbol('INTEGER')
        self.table.insert(type_symbol)

        variable_name = node.variable_node.value
        variable_symbol = VariableSymbol(variable_symbol)
        if self.table.lookup(variable_name) is not None:
                raise Exception(
                    "Error: Duplicate identifier '%s' found" % variable_name
                )

        self.table.insert(variable_symbol)
        self.table.insert(variable_symbol)

    def visit_Variable(self, node):
        var_name = node.value
        var_symbol = self.table.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )

    def visit_Assign(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_BinaryOperator(self, node):
        self.visit(node.left)
        self.visit(node.right)
