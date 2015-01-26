__author__ = 'iravid'

class Node(object):
    pass

class NExpression(Node):
    # TODO: Codegen interface for expressions should return (output_variable_name, code)
    pass

class NBinaryExpression(NExpression):
    op_inst_map = {
        "+": ("IADD", "RADD"),
        "-": ("ISUB", "RSUB"),
        "*": ("IMLT", "RMLT"),
        "/": ("IDIV", "RDIV")
    }

    def __init__(self, op, lhs, rhs):
        self.expr_type = "float" if "float" in (lhs.expr_type, rhs.expr_type) else "int"
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def codegen(self, context):
        lhs_output, lhs_code = self.lhs.codegen(context)
        rhs_output, rhs_code = self.rhs.codegen(context)

        if self.lhs.expr_type == "int" and self.rhs.expr_type == "int":
            code = lhs_code + rhs_code
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][0]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "float":
            code = lhs_code + rhs_code
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][1]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)

        elif self.lhs.expr_type == "int" and self.rhs.expr_type == "float":
            code = lhs_code + rhs_code
            code += "ITOR %s %s\n" % (lhs_output, lhs_output)
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][1]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)
        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "int":
            code = lhs_code + rhs_code
            code += "ITOR %s %s\n" % (rhs_output, rhs_output)
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][1]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)



class NAddExpression(NBinaryExpression):
    """
    expression PLUS/MINUS expression
    """
    def __init__(self, op, lhs, rhs):
        NBinaryExpression.__init__(self, op, lhs, rhs)

    def codegen(self, context):
        return NBinaryExpression.codegen(self, context)


class NMultExpression(NBinaryExpression):
    """
    expression MULT/DIV expression
    """
    def __init__(self, op, lhs, rhs):
        NBinaryExpression.__init__(self, op, lhs, rhs)

    def codegen(self, context):
        return NBinaryExpression.codegen(self, context)

class NRelExpression(NExpression):
    """
    expression </>/==/!= expression
    """
    op_inst_map = {
        "==": ["IEQL", "REQL"],
        "!=": ["INQL", "RNQL"],
        "<": ["ILSS", "RLSS"],
        ">": ["IGRT", "RGRT"]
    }

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.expr_type = "int"

    def codegen(self, context):
        lhs_output, lhs_code = self.lhs.codegen(context)
        rhs_output, rhs_code = self.rhs.codegen(context)

        if self.lhs.expr_type == "int" and self.rhs.expr_type == "int":
            code = lhs_code + rhs_code
            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][0]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "float":
            code = lhs_code + rhs_code
            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][1]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)

        elif self.lhs.expr_type == "int" and self.rhs.expr_type == "float":
            code = lhs_code + rhs_code
            code += "ITOR %s %s\n" % (lhs_output, lhs_output)

            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][1]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "int":
            code = lhs_code + rhs_code
            code += "ITOR %s %s\n" % (rhs_output, rhs_output)

            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][1]
            code += "%s %s %s %s\n" % (inst, output, lhs_output, rhs_output)

            return (output, code)



class NAndExpression(NExpression):
    """
    expression AND expression
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.expr_type = "int"

    def codegen(self, context):
        lhs_output, lhs_code = self.lhs.codegen(context)
        rhs_output, rhs_code = self.rhs.codegen(context)

        add_output = context.get_temp_var()
        add_code = "IADD %s %s %s\n" % (add_output, lhs_output, rhs_output)

        and_output = context.get_temp_var()
        and_code = "IEQL %s %s %d\n" % (and_output, add_output, 2)

        code = lhs_code + rhs_code + add_code + and_code

        return (and_output, code)

class NOrExpression(NExpression):
    """
    expression OR expression
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.expr_type = "int"

    def codegen(self, context):
        lhs_output, lhs_code = self.lhs.codegen(context)
        rhs_output, rhs_code = self.rhs.codegen(context)

        add_output = context.get_temp_var()
        add_code = "IADD %s %s %s\n" % (add_output, lhs_output, rhs_output)

        or_output = context.get_temp_var()
        or_code = "IGRT %s %s %d\n" % (or_output, add_output, 0)

        code = lhs_code + rhs_code + add_code + or_code

        return (or_output, code)

