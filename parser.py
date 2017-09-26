import token_names as tokens
import abstract_syntax_tree as AST

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(message)

    def consume(self, token_type):
        if self.current_token.type == token_type:
            print "Consuming %s" % token_type
            self.current_token = self.lexer.get_next_token()
        else:
            error_message = """
                Trying to consume token type \'{}\' but current token type is \'{}\'
            """.format(token_type, self.current_token.type)
            self.error(error_message)

    def program(self):
        """
        program : PROGRAM variable SEMI block BANG
        """
        self.consume(tokens.PROGRAM)
        variable_node = self.variable()
        program_name = variable_node.value
        self.consume(tokens.SEMI)
        block_node = self.block()
        self.consume(tokens.BANG)
        program_node = AST.Program(program_name, block_node)
        return program_node

    def block(self):
        """
        block : declarations compound_statement
        """
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        block_node = AST.Block(declaration_nodes, compound_statement_node)
        return block_node

    def declarations(self):
        """declarations : (VAR (variable_declaration SEMI)+)*
                        | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
                        | empty
        """
        declarations = []
        while True:
            if self.current_token.type == tokens.VAR:
                self.consume(tokens.VAR)
                while self.current_token.type == tokens.ID:
                    declarations.extend(self.variable_declarations())
                    self.consume(tokens.SEMI)
            if self.current_token.type == tokens.FUNCTION:
                while self.current_token.type == tokens.FUNCTION:
                    self.consume(tokens.FUNCTION)
                    function_name = self.current_token.value
                    self.consume(tokens.ID)
                    if self.current_token.type == tokens.LPAREN:
                        self.consume(tokens.LPAREN)
                        parameters = self.formal_parameter_list()
                        self.consume(tokens.RPAREN)
                    self.consume(tokens.SEMI)
                    block_node = self.block()
                    function_declaration = AST.FunctionDeclaration(function_name, parameters, block_node)
                    declarations.append(function_declaration)
            else:
                break
        return declarations

    def formal_parameter_list(self):
        """ formal_parameter_list : formal_parameters
                                  | formal_parameters SEMI formal_parameter_list
        """
        if not self.current_token.type == tokens.ID:
            return []
        parameter_nodes = self.formal_parameters()
        while self.current_token.type == tokens.SEMI:
            self.consume(tokens.SEMI)
            parameter_nodes.extend(self.formal_parameters())
        return parameter_nodes


    def formal_parameters(self):
        """ formal_parameters : ID (COMMA ID)* COLON type_spec """
        parameter_nodes = []
        parameter_tokens = [self.current_token]
        self.consume(tokens.ID)
        while self.current_token.type == tokens.COMMA:
            self.consume(tokens.COMMA)
            parameter_tokens.append(self.current_token)
            self.consume(tokens.ID)
        self.consume(tokens.COLON)
        type_node = self.type_spec()
        for token in parameter_tokens:
            parameter_node = AST.Parameter(AST.Variable(token), type_node)
            parameter_nodes.append(parameter_node)
        return parameter_nodes

    def variable_declarations(self):
        """
        variable_declarations : ID (COMMA ID)* COLON type_spec
        """
        variable_nodes = []
        variable_nodes.append(AST.Variable(self.current_token))
        self.consume(tokens.ID)
        while self.current_token.type == tokens.COMMA:
            self.consume(tokens.COMMA)
            variable_nodes.append(AST.Variable(self.current_token))
            self.consume(tokens.ID)
        self.consume(tokens.COLON)
        type_node = self.type_spec()
        variable_declarations = [
            AST.VariableDeclaration(variable_node, type_node) for variable_node in variable_nodes
        ]
        return variable_declarations

    def type_spec(self):
        """
        type_spec : INTEGER | REAL
        """
        token = self.current_token
        if self.current_token.type == tokens.INTEGER:
            self.consume(tokens.INTEGER)
            return AST.Type(token)
        elif self.current_token.type == tokens.REAL:
            self.consume(tokens.REAL)
            return AST.Type(token)
        else:
            self.error('Unexpected token type %s in type_spec function'.format(self.current_token.type))

    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | REAL
               | LPAREN expr RPAREN
               | variable
        """
        token = self.current_token
        if token.type == tokens.INTEGER:
            self.consume(tokens.INTEGER)
            return AST.Number(token)
        if token.type == tokens.REAL:
            self.consume(tokens.REAL)
            return AST.Number(token)
        if token.type == tokens.PLUS:
            self.consume(tokens.PLUS)
            node = AST.UnaryOperator(token, self.factor())
            return node
        if token.type == tokens.MINUS:
            self.consume(tokens.MINUS)
            node = AST.UnaryOperator(token, self.factor())
            return node
        if token.type == tokens.LPAREN:
            self.consume(tokens.LPAREN)
            node = self.expr()
            self.consume(tokens.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """
        term : factor (MULTIPLY | DIVIDE) factor)*
        """
        node = self.factor()

        while self.current_token.type in (tokens.MULTIPLY, tokens.DIVIDE):
            token = self.current_token
            if token.type == tokens.MULTIPLY:
                self.consume(tokens.MULTIPLY)
            elif token.type == tokens.DIVIDE:
                self.consume(tokens.DIVIDE)
            node = AST.BinaryOperator(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (tokens.PLUS, tokens.MINUS):
            token = self.current_token
            if token.type == tokens.PLUS:
                self.consume(tokens.PLUS)
            elif token.type == tokens.MINUS:
                self.consume(tokens.MINUS)
            node = AST.BinaryOperator(left=node, op=token, right=self.term())
        return node


    def compound_statement(self):
        """compound_statement : OPEN statement_list CLOSE"""
        self.consume(tokens.OPEN)
        nodes = self.statement_list()
        self.consume(tokens.CLOSE)

        root = AST.Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        while self.current_token.type == tokens.SEMI:
            self.consume(tokens.SEMI)
            results.append(self.statement())
        if self.current_token.type == tokens.ID:
            self.error('Unexpected token type %s in statement_list function'.format(self.current_token.type))

        return results

    def statement(self):
        """
        statement : compound_statement | assignment_statement | empty
        """
        if self.current_token.type == tokens.OPEN:
            node = self.compound_statement()
        elif self.current_token.type == tokens.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.consume(tokens.ASSIGN)
        right = self.expr()
        node = AST.Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = AST.Variable(self.current_token)
        self.consume(tokens.ID)
        return node

    def empty(self):
        """An empty production"""
        return AST.NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != tokens.EOF:
            self.error('Expected token type EOF but got %s'.format(self.current_token.type))
        return node
