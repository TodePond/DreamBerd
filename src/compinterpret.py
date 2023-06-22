import inspect
import locale
import os
import re
from typing import Generator, Iterable, Sequence

import requests

tokens = ["STRING", "NOT", "!", "IF", 'ELSE', '(', ')', '[', ']', 'TRUE', 'FALSE', 'CONST', 'VAR', '<', '>', 'INT',
          'REAL', 'INFINITY', 'FUNCTION', 'PREVIOUS',
          'NEXT', 'AWAIT', 'NEW_FILE', 'EXPORT', 'TO', 'CLASS', 'NEW', '.', 'USE', 'PLUS', 'MINUS', 'MULTIPLY',
          'DIVIDE', '=', 'IDENTIFIER', 'INDENT',
          'SPACE', 'DELETE', 'EOF', 'NEWLINE', '{', '}', 'INC', 'DEC', 'LOOSE_EQUALITY', 'PRECISE_EQUALITY',
          'LITERAL_EQUALITY', 'ERROR', 'CURRENCY',
          'WHEN', ":", "AND", 'OR', 'RETURN', "ARROW"]


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
            ":": ':',  # bruh
            "!": "!"
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
                file.pop()
                file.pop()
                # 3-space indent
                return Token('INDENT', '   ')
            else:
                return Token('SPACE', ' ')

        elif c in '+-':
            next_char = readchar()
            if c == next_char:
                return Token('INC' if c == '+' else 'DEC', c * 2)
            else:
                file.back()
                return Token('PLUS' if c == '+' else 'MINUS', c)

        elif c in '&|':
            next_char = readchar()
            if c == next_char:
                return Token('AND' if c == '&' else 'OR', c * 2)
            else:
                # Let em cook                
                file.back()

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
                return Token('=', '=')
            elif equals == 2:
                return Token('LOOSE_EQUALITY', '==')
            elif equals == 3:
                return Token('PRECISE_EQUALITY', '===')
            elif equals == 4:
                return Token('LITERAL_EQUALITY', '====')
            else:  # TODO: File splits (might have to be a preprocessor thing)
                return Token('ERROR', 'Too much Equality (max is 4)')

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

        elif c == '/' and file.peek() == '/':
            file.pop()  # Get rid of thge next slash
            while c not in '\n\r':
                c = file.pop()
            file.back()
            return self.getNextToken(file)  # Should capture newline

        elif c in self.basic_mappings.keys():
            return Token(self.basic_mappings[c], c)

        # INT and REAL
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

                return Token('REAL', float(lexeme))

            else:
                # INT
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
                return Token('ERROR',
                             'The className keyword is Case-Sensitive, you\'re hurting its feelings you monster')

            # check for function
            if self.is_fn_subset(tok):
                return Token('FUNCTION', lexeme)
            else:
                return Token('IDENTIFIER', lexeme)
        else:  # c is not alpha- only remaining case are special characters that count as whitespace
            if c == os.linesep[0]:
                if len(os.linesep) == 2 and readchar() != os.linesep[1]:
                    file.back()
                return Token('NEWLINE', os.linesep)
            elif c == '\t':
                # Was very tempted to force you to only use the 3 spaces but this is complicated enough already
                return Token('INDENT', c)
            else:
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


class VarState:
    __slots__ = ("reassign", "edit", "priority")
    def __init__(self, allow_reassign: bool, allow_edit: bool, priority: int) -> None:
        self.reassign = allow_reassign  # Can set it to something else
        self.edit = allow_edit  # Can call methods on this
        self.priority = priority  # Amount of '!' after the declaration


class SimpleTokenCrawler:
    __slots__ = ("raw", "cursor", "current_line")
    def __init__(self, raw: Sequence[Token]) -> None:
        self.raw = raw
        self.cursor = 0
        self.current_line = 1

    def pop(self, ignore_space: bool = True) -> Token:
        if self.cursor == len(self.raw):
            return Token('EOF', '')
        self.cursor += 1

        if ignore_space:
            while self.raw[self.cursor - 1].token in ['SPACE', 'INDENT']:
                self.cursor += 1

        if self.raw[self.cursor - 1].token == 'NEWLINE':
            self.current_line += 1

        return self.raw[self.cursor - 1]

    def back(self, count: int = 1, ignore_space: bool = True) -> None:
        self.cursor -= count

        if ignore_space:
            while self.raw[self.cursor - 1].token in ['SPACE', 'INDENT']:
                self.cursor -= 1

    def peek(self, ignore_space: bool = True) -> Token:
        if self.cursor == len(self.raw) - 1:
            return Token('EOF', '')

        if ignore_space:
            offset = 0
            while self.raw[self.cursor + offset].token in ['SPACE', 'INDENT']:
                offset += 1
            res = self.raw[self.cursor + offset]
        else:
            res = self.raw[self.cursor]
        return res

    def peek_n(self, number: int, ignore_space: bool = True) -> Sequence[Token]:
        token_list: list[Token] = []
        stop = False
        original_cursor = self.cursor
        while len(token_list) < number and not stop:
            token = self.peek(ignore_space)
            if token.token == 'EOF':
                stop = True
            token_list.append(token)
            self.cursor += 1
        self.cursor = original_cursor
        return token_list


