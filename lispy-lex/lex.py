from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def lex(code):
    keywords = {
        "if",
        "=>",
        "and",
        "begin",
        "case",
        "cond",
        "define",
        "delay",
        "do",
        "else",
        "lambda",
        "let",
        "let*",
        "letrec",
        "or",
        "quasiquote",
        "quote",
        "set!",
        "unquote",
        "unquote-splicing",
    }
    token_specification = [
        ("COMMENT", r";.*"),
        ("STRING", r'"([^"\\\n\r\b\f]+|\\["\\\/bfnrt])*"'),
        ("NUMBER", r"[\+\-]?\d+(\.\d*)?"),  # Integer or decimal number
        ("CHAR", r"#\\\w+"),
        ("BOOL", r"#(t|f)"),
        ("NEWLINE", r"\n"),  # Line endings
        ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
        (
            "NAME",
            r"[a-zA-Z_\-/<=>!?:$%&~^'.+*][a-zA-Z_0-9\-/<=>!?:$%&~^'.+*]*",
        ),  # Variable or function names
        ("LPAR", r"\("),  # Identificador para abrir parênteses
        ("RPAR", r"\)"),  # Identificador para fechar parênteses
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == "ID" and value in keywords:
            kind = value
        elif kind == "NEWLINE":
            line_start = mo.end()
            line_num += 1
            continue
        elif kind in("SKIP","COMMENT"):
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"{value!r} unexpected on line {line_num}")
        yield Token(kind, value, line_num, column)