class NNegationExpression(NExpression):
    def __init__(self, expression):
        self.expression = expression
        self.expr_type = expression.expr_type

    def codegen(self, context):
        expr_output, expr_code = self.expression.codegen(context)

        output = context.get_temp_var()

        if self.expression.expr_type == "int":
            code = expr_code + "ISUB %s %d %s" % (output, 0, expr_output)
        elif self.expression.expr_type == "float":
            code = expr_code + "RSUB %s %d %s" % (output, 0, expr_output)

        return (output, code)

class NIdentifier(NExpression):
    def __init__(self, ident_type, ident):
        self.ident = ident
        self.expr_type = ident_type

    def __repr__(self):
        return "<NIdentifier \"%s\">" % self.ident

    def codegen(self, context):
        output_var = context.get_temp_var()

        if self.expr_type == "int":
            code = "IASN %s %s\n" % (output_var, self.ident)
        else:
            code = "RASN %s %s\n" % (output_var, self.ident)

        return (output_var, code)

class NInteger(NExpression):
    def __init__(self, value):
        assert(type(value) in (int, long))
        self.value = value
        self.expr_type = "int"

    def __repr__(self):
        return "<NInteger %d>" % self.value

    def codegen(self, context):
        output_var = context.get_temp_var()
        code = "IASN %s %d\n" % (output_var, self.value)

        return (output_var, code)

class NFloat(NExpression):
    def __init__(self, value):
        assert(type(value) is float)
        self.value = value
        self.expr_type = "float"

    def __repr__(self):
        return "<NFloat %d>" % self.value

    def codegen(self, context):
        output_var = context.get_temp_var()
        code = "RASN %s %d\n" % (output_var, self.value)

        return (output_var, code)

class NProgram(Node):
    def __init__(self, program_name, declare_list, statement_list):
        self.program_name = program_name
        self.declare_list = declare_list
        self.statement_list = statement_list

    def __repr__(self):
        return "<NProgram \"%s\">" % self.program_name

class NDeclareList(Node):
    def __init__(self, var_list, const_list):
        self.var_list = var_list
        self.const_list = const_list

class NVarDecl(Node):
    def __init__(self, var_type, ident_list):
        self.var_type = var_type
        self.ident_list = ident_list

    def __repr__(self):
        return "<NVarDecl, type \"%s\", idents %s" % (self.var_type, self.ident_list)

class NConstDecl(Node):
    def __init__(self, const_type, const_ident, const_value):
        self.const_type = const_type
        self.const_ident = const_ident
        self.const_value = const_value

    def __repr__(self):
        return "<NConstDecl, type \"%s\", ident \"%s\", value %s" % (self.const_type, self.const_ident, self.const_value)

class NStatement(Node):
    pass

class NAssignStatement(NStatement):
    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

    def codegen(self, context):
        expr_output, expr_code = self.expression.codegen(context)

        # This assumes that incorrect assignments (int := float) have been discarded in the parsing stage
        if self.ident.expr_type == "int":
            return expr_code + "IASN %s %s\n" % (self.ident.ident, expr_output)
        else:
            if self.expression.expr_type == "float":
                return expr_code + "RASN %s %s\n" % (self.ident.ident, expr_output)
            else:
                # float := int assignment means we have to perform an ITOR on the expr_output
                return expr_code + "ITOR %s %s\n" % (self.expr_output, self.expr_output) \
                                 + "RASN %s %s\n" % (self.ident.ident, self.expr_output)

class NWriteStatement(NStatement):
    def __init__(self, expression):
        self.expression = expression

    def codegen(self, context):
        expr_output, expr_code = self.expression.codegen(context)

        if self.expression.expr_type == "int":
            return expr_code + ("IPRT %s\n" % expr_output)
        else:
            return expr_code + ("RPRT %s\n" % expr_output)

class NReadStatement(NStatement):
    def __init__(self, ident):
        self.ident = ident

    def codegen(self, context):
        if self.ident.expr_type == "int":
            return "IINP %s\n" % self.ident.ident
        else:
            return "RINP %s\n" % self.ident.ident

class NTypeConversionStatement(NStatement):
    def __init__(self, ident, dest_type, expression):
        self.ident = ident
        self.dest_type = dest_type
        self.expression = expression

    def codegen(self, context):
        expr_output, expr_code = self.expression.codegen(context)

        if self.dest_type == "int":
            return expr_code + "RTOI %s %s\n" % (self.ident.ident, expr_output)
        else:
            return expr_code + "ITOR %s %s\n" % (self.ident.ident, expr_output)


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