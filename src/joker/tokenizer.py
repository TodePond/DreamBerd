import inspect
import locale
import os
import re
from typing import Generator, Iterable, Sequence

import requests

operator_tokens = ["INC", "DEC", "ADD", "SUBTRACT", "NOT", "MULTIPLY", "EXPONENT", "DIVIDE", "AND", "OR",
          "BIT_AND", "BIT_OR_EX", "BIT_OR_IN", "MODULO", "BIT_SHIFT_LEFT", "BIT_SHIFT_RIGHT_EX", "BIT_SHIFT_RIGHT_0",
          "GTHAN", "LTHAN", "GEQUAL", "LEQUAL", "EQUAL", "LOOSE_EQUAL", "PRECISE_EQUAL", "LITERAL_EQUAL",
          "ADD_ASSIGN", "SUBTRACT_ASSIGN", "MULT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "EXP_ASSIGN", "ARROW",
          '(', ')', '[', ']', '{', '}', 'NOT_EQUAL']

reserved_words = ["!", "IF", 'ELSE', 'TRUE', 'FALSE', 'CONST', 'VAR', 'INFINITY', 'FUNCTION', 'PREVIOUS', 
                  'NEXT', 'AWAIT', 'EXPORT', 'TO', 'CLASS', 'NEW', 'USE', 'DELETE', 'CURRENCY', 'WHEN', 
                  'RETURN', 'IMPORT', 'COMMA']

internal_tokens = ['INDENT', 'SPACE', 'EOF', 'NEWLINE', 'IDENTIFIER', 'NEW_FILE', 'ERROR']

misc_tokens = ['.', ":"]
          
tokens = reserved_words + operator_tokens + internal_tokens + misc_tokens

class Token:
    __slots__ = ("token", "lexeme")
    def __init__(self, token: str, lexeme: str | int | float) -> None:
        global tokens
        assert token.upper() in tokens

        self.token = token.upper()
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f'{self.token}({repr(self.lexeme)})'

    def __str__(self) -> str:
        return f'{self.token}({repr(self.lexeme)})'


class SimpleStringCrawler:
    __slots__ = ("raw", "cursor")
    def __init__(self, raw: str) -> None:
        self.raw = raw
        self.cursor = 0

    def pop(self) -> str:
        if self.cursor == len(self.raw):
            return ''
        self.cursor += 1
        return self.raw[self.cursor - 1]

    def back(self, count: int = 1) -> None:
        self.cursor -= count

    def peek(self, count: int = 1, ignore_space: bool = False) -> str:
        if self.cursor == len(self.raw):
            return ''
        if ignore_space:
            effective_cursor = self.cursor
            while self.raw[effective_cursor] in ' \n\t\r':
                effective_cursor += 1
            return self.raw[effective_cursor]
        return self.raw[self.cursor:self.cursor + count]


