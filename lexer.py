import token_names as tokens
from token import Token

RESERVED_KEYWORDS = {
    'int': Token('int', 'int'),
    'var': Token('var', 'var'),
    'function': Token('function', 'function')
}

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, message):
        raise Exception(message)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        self.advance()
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        """Handles both variables and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(tokens.ID, result))
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isalpha():
                return self._id()
            if self.current_char == '=' and self.peek() != '=':
                self.advance()
                self.advance()
                return Token(tokens.ASSIGN, '=')
            if self.current_char == ';':
                self.advance()
                return Token(tokens.SEMI, ';')
            if self.current_char == ',':
                self.advance()
                return Token(tokens.COMMA, ',')
            if self.current_char == ':':
                self.advance()
                return Token(tokens.COLON, ':')
            if self.current_char == '!':
                self.advance()
                return Token(tokens.BANG, '!')
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '#':
                self.skip_comment()
                continue
            if self.current_char.isdigit():
                return Token(tokens.INT, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(tokens.PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(tokens.MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(tokens.MULTIPLY, '*')
            if self.current_char == '/':
                self.advance()
                return Token(tokens.DIVIDE, '/')
            if self.current_char == '(':
                self.advance()
                return Token(tokens.LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(tokens.RPAREN, ')')
            if self.current_char == '{':
                self.advance()
                return Token(tokens.OPEN, '{')
            if self.current_char == '}':
                self.advance()
                return Token(tokens.CLOSE, '}')
            self.error('Unknown character %s found' % self.current_char)
        return Token(tokens.EOF, None)
