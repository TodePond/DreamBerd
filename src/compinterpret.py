from codecs import decode
import gettext
from io import TextIOWrapper
import os
import locale

tokens = ["STRING", "NOT", "!", "IF", 'ELSE', '(', ')', '[', ']', 'TRUE', 'FALSE', 'CONST', 'VAR', '<', '>', 'INT', 'REAL', 'INFINITY', 'FUNCTION', 'PREVIOUS',
          'NEXT', 'AWAIT', 'NEW_FILE', 'EXPORT', 'TO', 'CLASS', 'NEW', '.', 'USE', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', '=', 'IDENTIFIER', 'INDENT',
           'SPACE', 'DELETE', 'EOF', 'NEWLINE', '{', '}', 'INC', 'DEC', 'LOOSE_EQUALITY', 'PRECISE_EQUALITY', 'LITERAL_EQUALITY', 'ERROR', 'CURRENCY',
           'WHEN', ":", "AND", 'OR']

locale.setlocale(locale.LC_ALL, '')

class Token():
    def __init__(self, token: str, lexeme: str) -> None:
        global tokens
        assert token.upper() in tokens

        self.token = token.upper()
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f'{self.token}({repr(self.lexeme)})'
    
    def __str__(self) -> str:
        return f'{self.token}({repr(self.lexeme)})'

class SimpleListCrawler():
    def __init__(self, raw) -> None:
        self.raw = raw
        self.cursor = 0
    
    def pop(self):
        if self.cursor == len(self.raw):
            return ''
        self.cursor += 1
        return self.raw[self.cursor-1]
    
    def back(self, count=1):        
        self.cursor -= count
        
    def peek(self, count=1):   
        if self.cursor == len(self.raw)-1:
            return ''     
        if count > 1: # QoL for Token iteration
            return self.raw[self.cursor:self.cursor+count]
        else:
            return self.raw[self.cursor]

