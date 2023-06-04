from codecs import decode
from io import TextIOWrapper
import os

tokens = ["QUOTE", ";", "!", "IF", 'ELSE', '(', ')', '[', ']', 'TRUE', 'FALSE', 'CONST', 'VAR', '<', '>', 'INT', 'REAL', 'INFINITY', 'FUNCTION', 'PREVIOUS',
          'NEXT', 'AWAIT', 'NEW_FILE', 'EXPORT', 'TO', 'CLASS', 'NEW', '.', 'USE', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUAL', 'IDENTIFIER', 'INDENT',
           'SPACE', 'DELETE', 'EOF']

class Token():
    def __init__(self, token: str, lexeme: str) -> None:
        global tokens
        assert token.upper() in tokens

        self.token = token.upper()
        self.lexeme = lexeme

def is_fn_subset(string):
    target = "FUNCTION"
    i = 0

    for char in string:
        if char == target[i]:
            i += 1
            if i == len(target):
                return True

    return False

lex_states = ['BEGIN']

def getNextToken(file: TextIOWrapper):
    def readchar(i=1):
        return decode(file.read(i))
    c = readchar()
    lexeme = ''

    basic_mappings = {
        ';': ';',
        '=': 'EQUAL',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '.': '.',
        '(': '(',
        ')': ')',
        '[': ']',
        '<': '<',
        '>': '>'
    }
    operators = '+-*/<>=()[] '

    if c == ' ':
        if readchar(2) == '  ':
            # 3-space indent
            return Token('INDENT', '   ')
        else:
            file.seek(-2, 1)
            return Token('SPACE', ' ')
            
    elif c == '!':
        marks = 0 #while loop will count one over
        while c == '!':
            c = readchar()
            marks += 1
        file.seek(-1, 1) #Pushback
        return Token('!', '!' * marks)       

    elif c in basic_mappings.keys():
        return Token(basic_mappings[c], c)
    
    #INT and REAL
    elif c.isdigit():            
        while c.isdigit():
            lexeme += c
            c = readchar()
        file.seek(-1, 1) #Pushback
        
        if c == '.':
            #REAL
            lexeme += '.'
            c = readchar()
            if c.isdigit():
                while c.isdigit():
                    lexeme += c
                    c = readchar()
            elif c not in operators:
                raise Exception('Tokenizer- Error: Letters are not real')

            file.seek(-1, 1)

            return Token('REAL', float(lexeme))

        else:
            #INT            
            return Token('INT', int(lexeme))

    while c != '' and not c.isspace():
        lexeme += c       

        c = readchar()
    if len(lexeme) > 0:
        tok = lexeme.upper()
        if tok in tokens:
            return Token(lexeme, lexeme)
        
        #check for function
        if is_fn_subset(tok):
            return Token('FUNCTION', lexeme)
        else:
            return Token('IDENTIFIER', lexeme)
    elif c == '':        
        #The file has ended
        return Token('EOF', lexeme)
    else:
        #character is space character like \n, \r, \t
        return Token('SPACE', c)

def tokenize_file(path):
    with open(path, 'rb') as reader:
        token = getNextToken(reader)
        while token.token != 'EOF':
            yield token
            token = getNextToken(reader)
        yield token #yield EOF
        reader.close()

for token in tokenize_file('test\\db\\db\\time_travel.db'):
    print(f'Token: {token.token} | Lex: {token.lexeme}')