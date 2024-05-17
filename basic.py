# Declaring digits constant
DIGITS = '0123456789'

# Creating an error class
class Error:
    def __init__(self, position_start, position_end, error_name, details):
        self.position_start = position_start
        self.position_end = position_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}, line {self.position_start.line_num + 1}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, position_start, position_end, details):
        super().__init__(position_start, position_end, 'Illegal Character', details)

# Making new class position where it keeps track of column number, line number, and current index
class Position:
    def __init__(self, index, line_num, col_num, file_name, file_text):
        self.index = index
        self.line_num = line_num
        self.col_num = col_num
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char=None):
        self.index += 1
        self.col_num += 1

        if current_char == '\n':
            self.line_num += 1
            self.col_num = 0
        return self

    def copy(self):
        return Position(self.index, self.line_num, self.col_num, self.file_name, self.file_text)

# Working on token class
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

# Now we work on lexer class
class Lexer:
    def __init__(self, file_name, text):
        self.text = text
        self.position = Position(-1, 0, -1, file_name, text)
        self.current_character = None
        self.advance()

    def advance(self):
        self.position.advance(self.current_character)
        self.current_character = self.text[self.position.index] if self.position.index < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_character is not None:
            if self.current_character in ' \t':
                self.advance()
            elif self.current_character in DIGITS:
                tokens.append(self.make_number())
            elif self.current_character == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_character == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_character == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                position_start = self.position.copy()
                char = self.current_character
                self.advance()
                return [], IllegalCharacterError(position_start, self.position, "'" + char + "'")
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_character is not None and self.current_character in DIGITS + '.':
            if self.current_character == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_character
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

# Building different node types
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'

# Defining parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        res = self.expr()
        return res

    def factor(self):
        token = self.current_token

        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(token)
        elif token.type == TT_LPAREN:
            self.advance()
            res = self.expr()
            if self.current_token.type == TT_RPAREN:
                self.advance()
                return res
            else:
                raise Exception("Expected ')'")
        else:
            raise Exception("Expected int or float")

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        left = func()

        while self.current_token is not None and self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left, op_token, right)

        return left

# Creating a run function
def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate Abstract Syntax Tree (AST)
    parser = Parser(tokens)
    ast = parser.parse()
    return ast, None
