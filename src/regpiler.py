import os
import re

import requests

from compinterpret import Tokenizer

reference_tokenizer = Tokenizer()

def split_raw_file(path):
    with open(path, 'r') as file:
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

def preprocess_line(line):
    if match := re.match(r'(?P<var_name>[^ +\\\-*\/<>=()\[\]!;:.{}\n]+)(?P<operator>\+\+|--)',
                         line):
        return f"{match.group('var_name')} {match.group('operator')[0]}= 1"
    return line

def process_expr(expr):
    new_expr = re.sub(r'([^ +\\\-*\/<>=()\[\]!;:.{}\n0-9]+)', r'"\1"', expr)
    new_expr = re.sub(r'([^ +\\\-*\/<>=()\[\]!;:.{}\n]+)', r'get_var(\1)', new_expr)
    return new_expr

def transpile_subfile(subfile):
    # Split the file content using the regex pattern
    split_content = re.split(r'(!+|\n|\?)', subfile)

    # Get the capture groups from the regex pattern
    capture_groups = re.findall(r'(!+|\n|\?)', subfile)

    result = ""

    futures = {}
    offset = 0
    for i in range(len(split_content)):
        if split_content[i] in '!?\n':
            offset -= 1
            continue

        if i in futures:
            result += '\n'.join(futures[i]) + '\n'
            futures[i] = []

        result += f'// DB_DEBUG: {split_content[i]}{capture_groups[i + offset]}\n'
        line, new_futures = transpile_line(preprocess_line(split_content[i]), len(capture_groups[i + offset]),
                                           '?' in capture_groups[i + offset], i)

        result += line + '\n'

        for k, v in new_futures:
            if k in futures:
                futures[k] = v
            else:
                futures[k].extend(v)

    return result

def check_indentation(match, line):
    indentation = match.group("indentation") if match.group("indentation") else ""
    if indentation and len(indentation) % 3 != 0:
        raise ValueError("What a strange indentation scheme that you use, this could confuse someone! Please use the"
                            "officially recognized 3 space indentation system, thank you. Error occurred in\n" + line)
    return indentation

def transpile_line(line: str, priority: int, debug: bool, line_num: int):
    futures = {}

    # Assignment
    if match := re.match(
            # With named groups is possible to have "optional" groups and the regex is still cursed.
            # I know that re.IGNORECASE is a thing but without it the regex looks more cursed.
            r'(?P<indentation> +)?(?:(?P<third_const>[Cc][Oo][Nn][Ss][Tt]) +(?=[Cc][Oo][Nn][Ss][Tt] +[Cc][Oo][Nn][Ss][Tt]))?(?P<invalid_mix>^[Cc][Oo][Nn][Ss][Tt] +(?= +[Vv][Aa][Rr] +(?=[Vv][Aa][Rr]|[Cc][Oo][Nn][Ss][Tt])))?(?P<first_const>[Cc][Oo][Nn][Ss][Tt]|[Vv][Aa][Rr]) +(?P<second_const>[Cc][Oo][Nn][Ss][Tt]|[Vv][Aa][Rr]) +(?P<var_name>[^ +\\\-*\/<>=()\[\]!;:.{}\n]+)(?:<(?P<lifetime>.*)>)? *(?P<assignment_operator>[+\-\/*]?)= *(?P<value>[^!\n?]+)',
            line
    ):
        if match.group("invalid_mix"):
            raise ValueError("You thought that having const or var three times without having all of them being const "
                             "was a good idea? Well it isn't so fix it")

        indentation = check_indentation(match, line) #Convenience function because this is checked a lot    

        allow_reassignment = match.group("first_const").lower() == 'var'
        lifetime = -1
        if match.group("lifetime") is not None:
            lifetime_match = match.group("lifetime")
            if lifetime_match[-1] != 's' and lifetime_match.lower() != 'infinity':
                futures[int(lifetime_match)] = [f'{lifetime_match}.kill();']
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
        return f'{indentation}assign("{match.group("var_name")}", {process_expr(value)}, {str(allow_reassignment).lower()}, {priority}, {lifetime});', futures
    
    # Reassignment
    elif match := re.match(
            r'(?P<indentation> +)?(?P<prevs>(?:previous +)+)?(?P<variable>[^ +\\\-*\/<>=()\[\]!;:.{}\n]+) *(?P<assignment_operator>[+\-\/*]?)= *(?P<value>[^!\n?]+)',
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
            return f'{indentation}assign(\"{match.group("variable")}\", {process_expr(value)}, undefined, {priority})', futures

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
    line = re.sub(r'previous +(?!=[()]*)([^?! ]*)', r'get_var("\1").previous()', line, 1, re.IGNORECASE)

    # Only here for debugging, when completed this should return an error if execution reaches the end
    return line, futures


if __name__ == '__main__':
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

    files = split_raw_file(f'test{os.sep}db{os.sep}db{os.sep}time_recursion.db')

    if not os.path.isdir('built'):
        os.mkdir('built')

    for file in files:
        result = ""
        if isinstance(file, str):
            result = transpile_subfile(file)
        else:
            result = transpile_subfile(file[0])

        filename = str(len(os.listdir('built'))) + '.tsx' if isinstance(file, str) else file[1]

        with open(f'src{os.sep}template.tsx', 'r') as reader:
            template = reader.read()
            result = template.replace('// USER CODE HERE //', result)

        with open(os.path.join('built', filename), 'w') as writer:
            writer.write(result)
