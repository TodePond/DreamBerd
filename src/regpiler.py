import os
import re
import requests
from typing import Sequence
from compinterpret import Tokenizer, SimpleStringCrawler

reference_tokenizer = Tokenizer()

# https://qph.cf2.quoracdn.net/main-qimg-8d58857bb87f14c8e1ce2f6686ef3e04
operator_precedence = {
    '(': 15,
    ')': 15,
    '.': 15,
    '++': 14,
    '--': 14,
    ';': 14,
    '**': 13,
    '*': 12,
    '/': 12,
    '\\': 12,
    '%': 12,
    '+': 11,
    '-': 11,
    '<<': 10, # WHY DOES JAVASCRIPT HAVE THESE?
    '>>': 10,
    '>>>': 10,
    '<=': 9,
    '<': 9,
    '>': 9,
    '>=': 9,
    '==': 8,
    '===': 8,
    '====': 8,
    '&': 7,
    '^': 6,
    '|': 5,
    '&&': 4,
    '||': 3,
}

class RawToken:
    __slots__ = ("token", "lexeme", "priority")
    def __init__(self, token: str, lexeme: str, priority: int = 0) -> None:
        self.token = token
        self.lexeme = lexeme
        self.priority = priority

    def __repr__(self) -> str:
        return f'{self.token}({repr(self.lexeme)})'

    def __str__(self) -> str:
        return f'{self.token}({repr(self.lexeme)})'
    
    def compare(self, other: "RawToken") -> int:
        #presume both are operators
        if self.priority < other.priority:
            return 1
        elif self.priority > other.priority:
            return -1
        else:
            if operator_precedence[self.lexeme] > operator_precedence[other.lexeme]:
                return 1
            elif operator_precedence[self.lexeme] < operator_precedence[other.lexeme]:
                return -1
            else:
                return 0

class RawTokenCrawler:
    def __init__(self, raw: Sequence[RawToken]) -> None:
        self.raw = raw
        self.cursor = 0

    def pop(self) -> RawToken | None:
        if self.cursor == len(self.raw):
            return None
        self.cursor += 1
        return self.raw[self.cursor - 1]

    def back(self, count: int = 1) -> None:
        self.cursor -= count

    def peek(self) -> RawToken | None:
        if self.cursor == len(self.raw) - 1:
            return None        
        return self.raw[self.cursor]

def split_raw_file(path: str) -> list[str] | list[tuple[str, str]]:
    with open(path, 'r', encoding="utf-8") as file:
        content = file.read()

    # Split the file content using the regex pattern
    split_content = re.split(r'={5,} *([^= ]*) *=+', content)

    # Get the capture groups from the regex pattern
    capture_groups = re.findall(r'={5,} *([^= ]*) *=+', content)

    if len(split_content) == 1:
        return split_content
    else:
        result = [(split_content[i], capture_groups[i]) for i in range(len(split_content))]

        return result

def preprocess_line(line: str) -> str:
    processed_line = line
    # Convert ++ to += 1 and -- to -= 1
    processed_line = re.sub(r'^([^ +\\\-*\/<>=()\[\]!;:.{}\n]+)(\+|-)\2$', r'\1 \2= 1', processed_line)

    return processed_line