# Running List of things that need to happen in runtime:
# Variable Lifetime checks
# `When` control flow
# Variable assignment priority

class Parser:
    __slots__ = ("tokens", "file", "js", "var_dict", "wanted_indent", "DEBUG")
    def __init__(self, tokens: Sequence[Token]) -> None:
        self.tokens = tokens
        self.file = SimpleTokenCrawler(tokens)
        self.js = ""
        self.var_dict: dict[str | int | float, list[VarState]] = {}
        # How much indent we are expecting to see at the moment
        self.wanted_indent: dict[int, str] = {}
        self.DEBUG = True
    
    def get_javascript(self) -> str:
        return self.js

    def new_indent(self, source: str) -> None:
        if not self.wanted_indent:
            self.wanted_indent[0] = source
        else:
            index = len(self.wanted_indent)
            self.wanted_indent[index] = source

    def expected_indent(self) -> int:
        expected = 0
        for ind in self.wanted_indent:
            if self.wanted_indent[ind]:
                expected += 1 if self.wanted_indent[ind] == "+" else -1
        return expected

    def RaiseError(self, message: str) -> None:
        cur_frame = inspect.currentframe()
        assert cur_frame is not None
        last_frame = cur_frame.f_back
        assert last_frame is not None
        last_code = last_frame.f_code
        assert last_code is not None
        caller_name = last_code.co_name
        if self.DEBUG:
            print(self.js)
        print(f"Parser- ParseError on Line {self.file.current_line} from '{caller_name}': {message}")

    def parse(self) -> bool:
        return self.StmtList()

    ### Every Statement should first check if it is valid in the current location
    ### If it is, it should be self-contained and output its valid JS to file.js
    ### If it is not valid, it should raise an error
    ### Functions should be committal- if you call a function, that means that it *should* be valid in that spot
    ### Some Exceptions; For example EndStmt is non-comittal
    ### FUNCTION NAMES ARE PART OF THE USER DEBUG INFO

    def StmtList(self) -> bool:
        while self.file.peek().token != 'EOF':
            if not self.Stmt():
                self.RaiseError('Failed to parse statement')
                return False
        self.file.pop()  # For Completeness sake
        return True

    def Stmt(self) -> bool:
        # Anything with a single equals sign: x = 5, const const x = 6
        if self.wanted_indent:
            self.file.peek(ignore_space=False)
            indent_check = self.Check_Indent_Stmt()
            if not indent_check:
                return indent_check
        if self.file.peek().token in ['CONST', 'VAR']:
            return self.Varable_Declaration_Stmt()
        if self.file.peek().token == "IDENTIFIER" and self.file.peek_n(2)[1].token in ["INC", "DEC"]:
            return self.Variable_Increase_Stmt()

        # Control Flow if ( ... ) { ... } else { ... }

        # Class declarations class x { ... }, className x { ... }

        # Function declarations: fn(x) => { ... }
        if self.file.peek().token == "FUNCTION":
            self.file.pop()
            return self.Function_Declaration_Stmt()

        # Floating expressions: print(x), x, x == 5
        return False

    # Non-Comittal
    def EndStmt(self) -> tuple[bool, int]:
        i = 0
        end = False
        while self.file.peek().token in '!?':  # Allow any mix of ! and ?
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

    # Indent checks
    def Check_Indent_Stmt(self) -> bool:
        if self.file.peek().token == "}":
            del self.wanted_indent[len(self.wanted_indent) - 1]
            self.file.pop()
            self.EndStmt()
            return True

        while self.file.peek(ignore_space=False).token == "INDENT":
            self.file.pop(ignore_space=False)
        if self.file.peek(ignore_space=False).token == "SPACE":
            self.RaiseError(
                "Good try with the indentation but I think you did something wrong since it isn't a multiple of three.")
            return False
        return True

    # Declaration of a variable
    def Varable_Declaration_Stmt(self) -> bool:
        # Declaration
        allow_reassign = self.file.pop().token == 'VAR'

        if self.file.peek().token not in ['CONST', 'VAR']:
            self.RaiseError('Double or nothing; Need two const/var keywords to declare variable')
            return False

        allow_edit = self.file.pop().token == 'VAR'

        # not sure about this check because we get here if var and const are at the beginning of the line

        if self.file.peek().token != 'IDENTIFIER':
            self.RaiseError('Identify yourself NOW; Declaration requires variable to declare')
            return False

        # Nothing in native JS allows you to prevent edits, so we only worry about reassignments here
        # Bad reassignments will be caught by JS
        if allow_reassign:
            keyword = 'let'
        else:
            keyword = 'const'  # javascript consts are cringe

        # We will handle bad edits in compile time

        var_name = self.file.pop().lexeme

        lifetime = None

        # lifetime detected
        if self.file.peek().token == "<":
            # remove opening lifetime identifier
            self.file.pop()

            # Lifetime can either be an INT, or an INT followed by and IDENTIFIER (the only valid identifier
            # after INT is 's')
            # Alternatively, it can be INFINITY, which turns the variable into an environment variable
            # With no specified lifetime, the variable will kill itself whenever normal variables would

            # If the lifetime is an INT, the variable lasts for that amount of lines
            # If the lifetime is an INT followed by s, the variable lasts for that amount of seconds (or until
            # the program dies)
            # If the lifetime is INFINITY, it is a environment variable

            # To get the value of the Expr we allow it to dump to the JS, and remove it afterward to process it properly
            rollback_idx = len(self.js)
            if not self.Expr():
                self.RaiseError('Lifetime must be an Expression')
                return False

            lifetime = self.js[rollback_idx:]  # INFINITY or Expression
            self.js = self.js[:rollback_idx]

            extracted_token = self.file.pop().lexeme
            # this can be improved by using valid lifetime characters
            while extracted_token not in [">", os.linesep]:
                lifetime += str(extracted_token)
                extracted_token = self.file.pop().lexeme
            if extracted_token != ">":
                self.RaiseError("CLOSE YOUR LIFETIME DEFINITION")

        if self.file.peek().token != '=':
            self.RaiseError('PUT AN EQUALS SIGN IN YOUR DECLARATION')
            return False
        self.file.pop()
        # pop the value (this is temporary)
        self.file.pop()
        self.js += f'assign(\"{var_name}\", '
        if self.Expr():  # inserts expression
            success, priority = self.EndStmt()
            if not success:
                self.RaiseError('Declaration statement didn\'t end when it should\'ve')
            if self.var_dict.get(var_name) is None:
                self.var_dict[var_name] = []
            self.var_dict[var_name].append(VarState(allow_reassign, allow_edit, priority))

            self.js += f', {keyword == "let"}, {priority}, {lifetime})'
        else:
            self.RaiseError('Failed to parse expression in declaration')
            return False
        return True

    def Function_Declaration_Stmt(self) -> bool:
        if self.file.peek().token != "IDENTIFIER":
            self.RaiseError(
                f'Something isn\'t right here after the function keyword there should be an identifier but I got a {self.file.peek().token}')
            return False

        function_name = self.file.pop()

        if not self.file.pop().token == "(":
            self.RaiseError("I think you tried to define a function but you forgot the parenthesis for the parameters")
            return False
        parameters = []
        while self.file.peek().token != ")":
            param = self.file.pop()
            if param.token == "IDENTIFIER":
                parameters.append(param)
            else:
                self.RaiseError(f"I was expecting a parameter but {param.lexeme} doesn't look like a valid IDENTIFIER")
        # consume the closing parenthesis
        self.file.pop()
        if self.file.pop().token != "ARROW":
            self.RaiseError(f'You say that you want a function and you give me the parenthesis but where is the "=>" ?')
            return False
        # At this point there is either a { for a multi-line function or a single line function without {
        if self.file.peek().lexeme == "{":
            self.file.pop()
            if self.file.peek().token != "NEWLINE":
                self.RaiseError(f'I see that you are writing more stuff after the {"{"}, if it is a single line then '
                                f'you don\'t need the {"{"} if there are multiple lines then you should send this other'
                                f' stuff to the new line')
                return False
            # from now until a } appears we should check that the code is indented
            self.new_indent("function")
            # consume exclamation marks or new_line
            self.file.pop()
        else:
            # it should be handled by the other functions
            pass
        return True

    def Variable_Increase_Stmt(self) -> bool:
        var_name = self.file.pop().lexeme
        operation = self.file.pop().lexeme
        self.js += f'{var_name}{operation}'
        success, _ = self.EndStmt()
        if not success:
            self.RaiseError('Declaration statement didn\'t end when it should\'ve')
            return False
        return True

    def Expr(self) -> bool:
        return True


