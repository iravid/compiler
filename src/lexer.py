__author__ = 'iravid'

import lex

import logging
logger = logging.getLogger("compile")

reserved_words = {
    "code": "CODE",
    "const": "CONST",
    "define": "DEFINE",
    "do": "DO",
    "float": "FLOATDECL",
    "from": "FROM",
    "if": "IF",
    "int": "INTDECL",
    "ival": "IVAL",
    "otherwise": "OTHERWISE",
    "read": "READ",
    "rval": "RVAL",
    "then": "THEN",
    "to": "TO",
    "when": "WHEN",
    "while": "WHILE",
    "write": "WRITE",
    "and": "AND",
    "or": "OR"
}

reserved_symbols = [
    "LPAREN", "RPAREN",
    "LCURLPAREN", "RCURLPAREN",
    "COMMA",
    "COLON",
    "SEMICOLON",
    "EXCLAMATION",
    "PLUS", "MINUS",
    "MULT", "DIV",
    "EQ", "NEQ", "LT", "LTE", "GT", "GTE",
    "ASSIGN", "CONSTASSIGN"
]

composed_tokens = [
    "ID",
    "INTEGER",
    "FLOAT"
]

tokens = reserved_symbols + reserved_words.values() + composed_tokens

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LCURLPAREN = r"\{"
t_RCURLPAREN = r"\}"

t_COMMA = r","
t_COLON = r":"
t_SEMICOLON = r";"
t_EXCLAMATION = r"!"

t_PLUS = r"\+"
t_MINUS = r"-"
t_MULT = r"\*"
t_DIV = r"/"

t_EQ = r"=="
t_NEQ = r"!="

t_LT = r"<"
t_LTE = r"<="
t_GT = r">"
t_GTE = r">="

t_ASSIGN = r":="
t_CONSTASSIGN = r"="

def t_ID(t):
    r"[a-zA-Z]([a-zA-Z]|[0-9])*"

    # Check if we found a reserved word
    t.type = reserved_words.get(t.value, "ID")

    return t

def t_FLOAT(t):
    r"[0-9]+\.[0-9]*"
    t.value = float(t.value)

    return t

def t_INTEGER(t):
    r"[0-9]+"
    t.value = int(t.value)

    return t

# Ignore whitespace
t_ignore = " \t"

# Multiline-handling comment rule
def t_COMMENT(t):
    r'//[^\n]*\n|/[*](.|\n)*?[*]/'
    t.lexer.lineno += t.value.count('\n')

def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    logging.warning("Line %d: Skipping unexpected character '%s'", t.lexer.lineno, t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()