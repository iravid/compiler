__author__ = 'iravid'

import ast
from ply import yacc
from lexer import tokens
from codegen import context

def p_program(p):
    "program : CODE ID LCURLPAREN declarations stmt_list RCURLPAREN"
    p[0] = ast.NProgram(p[2], p[4], p[5])
    context.root = p[0]

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
        # Install symbols for each ident
        for ident in p[3]:
            context.install_symbol(ident, ast.NIdentifier(p[1], ident))

        p[0] = [ast.NVarDecl(p[1], p[3])]

    elif len(p) == 6:
        for ident in p[4]:
            context.install_symbol(ident, ast.NIdentifier(p[2], ident))

        p[1].append(ast.NVarDecl(p[2], p[4]))
        p[0] = p[1]

def p_declarelist_constlist(p):
    """declarelist : declarelist ctype ID CONSTASSIGN number SEMICOLON
                   | ctype ID CONSTASSIGN number SEMICOLON"""
    if len(p) == 6:
        context.install_symbol(p[2], p[4])
        p[0] = [ast.NConstDecl(p[1], p[2], p[4])]
    elif len(p) == 7:
        context.install_symbol(p[3], p[5])
        p[1].append(ast.NConstDecl(p[2], p[3], p[5]))
        p[0] = p[1]

def p_number(p):
    """number : INTEGER
              | FLOAT"""
    if type(p[1]) is float:
        p[0] = ast.NFloat(p[1])
    elif type(p[1]) in (int, long):
        p[0] = ast.NInteger(p[1])

def p_number_error(p):
    """number : error"""
    print "Line %d: invalid number literal" % p.lineno(1)

def p_idents(p):
    """idents : idents COMMA ID
              | ID"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]

def p_idents_errors(p):
    """idents : error COMMA ID
              | error"""
    context.set_errors(True)
    print "Line %d: invalid identifier" % p.lineno(1)

def p_ctype(p):
    "ctype : CONST type"
    p[0] = p[2]

def p_type(p):
    """type : INTDECL
            | FLOATDECL"""
    p[0] = p[1]

def p_type_error(p):
    """type : error"""
    context.set_errors(True)
    print "Line %d: invalid type" % p.lineno(1)

def p_stmt_list_error(p):
    """stmt_list : stmt_list error"""
    context.set_errors(True)
    p[0] = p[1]

def p_stmt_list(p):
    """stmt_list : stmt_list stmt
                | empty"""
    if len(p) == 3:
        p[1].extend(p[2])
        p[0] = p[1]
    else:
        p[0] = []

def p_stmt(p):
    """stmt : assignment_stmt
            | type_conversion_stmt
            | control_stmt
            | read_stmt
            | write_stmt
            | stmt_block"""
    if type(p[1]) == list:
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_stmt_block(p):
    """stmt_block : LCURLPAREN stmt_list RCURLPAREN"""
    p[0] = p[2]

def p_write_stmt(p):
    "write_stmt : WRITE LPAREN expression RPAREN SEMICOLON"
    p[0] = ast.NWriteStatement(p[3])

def p_write_stmt_error(p):
    "write_stmt : WRITE LPAREN error RPAREN SEMICOLON"
    context.set_errors(True)
    print "Line %d: bad expression" % p.lineno(3)

def p_read_stmt(p):
    "read_stmt : READ LPAREN ID RPAREN SEMICOLON"
    symbol = context.get_symbol(p[3])

    if not symbol:
        print "Line %d: invalid identifier" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError
    if type(symbol) != ast.NIdentifier:
        print "Line %d: trying to read into a constant" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError

    p[0] = ast.NReadStatement(symbol)

def p_assignment_stmt(p):
    "assignment_stmt : ID ASSIGN expression SEMICOLON"
    symbol = context.get_symbol(p[1])

    if not symbol:
        print "Line %d: invalid identifier" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError
    if type(symbol) != ast.NIdentifier:
        print "Line %d: trying to assign into a constant" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError

    p[0] = ast.NAssignStatement(symbol, p[3])

def p_assignment_stmt_error(p):
    "assignment_stmt : ID ASSIGN error SEMICOLON"
    context.set_errors(True)
    print "Line %d: bad expression" % p.lineno(3)

def p_type_conversion_stmt(p):
    """type_conversion_stmt : ID ASSIGN IVAL LPAREN expression RPAREN SEMICOLON
                            | ID ASSIGN RVAL LPAREN expression RPAREN SEMICOLON"""
    symbol = context.get_symbol(p[1])

    if not symbol:
        print "Line %d: invalid identifier" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError
    if type(symbol) != ast.NIdentifier:
        print "Line %d: error trying to assign value to constant" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError

    if p[3] == "ival":
        p[0] = ast.NTypeConversionStatement(symbol, "int", p[5])
    elif p[3] == "rval":
        p[0] = ast.NTypeConversionStatement(symbol, "float", p[5])

def p_type_conversion_stmt_error(p):
    """type_conversion_stmt : ID ASSIGN IVAL LPAREN error RPAREN SEMICOLON
                            | ID ASSIGN RVAL LPAREN error RPAREN SEMICOLON"""
    context.set_errors(True)
    print "Line %d: bad expression" % p.lineno(5)

def p_control_stmt(p):
    """control_stmt : IF LPAREN boolexpr RPAREN THEN stmt OTHERWISE stmt
                    | WHILE LPAREN boolexpr RPAREN DO stmt
                    | FROM assignment_stmt TO boolexpr WHEN step DO stmt"""
    if p[1] == "if":
        p[0] = ast.NIfStatement(p[3], p[6], p[8])
    elif p[1] == "while":
        p[0] = ast.NWhileStatement(p[3], p[6])
    elif p[1] == "from":
        p[0] = ast.NFromStatement(p[2], p[4], p[6], p[8])

def p_control_stmt_error_expr(p):
    """control_stmt : IF LPAREN error RPAREN THEN stmt OTHERWISE stmt
                    | WHILE LPAREN error RPAREN DO stmt
                    | FROM assignment_stmt TO error WHEN step DO stmt"""
    context.set_errors(True)
    print "Line %d: error in test expression" % p.lineno(1)

def p_step(p):
    """step : ID ASSIGN ID addop number
            | ID ASSIGN ID mulop number"""

    lhs_symbol = context.get_symbol(p[1])
    rhs_symbol = context.get_symbol(p[3])

    if not lhs_symbol:
        print "Line %d: invalid identifier" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError
    if not rhs_symbol:
        print "Line %d: invalid identifier" % p.lineno(3)
        context.set_errors(True)
        raise SyntaxError
    if type(lhs_symbol) != ast.NIdentifier:
        print "Line %d: error trying to assign value to constant" % p.lineno(1)
        context.set_errors(True)
        raise SyntaxError

    if p[4] in ("+", "-"):
        expr = ast.NAddExpression(p[4], rhs_symbol, p[5])
    else:
        expr = ast.NMultExpression(p[4], rhs_symbol, p[5])

    p[0] = ast.NAssignStatement(lhs_symbol, expr)

def p_addop(p):
    """addop : PLUS
             | MINUS"""
    p[0] = p[1]

def p_mulop(p):
    """mulop : MULT
             | DIV"""
    p[0] = p[1]

def p_boolexpr(p):
    """boolexpr : boolexpr OR boolterm
                | boolterm"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.NOrExpression(p[1], p[3])

