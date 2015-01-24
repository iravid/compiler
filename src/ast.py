__author__ = 'iravid'

class Node(object):
    def __init__(self):
        pass

class NExpression(Node):
    pass

class NAddExpression(NExpression):
    """
    expression PLUS/MINUS expression
    """
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

class NMultExpression(NExpression):
    """
    expression MULT/DIV expression
    """
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

class NRelExpression(NExpression):
    """
    expression </>/<=/>=/==/!= expression
    """
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

class NAndStatement(NExpression):
    """
    expression AND expression
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class NOrStatement(NExpression):
    """
    expression OR expression
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class NIdentifier(NExpression):
    def __init__(self, ident):
        self.ident = ident

class NInteger(NExpression):
    def __init__(self, value):
        assert(type(value) in (int, long))
        self.value = value

class NFloat(NExpression):
    def __init__(self, value):
        assert(type(value) is float)
        self.value = value

class NProgram(Node):
    def __init__(self, declare_list, statement_list):
        self.declare_list = declare_list
        self.statement_list = statement_list

class NDeclareList(Node):
    def __init__(self, var_list, const_list):
        self.var_list = var_list
        self.const_list = const_list

class NVarDecl(Node):
    def __init__(self, var_type, ident_list):
        self.var_type = var_type
        self.ident_list = ident_list

class NConstDecl(Node):
    def __init__(self, const_type, const_ident):
        self.const_type = const_type
        self.const_ident = const_ident

class NStatement(Node):
    pass

class NAssignStatement(NStatement):
    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

class NWriteStatement(NStatement):
    def __init__(self, expression):
        self.expression = expression

class NReadStatement(NStatement):
    def __init__(self, ident):
        self.ident = ident

class NTypeConversionStatement(NStatement):
    def __init__(self, ident, dest_type, expression):
        self.ident = ident
        self.dest_type = dest_type
        self.expression = expression

class NIfStatement(NStatement):
    def __init__(self, test_expression, then_statements, otherwise_statements):
        self.test_expression = test_expression
        self.then_statements = then_statements
        self.otherwise_statements = otherwise_statements

class NWhileStatement(NStatement):
    def __init__(self, test_expression, body_statements):
        self.test_expression = test_expression
        self.body_statements = body_statements

class NFromStatement(NStatement):
    def __init__(self, start_assignment, test_expression, step_statement, body_statements):
        self.start_assignment = start_assignment
        self.test_expression = test_expression
        self.step_statement = step_statement
        self.body_statements = body_statements