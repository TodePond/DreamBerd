import re
import requests
import os
from compinterpret import Tokenizer, tokens

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

        line, new_futures = transpile_line(split_content[i], len(capture_groups[i+offset]), '?' in capture_groups[i+offset], i)

        result += line + '\n'

        for k, v in new_futures:
            if k in futures:
                futures[k] = v
            else:
                futures[k].extend(v)
                
    return result

def transpile_line(line: str, priority: int, debug: bool, line_num: int):
    futures = {}

    # Assignment
    if match := re.match(r'([Cc][Oo][Nn][Ss][Tt]|[Vv][Aa][Rr]) +([Cc][Oo][Nn][Ss][Tt]|[Vv][Aa][Rr]) +([^ +\-*\/<>=()\[\]!;:.{}]+)(?:<(.*)>)? *([\+-\/\*]?)= *([^!\n?]+)',
            line):      
        
        var_type = 'let' if match.groups()[0].lower() == 'var' else 'const'       

        lifetime = -1
        if match.groups()[3] != None:
            if match.groups()[3][-1] != 's' and match.groups()[3].lower() != 'infinity':
                futures[int(match.groups()[3])] = [f'{match.groups()[3]}.kill();']
            elif match.groups()[3][-1] == 's':
                lifetime = int(match.groups()[3][:-1])
            else:
                lifetime = 'infinity'

        value = match.groups()[5]
        if match.groups()[4] != None:
            value = f'{match.groups()[2]} {match.groups()[4]} {match.groups()[5]}'

        return f'assign({match.groups()[2]}, {value}, {var_type == "let"}, {priority}, {lifetime});', futures
    
    return line, futures
    

        

if __name__ == '__main__':
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

    files = split_raw_file(f'test{os.sep}db{os.sep}db{os.sep}time_travel.db')

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
