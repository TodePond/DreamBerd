from codecs import decode
from io import TextIOWrapper
import os

tokens = ["STRING", ";", "!", "IF", 'ELSE', '(', ')', '[', ']', 'TRUE', 'FALSE', 'CONST', 'VAR', '<', '>', 'INT', 'REAL', 'INFINITY', 'FUNCTION', 'PREVIOUS',
          'NEXT', 'AWAIT', 'NEW_FILE', 'EXPORT', 'TO', 'CLASS', 'NEW', '.', 'USE', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', '=', 'IDENTIFIER', 'INDENT',
           'SPACE', 'DELETE', 'EOF', 'NEWLINE', '{', '}', 'INC', 'DEC', 'LOOSE_EQUALITY', 'PRECISE_EQUALITY', 'LITERAL_EQUALITY', 'ERROR']

class Token():
    def __init__(self, token: str, lexeme: str) -> None:
        global tokens
        assert token.upper() in tokens

        self.token = token.upper()
        self.lexeme = lexeme

class SimpleTextCrawler():
    def __init__(self, raw) -> None:
        self.raw = raw
        self.cursor = 0
    
    def pop(self) -> str:
        if self.cursor == len(self.raw):
            return ''
        self.cursor += 1
        return self.raw[self.cursor-1]
    
    def back(self, count=1):
        self.cursor -= count

    def peek(self, count=1):   
        if self.cursor == len(self.raw)-1:
            return ''     
        return self.raw[self.cursor:self.cursor+count]

class Tokenizer():
    def __init__(self) -> None:
        self.operators = '+-*/<>=()[] '
        self.reserved_chars = '!;.{}' + self.operators

    def is_fn_subset(self, string):
        target = "FUNCTION"
        i = 0

        for char in string:
            if char == target[i]:
                i += 1
                if i == len(target):
                    return True

        return False

    def getNextToken(self, file: SimpleTextCrawler):
        def readchar(i=1):
            return ''.join([file.pop() for _ in range(i)])
        
        c = readchar()

        if c == '':        
            #The file has ended
            return Token('EOF', '')

        lexeme = ''

        basic_mappings = {
            ';': ';',
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
            '}': '}'
        }    

        if c == ' ':
            if file.peek(2) == '  ':
                file.pop()
                file.pop()
                # 3-space indent
                return Token('INDENT', '   ')
            else:
                return Token('SPACE', ' ')
                
        elif c == '!':
            marks = 0 #while loop will count one over
            while c == '!':
                c = readchar()
                marks += 1
            if file.peek() != '':
                # File might end after a statment, we want to let it end if it does
                # We can't just blindly push it back or we get an infinite loop
                # TODO: Make sure this doesn't happen elsewhere
                file.back() #Pushback
            return Token('!', '!' * marks)       

        elif c in '+-':
            next_char = readchar()
            if c == next_char:
                return Token('INC' if c == '+' else 'DEC', c*2)
            else:
                file.back()
                return Token('PLUS' if c == '+' else 'MINUS', c)
        
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
            while c not in '\"\'' and c != '':
                quote += c
                if c == '\\':
                    if file.peek() in '\"\'':
                        quote += file.pop() #Character already escaped
                c = file.pop()
            file.back()

            # check for end quotes
            if c == '':
                # EOF reached; User probably forgot the closing quote
                # Due to ambiguity the rest of the file is now a string
                # End quotes are presumed present, thus satisfying AI requirement
                # Diagnosis: skill issue
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

        elif c in basic_mappings.keys():
            return Token(basic_mappings[c], c)
        
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
            crawler = SimpleTextCrawler(reader.read())
            reader.close()

        token = self.getNextToken(crawler)
        while token.token != 'EOF':
            yield token
            token = self.getNextToken(crawler)
        yield token #yield EOF

tokenizer = Tokenizer()
for token in tokenizer.tokenize_file('test\\db\\db\\time_travel.db'):
    print(f'{token.token} | Lex: {repr(token.lexeme)}')