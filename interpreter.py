# from collections import OrderedDict
#
# import token_names as tokens
# from node_visitor import NodeVisitor
# from built_in_symbol import BuiltInSymbol
# from variable_symbol import VariableSymbol
# from scoped_symbol_table import ScopedSymbolTable
#
# class Interpreter(NodeVisitor):
#
#     def __init__(self, parser):
#         self.parser = parser
#         self.GLOBAL_SCOPE = OrderedDict()
#         self.symbol_table = SymbolTable()
#
#     def visit_Program(self, node):
#         self.visit(node.block)
#
#     def visit_Block(self, node):
#         for declaration in node.declarations:
#             self.visit(declaration)
#         self.visit(node.compound_statement)
#
#     def visit_Variable(self, node):
#         var_name = node.value
#         var_symbol = self.symbol_table.lookup(var_name)
#         if var_symbol is None:
#             raise Exception(
#                 "Error: Symbol(identifier) not found '%s'" % var_name
#             )
#     def visit_VariableDeclaration(self, node):
#         type_symbol = BuiltInSymbol('INTEGER') # TO DO: SET THIS DYNAMICALLY
#         variable_name = node.variable.value
#         variable_symbol = VariableSymbol(variable_name, type_symbol)
#         if self.symbol_table.lookup(variable_name) is not None:
#                 raise Exception(
#                     "Error: Duplicate identifier '%s' found" % variable_name
#                 )
#
#         self.symbol_table.insert(variable_symbol)
#         self.symbol_table.insert(variable_symbol)
#
#     def visit_FunctionDeclaration(self, node):
#         pass
#
#     def visit_UnaryOperator(self, node):
#         if node.op.type == tokens.PLUS:
#             return +self.visit(node.expr)
#         elif node.op.type == tokens.MINUS:
#             return -self.visit(node.expr)
#
#     def visit_BinaryOperator(self, node):
#         if node.op.type == tokens.PLUS:
#             return self.visit(node.left) + self.visit(node.right)
#         elif node.op.type == tokens.MINUS:
#             return self.visit(node.left) - self.visit(node.right)
#         elif node.op.type == tokens.MULTIPLY:
#             return self.visit(node.left) * self.visit(node.right)
#         elif node.op.type == tokens.DIVIDE:
#             return self.visit(node.left) / self.visit(node.right)
#
#     def visit_Number(self, node):
#         return node.value
#
#     def visit_Compound(self, node):
#         for child in node.children:
#             self.visit(child)
#
#     def visit_NoOp(self, node):
#         pass
#
#     def visit_Assign(self, node):
#         variable_name = node.left.value
#         type_symbol = node.left
#         variable_symbol = VariableSymbol(variable_name, type_symbol)
#         self.symbol_table.insert(variable_symbol)
#
#     def visit_Var(self, node):
#         var_name = node.value
#         val = self.symbol_table.get(var_name)
#         if val is None:
#             raise NameError(repr(var_name))
#         else:
#             return val
#
#     def interpret(self):
#         tree = self.parser.parse()
#         return self.visit(tree)