class Tokenizer():
    def __init__(self) -> None:
        self.operators = '+-*/<>=()[] '
        self.reserved_chars = '!;:.{}' + self.operators

        self.basic_mappings = {
            ';': 'NOT',
            '=': 'EQUAL',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '.': '.',
            '(': '(',
            ')': ')',
            '[': ']',
            '<': '<',
            '>': '>',
            '{': '{',
            '}': '}',
            ":": ':', #bruh
            "!": "!"
        }    

        regional_currency = locale.localeconv()['currency_symbol']
        if regional_currency == '':
            # For maximum international accessibility, the generic currency sign is used if there is no currency sign for the given locale
            regional_currency = '¤'
        self.basic_mappings[regional_currency] = 'CURRENCY'

    def is_fn_subset(self, string):
        target = "FUNCTION"
        i = 0

        for char in string:
            if char == target[i]:
                i += 1
                if i == len(target):
                    return True

        return False

    def getNextToken(self, file: SimpleListCrawler):
        def readchar(i=1):
            return ''.join([file.pop() for _ in range(i)])
        
        c = readchar()

        if c == '':        
            #The file has ended
            return Token('EOF', '')

        lexeme = ''

        if c == ' ':
            if file.peek(2) == '  ':
                file.pop()
                file.pop()
                # 3-space indent
                return Token('INDENT', '   ')
            else:
                return Token('SPACE', ' ')     

        elif c in '+-':
            next_char = readchar()
            if c == next_char:
                return Token('INC' if c == '+' else 'DEC', c*2)
            else:
                file.back()
                return Token('PLUS' if c == '+' else 'MINUS', c)
            
        elif c in '&|':
            next_char = readchar()
            if c == next_char:
                return Token('AND' if c == '&' else 'OR', c*2)
            else:
                # Let em cook                
                file.back()                
        
        elif c == '=':
            equals = 0 #while loop will count one over
            while c == '=':
                c = readchar()
                equals += 1
            file.back() #Pushback
            match equals:
                case 1:
                    return Token('=', '=')
                case 2:
                    return Token('LOOSE_EQUALITY', '==')
                case 3:
                    return Token('PRECISE_EQUALITY', '===')
                case 4:
                    return Token('LITERAL_EQUALITY', '====')
                case _: # TODO: File splits (might have to be a preprocessor thing)
                    return Token('ERROR', 'Too much Equality (max is 4)')

        elif c in '\"\'':
            quote_format = ''
            while c in '\"\'':
                quote_format += c
                c = file.pop()
            
            #leave c at the next char, it'll be added to the string

            quote = ''
            while c not in '\"\'\n' and c != '':
                quote += c
                if c == '\\':
                    if file.peek() in '\"\'':
                        quote += file.pop() #Character already escaped
                c = file.pop()
            file.back()

            # check for end quotes
            if c == '':
                # EOF reached; User probably forgot a closing quote
                # Due to ambiguity the rest of the file is now a string
                # End quotes are presumed present, thus satisfying AI requirement
                # Diagnosis: skill issue
                return Token('STRING', quote)
            elif c == '\n':
                # Line breaks within strings are not allowed, so the string ends here
                return Token('STRING', quote)
            else:
                # If there are end quotes, they must match the quote format exactly            
                for i in range(len(quote_format)):
                    c = file.pop()
                    if c != quote_format[-(i+1)]:
                        # Mismatch
                        return Token('ERROR', 'String quote format mismatched')
                
                return Token('STRING', quote)

        elif c == '/' and file.peek() == '/':
            file.pop() #Get rid of thge next slash
            while c not in '\n\r':
                c = file.pop()
            file.back()
            return self.getNextToken(file) #Should capture newline

        elif c in self.basic_mappings.keys():
            return Token(self.basic_mappings[c], c)
        
        #INT and REAL
        elif c.isdigit():            
            while c.isdigit():
                lexeme += c
                c = readchar()
            file.back() #Pushback

            # c is one character beyond the end
            if c == '.':
                #REAL
                lexeme += '.'
                c = readchar()
                if c.isdigit():
                    while c.isdigit():
                        lexeme += c
                        c = readchar()
                elif c not in self.operators:
                    return Token('ERROR', 'Non-Operator immediately after real; letters are not real')

                file.back()

                return Token('REAL', float(lexeme))

            else:
                #INT            
                return Token('INT', int(lexeme))

        while not c.isspace() and c not in self.reserved_chars:
            lexeme += c       

            c = readchar()    

        if len(lexeme) > 0: 
            file.back()
            tok = lexeme.upper()
            if tok in tokens:
                return Token(lexeme, lexeme)
            
            # Case sensitive for maximum user disgruntlement
            if lexeme == 'className': 
                return Token('CLASS', lexeme)
            elif tok == 'CLASSNAME':
                # Helpful error message to help insensitive users right their ways
                return Token('ERROR', 'The className keyword is Case-Sensitive, you\'re hurting its feelings you monster')

            #check for function
            if self.is_fn_subset(tok):
                return Token('FUNCTION', lexeme)
            else:
                return Token('IDENTIFIER', lexeme)
        else: #c is not alpha- only remaining case are special characters that count as whitespace
            if c == '\n':
                if readchar() != '\r':
                    file.back()
                return Token('NEWLINE', c)
            elif c == '\r':
                if readchar() != '\n':
                    file.back()
                return Token('NEWLINE', c)
            elif c == '\t':
                # Was very tempted to force you to only use the 3 spaces but this is complicated enough already
                return Token('INDENT', c)
            else:
                return Token('SPACE', c)

    def tokenize_file(self, path):  
        crawler = None  
        with open(path, 'r') as reader:
            crawler = SimpleListCrawler(reader.read())
            reader.close()

        token = self.getNextToken(crawler)
        while token.token != 'EOF':
            yield token
            token = self.getNextToken(crawler)
        yield token #yield EOF


def catch_tokenizer_errors(tokens: list[Token]):
    line = 1
    has_errors = False
    for token in tokens:
        if token.token == 'NEWLINE':
            line += 1
        elif token.token == 'ERROR':
            print(f'-Tokenizer: ParseError on Line {line}: {token.lexeme}')
            has_errors = True
    return has_errors

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.file = SimpleListCrawler(tokens)
        self.var_dict = {}

    def PrimType(sel):
    

if __name__ == '__main__':
    tokens = list(Tokenizer().tokenize_file('test\\db\\db\\time_travel.db'))

    if catch_tokenizer_errors(tokens):
        print('\n')
        print("Tokenizer reports L code, fix your code or I won't compile this garbage")
        exit(1)

