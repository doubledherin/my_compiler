import token_names as tokens
import abstract_syntax_tree as AST

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set initial current token to first token in input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == tokens.INTEGER:
            self.eat(tokens.INTEGER)
            return AST.Num(token)
        if token.type == tokens.PLUS:
            self.eat(tokens.PLUS)
            node = AST.UnaryOp(token, self.factor())
            return node
        if token.type == tokens.MINUS:
            self.eat(tokens.MINUS)
            node = AST.UnaryOp(token, self.factor())
            return node
        if token.type == tokens.LPAREN:
            self.eat(tokens.LPAREN)
            node = self.expr()
            self.eat(tokens.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """term : factor (MULTIPLY | DIVIDE) factor)*"""
        node = self.factor()

        while self.current_token.type in (tokens.MULTIPLY, tokens.DIVIDE):
            token = self.current_token
            if token.type == tokens.MULTIPLY:
                self.eat(tokens.MULTIPLY)
            elif token.type == tokens.DIVIDE:
                self.eat(tokens.DIVIDE)
            node = AST.BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MULTIPLY | DIVIDE) factor)*
        factor : (PLUS | MINUS)factor | INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (tokens.PLUS, tokens.MINUS):
            token = self.current_token
            if token.type == tokens.PLUS:
                self.eat(tokens.PLUS)
            elif token.type == tokens.MINUS:
                self.eat(tokens.MINUS)
            node = AST.BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != tokens.EOF:
            self.error()
        return node

    def program(self):
        """program : compound_statement BANG"""
        node = self.compound_statement()
        self.eat(tokens.BANG)
        return node

    def compound_statement(self):
        """compound_statement : OPEN statement_list CLOSE"""
        self.eat(tokens.OPEN)
        nodes = self.statement_list()
        self.eat(tokens.CLOSE)

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
            self.eat(tokens.SEMI)
            results.append(self.statement())
        if self.current_token.type == tokens.ID:
            self.error()

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
        self.eat(tokens.ASSIGN)
        right = self.expr()
        node = AST.Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = AST.Var(self.current_token)
        self.eat(tokens.ID)
        return node

    def empty(self):
        """An empty production"""
        return AST.NoOp()
