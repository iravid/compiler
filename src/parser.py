__author__ = 'iravid'

from lexer import tokens

def p_program(p):
    "program : CODE ID LCURLPAREN declarations stmtlist RCURLPAREN"
    pass

def p_declarations(p):
    """declarations : DEFINE declarelist
                  | empty"""
    pass

def p_declarelist(p):
    """declarelist : declarelist type COLON idents
                    | type COLON idents
                    | declarelist ctype ID CONSTASSIGN INTEGER SEMICOLON
                    | declarelist ctype ID CONSTASSIGN FLOAT SEMICOLON
                    | ctype ID CONSTASSIGN INTEGER SEMICOLON
                    | ctype ID CONSTASSIGN FLOAT SEMICOLON"""
    pass

def p_idents(p):
    """idents : ID COMMA idents
              | ID SEMICOLON"""
    pass

def p_ctype(p):
    "ctype : CONST type"

def p_type(p):
    """type : INTDECL
            | FLOATDECL"""
    pass

def p_stmtlist(p):
    """stmtlist : stmtlist stmt
                | empty"""
    pass

def p_stmt(p):
    """stmt : assignment_stmt
            | val
            | control_stmt
            | read_stmt
            | write_stmt
            | stmt_block"""
    pass

def p_write_stmt(p):
    "write_stmt : WRITE LPAREN expression RPAREN SEMICOLON"
    pass

def p_read_stmt(p):
    "read_stmt : READ LPAREN ID RPAREN SEMICOLON"
    pass

def p_assignment_stmt(p):
    "assignment_stmt : ID ASSIGN expression SEMICOLON"
    pass