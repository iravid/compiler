__author__ = 'iravid'

import ast
from lexer import tokens

def p_program(p):
    "program : CODE ID LCURLPAREN declarations stmtlist RCURLPAREN"
    p[0] = ast.NProgram(p[2], p[4], p[5])

def p_declarations(p):
    """declarations : DEFINE declarelist
                  | empty"""
    if len(p) == 3:
        p[0] = ast.NDeclareList(filter(lambda d: isinstance(d, ast.NVarDecl), p[2]),
                                filter(lambda d: isinstance(d, ast.NConstDecl), p[2]))
    else:
        p[0] = ast.NDeclareList([], [])

def p_declarelist_varlist(p):
    """declarelist : declarelist type COLON idents SEMICOLON
                   | type COLON idents SEMICOLON"""
    if len(p) == 5:
        p[0] = [ast.NVarDecl(p[1], p[3])]
    elif len(p) == 6:
        p[1].append(ast.NVarDecl(p[2], p[4]))
        p[0] = p[1]

def p_declarelist_constlist(p):
    """declarelist : declarelist ctype ID CONSTASSIGN number SEMICOLON
                   | ctype ID CONSTASSIGN number SEMICOLON"""
    if len(p) == 6:
        p[0] = [ast.NConstDecl(p[1], p[2], p[5])]
    elif len(p) == 7:
        p[1].append(ast.NConstDecl(p[2], p[3], p[6]))
        p[0] = p[1]

def p_number(p):
    """number : INTEGER
              | FLOAT"""
    if type(p[1]) is float:
        p[0] = ast.NFloat(p[1])
    elif type(p[1]) in (int, long):
        p[0] = ast.NInteger(p[1])


def p_idents(p):
    """idents : idents COMMA ID
              | ID"""
    if len(p) == 2:
        p[0] = [ast.NIdentifier(p[1])]
    elif len(p) == 4:
        p[1].append(ast.NIdentifier(p[3]))
        p[0] = p[1]

def p_ctype(p):
    "ctype : CONST type"
    p[0] = p[2]

def p_type(p):
    """type : INTDECL
            | FLOATDECL"""
    p[0] = p[1]

def p_stmt_list(p):
    """stmt_list : stmt_list stmt
                | empty"""
    pass

def p_stmt(p):
    """stmt : assignment_stmt
            | type_conversion_stmt
            | control_stmt
            | read_stmt
            | write_stmt
            | stmt_block"""
    pass

def p_stmt_block(p):
    """stmt_block : LCURLPAREN stmt_list RCURLPAREN"""
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

def p_type_conversion_stmt(p):
    """type_conversion_stmt : ID ASSIGN IVAL LPAREN expression RPAREN SEMICOLON
                            | ID ASSIGN RVAL LPAREN expression RPAREN SEMICOLON"""
    pass

def p_control_stmt(p):
    """control_stmt : IF LPAREN boolexpr RPAREN THEN stmt OTHERWISE stmt
                    | WHILE LPAREN boolexpr RPAREN DO stmt
                    | FROM assignment_stmt TO boolexpr WHEN step DO stmt"""
    pass

def p_step(p):
    """step : ID ASSIGN ID addop number
            | ID ASSIGN ID mulop number"""
    pass

def p_addop(p):
    """addop : PLUS
             | MINUS"""
    pass

def p_mulop(p):
    """mulop : MULT
             | DIV"""
    pass

def p_boolexpr(p):
    """boolexpr : boolexpr OR boolterm
                | boolterm"""
    pass

def p_boolterm(p):
    """boolterm : boolterm AND boolfactor
                | boolfactor"""
    pass

def p_boolfactor(p):
    """boolfactor : EXCLAMATION LPAREN boolfactor RPAREN
                  | expression relop expression"""
    pass

def p_relop(p):
    """relop : EQ
             | NEQ
             | LT
             | LTE
             | GT
             | GTE"""
    pass

def p_expression(p):
    """expression : expression addop term
                  | term"""
    pass

def p_term(p):
    """term : term mulop factor
            | factor"""
    pass

def p_factor(p):
    """factor : LPAREN expression RPAREN
              | ID
              | number"""
    pass