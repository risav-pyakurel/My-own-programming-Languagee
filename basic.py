# Declaring digits constant
DIGITS = '0123456789'

# Creating an error class
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

# making new class position where it keeps track of column number line number and current index

class Position:
    def __init__(self, index, line_num, col_num):
        self.index = index
        self.line_num = line_num
        self.col_num = col_num

    def advance(self, current_char):
        self.index +=1
        self.col_num +=1

        if current_char == '\n':
            self.line_num +=1
            self.col_num = 0
        return self
    def copy(self):
        return Position(self.index, self.line_num, self.col_num)

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
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.current_character = None
        self.advance()

    def advance(self):
        self.position += 1
        self.current_character = self.text[self.position] if self.position < len(self.text) else None

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
                char = self.current_character
                self.advance()
                return [], IllegalCharacterError("'" + char + "'")
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

# Creating a run function
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error