def process_expr(expr: str) -> str:
    expr_split = expr.split('{')[-1].split('}')[0]
    if expr_split == '':
        return expr # Wasn't an expression
    else:
        expr = expr_split
    
    tokens: list[RawToken] = []
    crawler = SimpleStringCrawler(expr.strip().replace('×', '*').replace('÷', '/').replace('^', '**'))

    # 0 = Identifier / Number (same thing)
    # 1 = Parenthetical
    # 2 = Operator (anything else)
    # 3 = Redirect

    state = 3
    
    if crawler.peek() in '+\\-*/<>%=)]!;:.{}':
        raise ValueError('Who starts an Expression like that? I just got here!')

    while crawler.peek() != '':
        match state:
            case 0:
                # Remove leading spaces
                while crawler.peek() in ' \n\r\t':                    
                    crawler.pop()
                    if crawler.peek() == '':
                        break
                if crawler.peek() == '':
                    break
                identifier = ''
                while crawler.peek() not in '+\\-*/<>%=()[]!;&:{} \n\r\t':
                    identifier += crawler.pop()
                tokens.append(RawToken('IDENTIFIER', identifier))
                state = 3
            case 1:
                # Deprecated
                pass
            case 2:
                spaces = 0
                operator = ''
                trail = 0
                while crawler.peek() in '+\\-*/<>%=&()[] \t':
                    if crawler.peek() in ' \t':
                        # Indents are 3 space
                        spaces += 1 if crawler.pop() == ' ' else 3
                        if operator != '':
                            trail += 1
                    else:
                        # &   & == &&
                        if operator != '' and trail > 0:
                            break
                        if crawler.peek() in ')]}' and operator in '([{' and operator != '':
                            break
                        operator += crawler.pop()
                    if crawler.peek() == '':
                        break                
                tokens.append(RawToken('OPERATION', operator, spaces))
                crawler.back(trail)
                if crawler.peek() == '':
                    break
                state = 3
            case 3:        
                if crawler.peek() == '':
                    # Valid spot to stop
                    # We also have to stop
                    break
                # if crawler.peek() in '([':
                #     state = 1
                #     continue
                if crawler.peek(ignore_space=True) in '+\\-*/<>%=& \t([])':
                    state = 2
                    continue
                elif crawler.peek(ignore_space=True) in '\n\r{}:':
                    raise ValueError('Malformed Expression')
                else:
                    state = 0
                    continue
                    
    postfix_tokens = []
    operator_stack: list[RawToken] = []
    
    for token in tokens:        
        if token.token == 'OPERATION':
            if ')' in token.lexeme:
                while '(' not in operator_stack[-1].lexeme:
                    postfix_tokens.append(operator_stack.pop())
                operator_stack.pop() # Remove extra parentheses
            elif '(' in token.lexeme:
                operator_stack.append(token)
            elif len(operator_stack) == 0 or '(' in operator_stack[-1].lexeme or token.compare(operator_stack[-1]) == 1:
                operator_stack.append(token)
            else:
                while len(operator_stack) > 0 and token.compare(operator_stack[-1]) <= 0:
                    postfix_tokens.append(operator_stack.pop())
                operator_stack.append(token)
        else: # IDENTIFIER        
            postfix_tokens.append(token)

    while len(operator_stack) > 0:
        postfix_tokens.append(operator_stack.pop())
    
    reconstructed: list[RawToken] = []

    def varify(identifier: str) -> str:
        if re.match(r'^[0-9]+(?:\.[0-9]+)?', identifier):
            return identifier
        elif re.match(r'^\".*\"$', identifier):
            # String object
            # This is so stupid
            return f"\\\"{identifier}\\\""
        else:
            return f'\"{identifier}\"'

    for token in postfix_tokens:
        if token.token == 'OPERATION':
            op1 = reconstructed.pop()
            op2 = reconstructed.pop()

            if token.lexeme == '====':
                # We do a little compile-time evaluation
                if op2.lexeme == op1.lexeme:                    
                    reconstructed.append(RawToken('SYSTEM', 'true'))
                else:                              
                    reconstructed.append(RawToken('SYSTEM', 'false'))
            else:
                reconstructed.append(RawToken('SYSTEM', f'current_scope.get_var(current_scope.get_var({varify(op2.lexeme)}){token.lexeme.strip()}current_scope.get_var({varify(op1.lexeme)}))'))
        else:
            reconstructed.append(token)

    out_str = ""

    # This being a loop is only really a formality because it should always parse to a single token
    for token in reconstructed:
        out_str += token.lexeme
    
    return out_str
    