class Tokenizer:
    __slots__ = ("operators", "reserved_chars", "basic_mappings")
    def __init__(self) -> None:
        self.operators = '+-*/\\<>=()[] \t\n\r%^&|'
        self.reserved_chars = '!;:.{},' + self.operators

        self.basic_mappings = {
            ';': 'NOT',
            '\\': 'DIVIDE',
            '.': '.',
            '(': '(',
            ')': ')',
            '[': ']',
            '{': '{',
            '}': '}',
            ":": ':',  # bruh
            "!": "!",
            "^": "BIT_OR_EX",
            '<': 'LTHAN',
            '>': 'GTHAN',
            '%': 'MODULO',
            ',': 'COMMA'         
        }

        locale.setlocale(locale.LC_ALL, '')
        regional_currency = str(locale.localeconv()['currency_symbol'])
        if regional_currency == '':
            # For maximum international accessibility, the generic currency sign is used if there is no currency sign for the given locale
            regional_currency = '¤'
        self.basic_mappings[regional_currency] = 'CURRENCY'

    def is_fn_subset(self, string: str) -> bool:
        # to solve the function syntax I created this regex:
        # if it doesn't get exactly one match then the word is invalid
        function_regex = r"(?=.)(f{0,1}u{0,1}n{0,1}c{0,1}t{0,1}i{0,1}o{0,1}n{0,1})"
        groups = re.findall(function_regex, string, re.IGNORECASE)
        # the and is needed because if there is no match an empty string is the resulting group
        return len(groups) == 1 and groups[0]

    def getNextToken(self, file: SimpleStringCrawler) -> Token:
        def readchar(i: int = 1) -> str:
            return ''.join(file.pop() for _ in range(i))

        c = readchar()
        if c == '':
            # The file has ended
            return Token('EOF', '')

        lexeme = ''

        if c == ' ':
            if file.peek(2) == '  ':
                c += file.pop()
                c += file.pop()
                # 3-space indent
                return Token('INDENT', c)
            else:
                print(f"   -2   {c}")
                return Token('SPACE', c)

        elif c in '+-*/\\<>%;' and file.peek() == '=':
            file.pop()
            token_map = {
                '+': 'ADD_ASSIGN',
                '-': 'SUBTRACT_ASSIGN',
                '*': 'MULT_ASSIGN',
                '/': 'DIV_ASSIGN',
                '\\': 'DIV_ASSIGN',
                '<': 'LEQUAL',
                '>': 'GEQUAL',
                '%': 'MOD_ASSIGN',
                ';': 'NOT_EQUAL'
            }
            return Token(token_map[c], c + '=')
            # Let it continue if not followed by equal sign


        elif c in '+-*&|<':
            next_char = readchar()
            if c == next_char:
                token_map = {
                    '+': 'INC',
                    '-': 'DEC',
                    '*': 'EXPONENT',
                    '&': 'AND',
                    '|': 'OR',
                    '<': 'BIT_SHIFT_LEFT'
                }
                if c == '*' and file.peek() == '=':
                    return Token('EXP_ASSIGN', '**=')
                return Token(token_map[c], c*2)
            else:
                file.back()
                token_map = {
                    '+': 'ADD',
                    '-': 'SUBTRACT',
                    '*': 'MULTIPLY',
                    '&': 'BIT_AND',
                    '|': 'BIT_OR_IN',
                    '<': 'LTHAN'
                }
                return Token(token_map[c], c)

        elif c == '=':
            equals = 0  # while loop will count one over
            while c == '=':
                c = readchar()
                equals += 1
            file.back()  # Pushback
            if equals == 1:
                if c == ">":
                    # consume the ">"
                    readchar()
                    return Token('ARROW', '=>')
                return Token('EQUAL', '=')
            elif equals == 2:
                return Token('LOOSE_EQUAL', '==')
            elif equals == 3:
                return Token('PRECISE_EQUAL', '===')
            elif equals == 4:
                return Token('LITERAL_EQUAL', '====')
            else:  # TODO: File splits (might have to be a preprocessor thing)
                return Token('ERROR', 'Too much Equality (max is 4)')

        elif c == '>':
            if file.peek() == '>':
                file.pop()
                if file.peek() == '>':
                    file.pop()
                    return Token('BIT_SHIFT_RIGHT_0', '>>>')
                else:
                    return Token('BIT_SHIFT_RIGHT_EX', '>>')
            else:
                return Token('GTHAN', '>')

        elif c in '\"\'':
            quote_format = ''
            while c in '\"\'':
                quote_format += c
                c = file.pop()

            # leave c at the next char, it'll be added to the string

            quote = ''
            while c not in '\"\'\n' and c != '':
                quote += c
                if c == '\\':
                    if file.peek() in '\"\'':
                        quote += file.pop()  # Character already escaped
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
                    if c != quote_format[-(i + 1)]:
                        # Mismatch
                        return Token('ERROR', 'String quote format mismatched')

                return Token('STRING', quote)

        # Comments or division with the wrong slash
        elif c == '/':
            if file.peek() == '/':
                file.pop()  # Get rid of thge next slash
                while c not in '\n\r':
                    c = file.pop()
                file.back()
                return self.getNextToken(file)  # Should capture newline
            else:
                return Token('DIVIDE', c)       
        

        elif c in self.basic_mappings.keys():
            return Token(self.basic_mappings[c], c)

        # INT and REAL (really just IDENTIFIERS)
        elif c.isdigit():
            while c.isdigit():
                lexeme += c
                c = readchar()
            file.back()  # Pushback

            # c is one character beyond the end
            if c == '.':
                # REAL
                lexeme += '.'
                c = readchar()
                if c.isdigit():
                    while c.isdigit():
                        lexeme += c
                        c = readchar()
                elif c not in self.operators:
                    return Token('ERROR', 'Non-Operator immediately after real; letters are not real')

                file.back()

                return Token('IDENTIFIER', float(lexeme))

            else:
                # INT
                return Token('IDENTIFIER', int(lexeme))

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
                return Token('ERROR',
                             'The className keyword is Case-Sensitive, you\'re hurting its feelings you monster')

            # check for function
            if self.is_fn_subset(tok):
                return Token('FUNCTION', lexeme)
            else:
                return Token('IDENTIFIER', lexeme)
        else:  # c is not alpha- only remaining case are special characters that count as whitespace
            if c in os.linesep:
                if len(os.linesep) == 2 and readchar() != os.linesep[1]:
                    file.back()
                return Token('NEWLINE', c)
            elif c == '\t':
                # Was very tempted to force you to only use the 3 spaces but this is complicated enough already
                return Token('INDENT', c)
            else:
                print(f"   -1   {c}")
                return Token('SPACE', c)

    def tokenize_file(self, path: str) -> Generator[Token, None, None]:
        crawler = None
        with open(path, 'r') as reader:
            crawler = SimpleStringCrawler(reader.read())
            reader.close()

        token = self.getNextToken(crawler)        
        while token.token != 'EOF':
            yield token
            token = self.getNextToken(crawler)
        yield token  # yield EOF


def catch_tokenizer_errors(tokens: Iterable[Token]) -> bool:
    line = 1
    has_errors = False
    for token in tokens:
        if token.token == 'NEWLINE':
            line += 1
        elif token.token == 'ERROR':
            print(f'-Tokenizer: ParseError on Line {line}: {token.lexeme}')
            has_errors = True
    return has_errors

if __name__ == "__main__":
    tokens = list(Tokenizer().tokenize_file(os.path.join('test', 'db', 'db', 'functions.db')))
    out = ""
    for token in tokens:
        if token.token == 'NEWLINE':
            out += '\n'
        else:
            out += token.token + ' '
    print(out)
    