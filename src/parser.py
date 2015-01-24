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
                    | declarelist ctype ID CONSTASSIGN number SEMICOLON
                    | ctype ID CONSTASSIGN number SEMICOLON"""
    pass

def p_number(p):
    """number : INTEGER
              | FLOAT"""
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