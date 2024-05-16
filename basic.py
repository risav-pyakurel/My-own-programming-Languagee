# Declaring digits constant

DIGITS = '0123456789'


# creating an error class

class Error:
    def __init__(self,error_name, details):
        self.error_name = error_name
        self.details = details
    def as_string(self):
         result = f'{self.error_name}: {self.details}'
         return result

class Illegal_character_Error(Error): #Illegal characterError is standard error  used when lexer comes across the char that doesn't support
    def __init__(self, details):
        super().__init__('Illegal Character', details)


# working on token class

TT_INT= 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL= 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

class Token :
    def __init__(self,type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type} : {self.value}'
        return f'{self.type}'


#now we work on lexer class
class Lexer:
    def __init__(self,text):
        self.text =text
        self.position = -1
        self.current_character = None
        self.advance()


    def advance(self):
        self.position +=1
        self.current_character = self.text[position] if self.position < len(self.text) else None

        def make_tokens(self):
            tokens= []
            while self.current_character != None:
                if self.current_character in ' \t':
                    self.advance()
                elif self.current_character in DIGITS:
                    tokens.append(self.make_number())

                elif self.current_character == '+':
                    tokens.append(Token(TT_PLUS))
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

                else:    #   if we don't find the character we are looking for we have to throw the error
                     char= self.current_character
                     self.advance()
                     return [], Illegal_character_Error( "'" +char + "'")
                
                








            return tokens

        def make_number(self):
            num_str= ''
            dot_count= 0

            while self.current_character != None and self.current_character in DIGITS + '.':
                if self.current_character == '.':
                    dot_count +=1
                    num_str += '.'

                else:
                    num_str += self.current_char

            if dot_count == 0:
                return Token(TT_INT, int(num_str))
            else:
                return Token(TT_FLOAT, float(num_str))