def transpile(file_path: str) -> str:
    try:
        # TODO: Replace with DreamBerd 3const server
        response = requests.head("http://www.google.com", timeout=5)
        if response.status_code != 200:
            print(
                "-Meta: NetworkError: DreamBerd 3const services are down, or you do not have an internet connection. Please rectify either as soon as possible.")
            exit(1)
    except requests.ConnectionError:
        print(
            "-Meta: NetworkError: DreamBerd 3const services are down, or you do not have an internet connection. Please rectify either as soon as possible. ")
        exit(1)

    tokens = tuple(Tokenizer().tokenize_file(file_path))

    if catch_tokenizer_errors(tokens):
        print('\n')
        print("Tokenizer reports L code, fix your code or I won't compile this garbage")
        exit(1)

    parser = Parser(tokens)
    if parser.parse():
        # If succeeded parsing
        return parser.get_javascript()
    raise RuntimeError("Somehow token error was not caught")


def transpile_and_save(read_file_path: str, write_file_path: str | None = None) -> None:
    if write_file_path is None:
        directory, filename = os.path.split(read_file_path)
        head, _ = filename.rsplit(".", 1)
        write_file_path = os.path.join(directory, f'{head}.js')
    javascript = transpile(read_file_path)
    with open(write_file_path, "w", encoding="utf-8") as write_file:
        write_file.write(javascript)


if __name__ == '__main__':
    transpile_and_save(os.path.join('test', 'db', 'db', 'functions.db'))

