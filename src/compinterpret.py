from codecs import decode
import gettext
from io import TextIOWrapper
import os
import locale
import requests
import inspect


tokens = ["STRING", "NOT", "!", "IF", 'ELSE', '(', ')', '[', ']', 'TRUE', 'FALSE', 'CONST', 'VAR', '<', '>', 'INT', 'REAL', 'INFINITY', 'FUNCTION', 'PREVIOUS',
          'NEXT', 'AWAIT', 'NEW_FILE', 'EXPORT', 'TO', 'CLASS', 'NEW', '.', 'USE', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', '=', 'IDENTIFIER', 'INDENT',
           'SPACE', 'DELETE', 'EOF', 'NEWLINE', '{', '}', 'INC', 'DEC', 'LOOSE_EQUALITY', 'PRECISE_EQUALITY', 'LITERAL_EQUALITY', 'ERROR', 'CURRENCY',
           'WHEN', ":", "AND", 'OR', 'RETURN']

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

class SimpleStringCrawler():
    def __init__(self, raw) -> None:
        self.raw = raw
        self.cursor = 0
    
    def pop(self) -> str:
        if self.cursor == len(self.raw):
            return ''
        self.cursor += 1
        return self.raw[self.cursor-1]
    
    def back(self, count=1) -> str:        
        self.cursor -= count
        
    def peek(self, count=1) -> str:   
        if self.cursor == len(self.raw)-1:
            return ''     
        return self.raw[self.cursor:self.cursor+count]

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

        locale.setlocale(locale.LC_ALL, '')
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

    def getNextToken(self, file: SimpleStringCrawler):
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
            crawler = SimpleStringCrawler(reader.read())
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

class VarState():
    def __init__(self, allow_reassign: bool, allow_edit: bool, priority: int) -> None:
        self.reassign = allow_reassign # Can set it to something else
        self.edit = allow_edit # Can call methods on this
        self.priority = priority #Amount of '!' after the declaration

class SimpleTokenCrawler():
    def __init__(self, raw: list[Token]) -> None:
        self.raw: list[Token] = raw
        self.cursor = 0
        self.current_line = 1
    
    def pop(self, ignore_space=True) -> Token:
        if self.cursor == len(self.raw):
            return None
        self.cursor += 1

        if ignore_space:
            while self.raw[self.cursor-1].token in ['SPACE', 'INDENT']:
                self.cursor += 1

        if self.raw[self.cursor-1].token == 'NEWLINE':
            self.current_line += 1

        return self.raw[self.cursor-1]
    
    def back(self, count=1, ignore_space=True) -> Token:        
        self.cursor -= count

        if ignore_space:
            while self.raw[self.cursor-1].token in ['SPACE', 'INDENT']:
                self.cursor -= 1
        
    def peek(self, ignore_space=True) -> Token:   
        if self.cursor == len(self.raw)-1:
            return ''   

        if ignore_space:
            offset = 0
            while self.raw[self.cursor+offset].token in ['SPACE', 'INDENT']:
                offset += 1
            return self.raw[self.cursor+offset]
        else:
            return self.raw[self.cursor]

# Running List of things that need to happen in runtime:
# Variable Lifetime checks
# `When` control flow
# Variable assignment priority

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.file = SimpleTokenCrawler(tokens)
        self.js = ""      
        self.var_dict = {}

    def RaiseError(self, message):
        caller_name = inspect.currentframe().f_back.f_code.co_name
        print(f"Parser- ParseError on Line {self.file.current_line} from '{caller_name}': {message}")

    def parse(self):
        return self.StmtList()
    
    ### Every Statement should first check if it is valid in the current location
    ### If it is, it should be self-contained and output its valid JS to file.js
    ### If it is not valid, it should not insert any JS and raise and error
    ### Functions should only be called if they should be true- do not use it to check if something is true
    ### FUNCTION NAMES ARE PART OF THE USER DEBUG INFO

    def StmtList(self):
        while self.file.peek().token != 'EOF':
            if not self.Stmt():
                self.RaiseError('Failed to parse statement')
                return False
        self.file.pop() # For Completeness sake
        return True

    def Stmt(self):
        # Anything with a single equals sign: x = 5, const const x = 6
        if self.file.peek().token in ['CONST', 'VAR']:
            return self.Varable_Declaration_Stmt()
        # Control Flow if ( ... ) { ... } else { ... }

        # Class declarations class x { ... }, className x { ... }

        # Function declarations: fn(x) => { ... }

        # Floating expressions: print(x), x, x == 5
        pass

    def EndStmt(self):
        i = 0
        end = False
        while self.file.peek().token in '!?': # Allow any mix of ! and ?
            self.file.pop()
            i += 1
            end = True
        
        # Due to AI, new lines define a line if an ! is missing
        # New line endings take the lowest priority- lower than a single !
        if self.file.peek().token == 'NEWLINE': 
            self.file.pop()            
            end = True
        
        if end:
            self.js += ';'

        return end, i
            

    # Declaration of a variable
    def Varable_Declaration_Stmt(self):
        # Declaration
        allow_reassign = self.file.pop().token == 'VAR'

        if self.file.peek().token not in ['CONST', 'VAR']:
            self.RaiseError('Double or nothing; Need two const/var keywords to declare variable')
            return False
        
        allow_edit = self.file.pop().token == 'VAR'

        if self.file.peek().token != 'IDENTIFIER':
            self.RaiseError('Identify yourself NOW; Declaration requires variable to declare')
            return False

        # Nothing in native JS allows you to prevent edits, so we only worry about reassignments here
        # Bad reassignments will be caught by JS
        if allow_reassign:
            keyword = 'let'
        else:
            keyword = 'const' #javascript consts are cringe
        
        # We will handle bad edits in compile time

        var_name = self.file.pop().lexeme

        if self.file.peek().token != '=':
            self.RaiseError('PUT AN EQUALS SIGN IN YOUR DECLARATION')
            return False
        self.file.pop()

        rollback_idx = len(self.js)
        self.js += f'{keyword} {var_name} = '
        
        if self.Expr():            
            success, priority = self.EndStmt()
            if not success:
                self.RaiseError('Declaration statement didn\'t end when it should\'ve')
            
            self.var_dict[var_name].append(VarState(allow_reassign, allow_edit, priority))              
        else:
            #Rollback
            self.js = self.js[:rollback_idx]
            self.RaiseError('Failed to parse expression in declaration')
            return False
        
    def Expr(self):
        pass


if __name__ == '__main__':
    try:
        # TODO: Replace with DreamBerd 3const server
        response = requests.head("http://www.google.com", timeout=5)
        if response.status_code != 200:
            print("-Meta: NetworkError: DreamBerd 3const services are down, or you do not have an internet connection. Please rectify either as soon as possible.")
            exit(1)
    except requests.ConnectionError:
        print("-Meta: NetworkError: DreamBerd 3const services are down, or you do not have an internet connection. Please rectify either as soon as possible. ")
        exit(1)


    tokens = list(Tokenizer().tokenize_file('test\\db\\db\\time_travel.db'))

    if catch_tokenizer_errors(tokens):
        print('\n')
        print("Tokenizer reports L code, fix your code or I won't compile this garbage")
        exit(1)

    parse = Parser(tokens).parse()
