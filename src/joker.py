import os

import requests

from compinterpret import SimpleStringCrawler, BaseTokenizer, Token as BaseToken, catch_tokenizer_errors


OPERATOR_TOKENS = {"INC", "DEC", "ADD", "SUBTRACT", "NOT", "MULTIPLY", "EXPONENT", "DIVIDE", "AND", "OR",
          "BIT_AND", "BIT_OR_EX", "BIT_OR_IN", "MODULO", "BIT_SHIFT_LEFT", "BIT_SHIFT_RIGHT_EX", "BIT_SHIFT_RIGHT_0",
          "GTHAN", "LTHAN", "GEQUAL", "LEQUAL", "EQUAL", "LOOSE_EQUAL", "PRECISE_EQUAL", "LITERAL_EQUAL",
          "ADD_ASSIGN", "SUBTRACT_ASSIGN", "MULT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "EXP_ASSIGN", "ARROW",
          '(', ')', '[', ']', '{', '}', 'NOT_EQUAL'}

RESERVED_WORDS = {"!", "IF", 'ELSE', 'TRUE', 'FALSE', 'CONST', 'VAR', 'INFINITY', 'FUNCTION', 'PREVIOUS',
                  'NEXT', 'AWAIT', 'EXPORT', 'TO', 'CLASS', 'NEW', 'USE', 'DELETE', 'CURRENCY', 'WHEN',
                  'RETURN', 'IMPORT', 'COMMA'}

INTERNAL_TOKENS = {'INDENT', 'SPACE', 'EOF', 'NEWLINE', 'IDENTIFIER', 'NEW_FILE', 'ERROR'}

MISC_TOKENS = {'.', ":"}

TOKENS = RESERVED_WORDS | OPERATOR_TOKENS | INTERNAL_TOKENS | MISC_TOKENS


class Token(BaseToken):
    __slots__ = ()
    valid_token_names = TOKENS


class Tokenizer(BaseTokenizer[Token]):
    __slots__ = ()
    basic_mappings = {
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
    operators = '+-*/\\<>=()[] \t\n\r%^&|'
    reserved_chars = '!;:.{},' + operators

    def __init__(self) -> None:
        super().__init__(Token)

    def getNextToken(self, file: SimpleStringCrawler) -> Token:
        def readchar(i: int = 1) -> str:
            return ''.join(file.pop() for _ in range(i))

        c = readchar()
        if c == '':
            # The file has ended
            return self._token('EOF', '')

        lexeme = ''

        if c == ' ':
            if file.peek(2) == '  ':
                c += file.pop()
                c += file.pop()
                # 3-space indent
                return self._token('INDENT', c)
            else:
                print(f"   -2   {c}")
                return self._token('SPACE', c)

        elif c in '+-*/\\<>%;':
            if file.peek() == '=':
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
                return self._token(token_map[c], c + '=')
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
                    return self._token('EXP_ASSIGN', '**=')
                return self._token(token_map[c], c*2)
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
                return self._token(token_map[c], c)

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
                    return self._token('ARROW', '=>')
                return self._token('EQUAL', '=')
            elif equals == 2:
                return self._token('LOOSE_EQUAL', '==')
            elif equals == 3:
                return self._token('PRECISE_EQUAL', '===')
            elif equals == 4:
                return self._token('LITERAL_EQUAL', '====')
            else:  # TODO: File splits (might have to be a preprocessor thing)
                return self._token('ERROR', 'Too much Equality (max is 4)')

        elif c == '>':
            if file.peek() == '>':
                file.pop()
                if file.peek() == '>':
                    file.pop()
                    return self._token('BIT_SHIFT_RIGHT_0', '>>>')
                else:
                    return self._token('BIT_SHIFT_RIGHT_EX', '>>')
            else:
                return self._token('GTHAN', '>')

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
                return self._token('STRING', quote)
            elif c == '\n':
                # Line breaks within strings are not allowed, so the string ends here
                return self._token('STRING', quote)
            else:
                # If there are end quotes, they must match the quote format exactly
                for i in range(len(quote_format)):
                    c = file.pop()
                    if c != quote_format[-(i + 1)]:
                        # Mismatch
                        return self._token('ERROR', 'String quote format mismatched')

                return self._token('STRING', quote)

        # Comments or division with the wrong slash
        elif c == '/':
            if file.peek() == '/':
                file.pop()  # Get rid of thge next slash
                while c not in '\n\r':
                    c = file.pop()
                file.back()
                return self.getNextToken(file)  # Should capture newline
            else:
                return self._token('DIVIDE', c)


        elif c in self.basic_mappings.keys():
            return self._token(self.basic_mappings[c], c)

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
                    return self._token('ERROR', 'Non-Operator immediately after real; letters are not real')

                file.back()

                return self._token('IDENTIFIER', float(lexeme))

            else:
                # INT
                return self._token('IDENTIFIER', int(lexeme))

        while not c.isspace() and c not in self.reserved_chars:
            lexeme += c

            c = readchar()

        if lexeme:
            file.back()
            tok = lexeme.upper()
            if tok in TOKENS:
                return self._token(lexeme, lexeme)

            # Case sensitive for maximum user disgruntlement
            if lexeme == 'className':
                return self._token('CLASS', lexeme)
            elif tok == 'CLASSNAME':
                # Helpful error message to help insensitive users right their ways
                return self._token('ERROR',
                             'The className keyword is Case-Sensitive, you\'re hurting its feelings you monster')

            # check for function
            if self.is_fn_subset(tok):
                return self._token('FUNCTION', lexeme)
            else:
                return self._token('IDENTIFIER', lexeme)
        else:  # c is not alpha- only remaining case are special characters that count as whitespace
            if c in os.linesep:
                if len(os.linesep) == 2 and readchar() != os.linesep[1]:
                    file.back()
                return self._token('NEWLINE', c)
            elif c == '\t':
                # Was very tempted to force you to only use the 3 spaces but this is complicated enough already
                return self._token('INDENT', c)
            else:
                print(f"   -1   {c}")
                return self._token('SPACE', c)


if __name__ == "__main__":
    tokens = list(Tokenizer().tokenize_file(os.path.join('test', 'db', 'db', 'functions.db')))
    #[print(token) for token in tokens]