def p_boolterm(p):
    """boolterm : boolterm AND boolfactor
                | boolfactor"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.NAndExpression(p[1], p[3])

def p_boolfactor(p):
    """boolfactor : EXCLAMATION LPAREN boolexpr RPAREN
                  | expression relop expression"""
    if len(p) == 5:
        p[0] = ast.NNegationExpression(p[3])
    elif len(p) == 4:
        # Quad doesn't support GTE and LTE, so we'll convert the expression
        # to (lhs RELOP rhs) OR (lhs == rhs).
        if p[2] in (">=", "<="):
            relop_map = {">=": ">", "<=": "<"}

            eq_exp = ast.NRelExpression("==", p[1], p[3])
            relop_exp = ast.NRelExpression(relop_map[p[2]], p[1], p[3])

            p[0] = ast.NOrExpression(relop_exp, eq_exp)

        else:
            p[0] = ast.NRelExpression(p[2], p[1], p[3])

def p_relop(p):
    """relop : EQ
             | NEQ
             | LT
             | LTE
             | GT
             | GTE"""
    p[0] = p[1]

def p_expression(p):
    """expression : expression addop term
                  | term"""
    if len(p) == 4:
        p[0] = ast.NAddExpression(p[2], p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_term(p):
    """term : term mulop factor
            | factor"""
    if len(p) == 4:
        p[0] = ast.NMultExpression(p[2], p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_factor(p):
    """factor : LPAREN expression RPAREN
              | ID
              | number"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        if type(p[1]) is str:
            symbol = context.get_symbol(p[1])

            if not symbol:
                print "Line %d: invalid identifier" % p.lineno(1)
                context.set_errors(True)
                raise SyntaxError

            p[0] = symbol
        else:
            p[0] = p[1]

def p_empty(p):
    """empty : """
    pass

def p_error(p):
    pass

parser = yacc.yacc()