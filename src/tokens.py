__author__ = 'iravid'

from ply import lex
from ply.lex import TOKEN

reserved_words = {
    "code": "CODE",
    "const": "CONST",
    "define": "DEFINE",
    "do": "DO",
    "float": "FLOAT",
    "from": "FROM",
    "if": "IF",
    "int": "INT",
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

reserved_symbols = (
    "LPAREN", "RPAREN",
    "LCURLPAREN", "RCURLPAREN",
    "COMMA",
    "COLON",
    "SEMICOLON",
    "EXCLAMATION",
    "PLUS", "MINUS",
    "MULT", "DIV",
    "EQ", "NEQ", "LT", "LTE", "GT", "GTE"
    "ASSIGN"
)

composed_tokens = (
    "ID",
    "NUMBER"
)

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

# Comment handling

# Multiline comments are allowed, so define a state that the lexer will be switched into when '/*' is encountered
states = (
    "COMMENT", "exclusive"
)

# Comment start encountered - push COMMENT onto the state stack
def t_start_comment(t):
    r"/\*"
    t.lexer.push_state("COMMENT")

# Ignore all contents within comment
t_COMMENT_contents = r".*"

# Comment end encountered - pop state
def t_end_comment(t):
    r"\*/"
    t.lexer.pop_state()
