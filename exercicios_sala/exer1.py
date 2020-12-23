# Exercício: Crie um analisador léxico para uma calculadora que 
# aceite as expressões matemáticas usuais com as quatro operações,
# além de agrupamento utilizando parênteses, atribuição de variáveis
# e chamada de funções.
# 
# Ref: https://docs.python.org/3/library/re.html
from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r'='),           # Assignment operator
        ('COMA',      r','),            # Statement terminator
        ('OP',       r'[+\-*/\^]'),      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ("NAME", r"[a-zA-Z_][a-zA-Z_0-9]*"),  # Variable or function names
        ("ABRIR_PARENTESE", r"\("), # Identificador para abrir parênteses
        ("FECHAR_PARENTESE", r"\)"), # Identificador para fechar parênteses
        ("FAT",r"!"),
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)


exemplos = [
    "42 / 12",
    "(10 + 11) * 2",
    "80 / 2",
    "20 - 1",
    "10 ^ 2",
    "3.14",
    "sqrt(5)",
    "x = 10",
    "sum(1,2)",
    "53! + 4"
]

for ex in exemplos:
    print(ex)
    for tok in tokenize(ex):
        print('    ', tok)
    print()