def preprocess_subfile(subfile: str) -> str:
    # Remove comments
    subfile = re.sub(r'//[^\n\r]*', '', subfile)

    # Convert all functions to common syntax
    subfile = re.sub(r'=> *([^\s{}][^\n\r!?{}]+)([!?]*)', r'=> {return \1}', subfile)
    subfile = re.sub(r'([^ +\\\-*\/<>=()\[\]!;:.{}\n,]+) =>', r'(\1) =>', subfile)
    subfile = re.sub(r'[functio]u?n?c?t?i?o?n? +\(([^ +\\\-*\/<>=()\[\]!;:.{}\n,]+(?:, *[^ +\\\-*\/<>=()\[\]!;:.{}\n,]+)*)?\) *(?:=>)?', r'(\1) =>', subfile)
    subfile = re.sub(r'[functio]u?n?c?t?i?o?n? +([^ +\\\-*\/<>=()\[\]!;:.{}\n,]+)\(([^ +\\\-*\/<>=()\[\]!;:.{}\n,]+(?:, *[^ +\\\-*\/<>=()\[\]!;:.{}\n,]+)*)?\) *(?:=>)?', r'const const \1 = (\2) =>', subfile)

    # Regularize how code blocks are formatted for easier parsing
    subfile = re.sub(r'[\n\r]*{', r'{\n', subfile, re.DOTALL)
    subfile = subfile.replace('}', '\n}')

    return subfile

def transpile_subfile(subfile: str) -> str:
    subfile = preprocess_subfile(subfile)
    # Split the file content using the regex pattern
    split_content = re.split(r'(!+|\n|\?)', subfile)

    # Get the capture groups from the regex pattern
    capture_groups = re.findall(r'(!+|\n|\?)', subfile)

    result = ""

    futures: dict[int, list[str]] = {}
    offset = 0
    for i in range(len(split_content)):
        if split_content[i] in '!?\n':
            offset -= 1
            continue

        if i+offset in futures:
            result += '\n'.join(futures[i+offset]) + '\n'
            futures[i] = []

        if split_content[i].strip() == '':
            continue

        result += f'// DB_DEBUG: {split_content[i]}{capture_groups[i + offset]}\n'
        line, new_futures = transpile_line(preprocess_line(split_content[i]), len(capture_groups[i + offset]),
                                           '?' in capture_groups[i + offset], i)

        result += line + '\n'

        result += 'WHEN_BLOCK_MANAGER.checkConditions(); // Check all pending when statements in case the above line changed something\n'

        for k, v in new_futures.items():
            if k not in futures:
                futures[k] = v
            else:
                futures[k].extend(v)

    return result

def check_indentation(match: re.Match[str], line: str) -> str:
    indentation = match.group("indentation") if match.group("indentation") else ""
    if indentation and len(indentation) % 3 != 0:
        raise ValueError("What a strange indentation scheme that you use, this could confuse someone! Please use the"
                            "officially recognized 3 space indentation system, thank you. Error occurred in\n" + line)
    return indentation

