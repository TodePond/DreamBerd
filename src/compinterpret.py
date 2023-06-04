from io import TextIOWrapper
import os

tokens = ["QUOTE", ";", "!", "IF", 'ELSE', '(', ')', '[', ']', 'TRUE', 'FALSE', 'CONST', 'VAR', '<', '>', 'INT', 'REAL', 'INFINITY', 'FUNCTION', 'PREVIOUS',
          'NEXT', 'AWAIT', 'NEW_FILE', 'EXPORT', 'TO', 'CLASS', 'NEW', '.', 'USE', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUAL', 'IDENTIFIER', 'INDENT', 'SPACE']

class Token():
    def __init__(self, token: str, lexeme: str) -> None:
        global tokens
        assert token.upper() in tokens

        self.token = token.upper()
        self.lexeme = lexeme

lex_states = ['BEGIN']

def getNextToken(file: TextIOWrapper):
    c = file.read(1)[0]
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

    while c != '':
        if c == ' ':
            if file.read(2) == '  ':
                # 3-space indent
                return Token('INDENT', '   ')
            else:
                file.seek(-2, 1)
                return Token('SPACE', ' ')
                
        if c == '!':
            marks = 0 #while loop will count one over
            while c == '!':
                c = file.read(1)
                mark += 1
            file.seek(-1, 1) #Push back a character
            return Token('!', '!' * marks)       

        if c in basic_mappings.keys():
            return Token(basic_mappings[c], c)
        
        

        c = file.read(1)
    
    #If it gets this far, the file has ended
    return Token('EOF', lexeme)

def tokenize_file(path):
    with open(path, 'r') as reader:
        token = getNextToken(reader)
        while token.token != 'EOF':
            yield token
            token = getNextToken(reader)
        yield token #yield EOF
        reader.close()