from node_visitor import NodeVisitor
from scoped_symbol_table import ScopedSymbolTable
from built_in_symbol import BuiltInSymbol
from variable_symbol import VariableSymbol
from function_symbol import FunctionSymbol

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        print 'Entering global scope...'
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = global_scope
        self.visit(node.block)
        print global_scope
        self.current_scope = self.current_scope.enclosing_scope
        print 'Leaving global scope...'

    def visit_FunctionDeclaration(self, node):
        function_name = node.name
        function_symbol = FunctionSymbol(function_name)
        self.current_scope.insert(function_symbol)

        print 'Entering %s scope' % function_name
        function_scope = ScopedSymbolTable(
            scope_name=function_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = function_scope

        for parameter in node.parameters:
            parameter_type = self.current_scope.lookup(parameter.type_node.value)
            parameter_name = parameter.variable_node.value
            variable_symbol = VariableSymbol(parameter_name, parameter_type)
            self.current_scope.insert(variable_symbol)
            function_symbol.parameters.append(variable_symbol)

        self.visit(node.block)
        print function_scope
        self.current_scope = self.current_scope.enclosing_scope
        print 'Leaving %s scope' % function_name

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Number(self, node):
        pass

    def visit_VariableDeclaration(self, node):
        type_name = node.type.value
        type_symbol = self.current_scope.lookup(type_name)
        variable_name = node.variable.value
        variable_symbol = VariableSymbol(variable_name, type_symbol)
        if self.current_scope.lookup(variable_name) is not None:
            raise Exception(
                'Duplicate declaration for variable %s found' % variable_name
        )
        self.current_scope.insert(variable_symbol)

    def visit_Variable(self, node):
        variable_name = node.value
        variable_symbol = self.current_scope.lookup(variable_name)
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