def transpile_line(line: str, priority: int, debug: bool, line_num: int) -> tuple[str, dict[int, list[str]]]:
    futures = {}

    # Assignment
    if match := re.match(
            # With named groups is possible to have "optional" groups and the regex is still cursed.
            # I know that re.IGNORECASE is a thing but without it the regex looks more cursed.
            r'^(?P<indentation> +)?(?:(?P<third_const>[Cc][Oo][Nn][Ss][Tt]) +(?=[Cc][Oo][Nn][Ss][Tt] +[Cc][Oo][Nn][Ss][Tt]))?(?P<invalid_mix>^[Cc][Oo][Nn][Ss][Tt] +(?= *([Vv][Aa][Rr]|[Cc][Oo][Nn][Ss][Tt]) +(?=[Vv][Aa][Rr]|[Cc][Oo][Nn][Ss][Tt])))?(?P<first_const>[Cc][Oo][Nn][Ss][Tt]|[Vv][Aa][Rr]) +(?P<second_const>[Cc][Oo][Nn][Ss][Tt]|[Vv][Aa][Rr]) +(?P<var_name>[^ +\\\-*\/<>=()\[\]!;:.{}\n]+)(?:<(?P<lifetime>.*)>)?(?: *: *[A-Za-z]+)? *(?P<assignment_operator>[+\-\/*]?)= *(?P<value>[^!\n?]+)',
            line
    ):
        if match.group("invalid_mix"):
            raise ValueError("You thought that having const or var three times without having all of them being const "
                             "was a good idea? Well it isn't so fix it")

        indentation = check_indentation(match, line) #Convenience function because this is checked a lot    

        allow_reassignment = match.group("first_const").lower() == 'var'
        lifetime: str | int = -1
        if match.group("lifetime") is not None:
            lifetime_match = match.group("lifetime")
            if lifetime_match[-1] != 's' and lifetime_match.lower() != 'infinity':
                futures[int(lifetime_match)+line_num] = [f'variables.get({lifetime_match})!.kill();']
            elif lifetime_match[-1] == 's':
                lifetime = int(lifetime_match[:-1])
            else:
                lifetime = 'infinity'

        if match.group("third_const"):
            # TODO implement const const const
            pass

        value = match.group("value")
        if match.group("assignment_operator"):
            value = f'{match.group("var_name")} {match.group("assignment_operator")} {match.group("value")}'

        name = match.group("var_name")
        if not re.match('[0-9]*.?[0-9]+', name):
            # Not a number
            name = f"\"{name}\""
        return f'{indentation}current_scope.assign({name}, {process_expr(value)}, {str(allow_reassignment).lower()}, {priority}, {lifetime});', futures
    
    # Reassignment
    elif match := re.match(
            r'^(?P<indentation> +)?(?P<prevs>(?:previous +)+)?(?P<variable>[^ +\\\-*\/<>=()\[\]!;:.{}\n]+) *(?P<assignment_operator>[+\-\/*]?)= *(?P<value>[^!\n?]+)',
            line,
            re.IGNORECASE
    ):
        indentation = check_indentation(match, line) #Convenience function because this is checked a lot    

        if match.group('assignment_operator'):
            value = f'{match.group("variable")} {match.group("assignment_operator")} ({match.group("value")})'
        else:
            value = match.group('value')

        if match.group('prevs'):
            # TODO: Time travel
            pass
        else:

            name = match.group("variable")
            if not re.match('[0-9]*.?[0-9]+', name):
                # Not a number
                name = f"\"{name}\""

            return f'{indentation}current_scope.assign({name}, {process_expr(value)}, undefined, {priority})', futures

    # single line function, in the case of the multi-line one code is "{"
    elif match := re.match(
            r'(?= *[functio])((?P<indentation> +)?(?P<function>f?u?n?c?t?i?o?n?) )+(?P<name>.+?) *(?P<parameters>\(.*?\)) +=> +(?P<code>.+)',
            line,
            re.IGNORECASE
    ):
        func_keyword = match.group("function")
        func_name = match.group("name")
        parameters = match.group("parameters")
        # code syntax should be checked
        code = match.group("code")
        line = line.replace(func_keyword, "function").replace("=>", "")
        return line, futures

    # replace the previous keyword with the function call (not sure if this is right)
    line = re.sub(r'previous +(?!=[()]*)([^?! ]*)', r'current_scope.get_var("\1").previous()', line, 1, re.IGNORECASE)

    # Only here for debugging, when completed this should return an error if execution reaches the end
    return f"{line} // TODO", futures


def regpile() -> None:
    try:
        # TODO: Replace with DreamBerd 3const server
        response = requests.head("http://www.google.com", timeout=5)
        if response.status_code != 200:
            print(
                "-Meta: NetworkError: DreamBerd 3const services are down, or you do not have an internet connection. "
                "Please rectify either as soon as possible.")
            exit(1)
    except requests.ConnectionError:
        print(
            "-Meta: NetworkError: DreamBerd 3const services are down, or you do not have an internet connection. "
            "Please rectify either as soon as possible. ")
        exit(1)

    files = split_raw_file(os.path.join('test', 'db', 'db', 'functions.db'))

    if not os.path.isdir('built'):
        os.mkdir('built')

    for file in files:
        result = ""
        if isinstance(file, str):
            result = transpile_subfile(file)
        else:
            result = transpile_subfile(file[0])

        filename = str(len(os.listdir('built'))) + '.tsx' if isinstance(file, str) else file[1]

        with open(f'src{os.sep}template.tsx', 'r', encoding="utf-8") as reader:
            template = reader.read()
            result = template.replace('// USER CODE HERE //', result)

        with open(os.path.join('built', filename), 'w', encoding="utf-8") as writer:
            writer.write(result)


if __name__ == '__main__':
    regpile()
