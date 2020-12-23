import re


class Token(str):
    kind : str

    def __new__(cls, value, kind):
        tk = str.__new__(cls, value)
        tk.kind = kind
        return tk

    def __repr__(self):
        value = super().__repr__()
        return f'Token({value}, {self.kind})'


REGEX_MAP = {
    "STRING"  : r'"[^"\n]*"', 
    "NUMBER"  : r'-?\d+(\.\d+)?', 
    "LITERAL" : r'true|false|null',
    "OP"      : r'[{}[\],:]',
    "WS"      : r'\s+',
    "ERROR"   : r'.',
}

REGEX = re.compile('|'.join(
    f'(?P<{k}>{v})' for k, v in REGEX_MAP.items()
))


def lex(src) -> list:
    tokens = []
    for m in REGEX.finditer(src):
        kind = m.lastgroup
        value = src[m.start():m.end()]
        tk = Token(value, kind)
        if kind == 'WS':
            continue
        elif kind == 'ERROR':
            raise SyntaxError(r'bad token: {tk}')
        else:
            tokens.append(tk)
    
    return tokens

def peek(tokens):
    return tokens[0]

def read(tokens):
    return tokens.pop(0)

def expect(value, tokens):
    tk = peek(tokens)
    if tk != value:
        raise SyntaxError(r'bad token: {tk}')
    return read(tokens)
    
def parse(src):
    tokens = lex(src)
    return start(tokens)

def start(tokens):
    """
    start  : object | array
    """
    if peek(tokens) == '{':
        return object(tokens)
    else:
        return array(tokens) 

def object(tokens):
    """
    object : "{" [pair ("," pair)*] "}"
    """
    expect("{", tokens)
    
    if peek(tokens) == "}":
        expect("}", tokens)
        return []

    pairs = [pair(tokens)]
    
    tk = read(tokens)
    while tk == ',':
        pairs.append(pair(tokens))
        tk = read(tokens)
    if tk != "}":
        raise SyntaxError(f'bad token: {tk}')
    
    return dict(pairs)

def array(tokens):
    """
    array  : "[" [value ("," value)*] "]"
    """
    expect("[", tokens)
    
    if peek(tokens) == "]":
        expect("]", tokens)
        return []

    values = [value(tokens)]
    
    tk = read(tokens)
    while tk == ',':
        values.append(value(tokens))
        tk = read(tokens)
    if tk != "]":
        raise SyntaxError(f'bad token: {tk}')
    
    return values

def pair(tokens):
    """
    pair   : STRING ":" value
    """
    tk = read(tokens)
    if tk.kind != "STRING":
        raise SyntaxError(f'bad token: {tk}')
    left = 
    expect(":", tokens)
    right = value(tokens) 

    return (left, right)

def value(tokens):
    """
    value  : object
           | array 
           | STRING
           | NUMBER
           | LITERAL
    """
    tk = peek(tokens)
    if tk == "{":
        return object(tokens)
    elif tk == "[":
        return array(tokens)
    
    tk = read(tokens)
    if tk.kind == "STRING":
        return 
    elif tk.kind == "NUMBER":
        return float(tk)
    elif tk == "true":
        return True
    elif tk == "false":
        return False
    elif tk == "null":
        return None


src = r"""
{
    "name": "Fábio",
    "age": 38,
    "langs": ["Python", "Js", "C"],
    "data": [
        [true, false, null],
        {"data": {}},
        [[]]
    ]
}
"""
print(parse(src))

