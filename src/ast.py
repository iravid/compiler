__author__ = 'iravid'

from codegen import QuadInstruction

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
        # Generate code for lhs and rhs expressions
        lhs_index = self.lhs.codegen(context)
        rhs_index = self.rhs.codegen(context)

        # Retrieve the temporary variable names
        lhs_output = context.get_instruction(lhs_index).a
        rhs_output = context.get_instruction(rhs_index).a

        # Generate code according to expression types
        if self.lhs.expr_type == "int" and self.rhs.expr_type == "int":
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][0]
            return context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "float":
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][1]
            return context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "int" and self.rhs.expr_type == "float":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, lhs_output))
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][1]
            return context.append_instruction(QuadInstruction(inst, output, conversion_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "int":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, rhs_output))
            output = context.get_temp_var()

            inst = NBinaryExpression.op_inst_map[self.op][1]
            return context.append_instruction(QuadInstruction(inst, output, lhs_output, conversion_output))



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
        # Generate code for lhs and rhs expressions
        lhs_index = self.lhs.codegen(context)
        rhs_index = self.rhs.codegen(context)

        # Retrieve output variable names for the expressions
        lhs_output = context.get_instruction(lhs_index).a
        rhs_output = context.get_instruction(rhs_index).a

        # Generate code according to expression types
        if self.lhs.expr_type == "int" and self.rhs.expr_type == "int":
            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][0]
            return context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "float":
            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][1]
            return context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "int" and self.rhs.expr_type == "float":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, lhs_output))
            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][1]
            return context.append_instruction(QuadInstruction(inst, output, conversion_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "int":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, rhs_output))
            output = context.get_temp_var()

            inst = NRelExpression.op_inst_map[self.op][1]
            return context.append_instruction(QuadInstruction(inst, output, lhs_output, conversion_output))



class NAndExpression(NExpression):
    """
    expression AND expression
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.expr_type = "int"

    def codegen(self, context):
        # Generate code for expressions
        lhs_index = self.lhs.codegen(context)
        rhs_index = self.rhs.codegen(context)

        # Retrieve output variables
        lhs_output = context.get_instruction(lhs_index).a
        rhs_output = context.get_instruction(rhs_index).a

        add_output = context.get_temp_var()
        add_index = context.append_instruction(QuadInstruction("IADD", add_output, lhs_output, rhs_output))

        and_output = context.get_temp_var()
        and_index = context.append_instruction(QuadInstruction("IEQL", and_output, add_output, 2))

        return and_index

class NOrExpression(NExpression):
    """
    expression OR expression
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.expr_type = "int"

    def codegen(self, context):
        # Generate code for expressions
        lhs_index = self.lhs.codegen(context)
        rhs_index = self.rhs.codegen(context)

        # Retrieve output variables
        lhs_output = context.get_instruction(lhs_index).a
        rhs_output = context.get_instruction(rhs_index).a

        add_output = context.get_temp_var()
        add_index = context.append_instruction(QuadInstruction("IADD", add_output, lhs_output, rhs_output))

        or_output = context.get_temp_var()
        or_index = context.append_instruction(QuadInstruction("IGRT", or_output, add_output, 0))

        return or_index


class NNegationExpression(NExpression):
    def __init__(self, expression):
        self.expression = expression
        self.expr_type = expression.expr_type

    def codegen(self, context):
        expr_index = self.expression.codegen(context)
        expr_output = context.get_instruction(expr_index).a

        output = context.get_temp_var()

        if self.expression.expr_type == "int":
            index = context.append_instruction(QuadInstruction("ISUB", output, 0, expr_output))
        elif self.expression.expr_type == "float":
            index = context.append_instruction(QuadInstruction("RSUB", output, 0, expr_output))

        return index

class NIdentifier(NExpression):
    def __init__(self, ident_type, ident):
        self.ident = ident
        self.expr_type = ident_type

    def __repr__(self):
        return "<NIdentifier \"%s\">" % self.ident

    def codegen(self, context):
        output_var = context.get_temp_var()

        if self.expr_type == "int":
            index = context.append_instruction(QuadInstruction("IASN", output_var, self.ident))
        else:
            index = context.append_instruction(QuadInstruction("RASN", output_var, self.ident))

        return index

class NInteger(NExpression):
    def __init__(self, value):
        assert(type(value) in (int, long))
        self.value = value
        self.expr_type = "int"

    def __repr__(self):
        return "<NInteger %d>" % self.value

    def codegen(self, context):
        output_var = context.get_temp_var()
        return context.append_instruction(QuadInstruction("IASN", output_var, self.value))


class NFloat(NExpression):
    def __init__(self, value):
        assert(type(value) is float)
        self.value = value
        self.expr_type = "float"

    def __repr__(self):
        return "<NFloat %d>" % self.value

    def codegen(self, context):
        output_var = context.get_temp_var()
        return context.append_instruction(QuadInstruction("RASN", output_var, self.value))

class NProgram(Node):
    def __init__(self, program_name, declare_list, statement_list):
        self.program_name = program_name
        self.declare_list = declare_list
        self.statement_list = statement_list

    def __repr__(self):
        return "<NProgram \"%s\">" % self.program_name

    def codegen(self, context):
        for stmt in self.statement_list:
            stmt.codegen(context)

        # Append a halt instruction
        context.append_instruction(QuadInstruction("HALT"))

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
        expr_index = self.expression.codegen(context)
        expr_output = context.get_instruction(expr_index).a

        # This assumes that incorrect assignments (int := float) have been discarded in the parsing stage
        if self.ident.expr_type == "int":
            return context.append_instruction(QuadInstruction("IASN", self.ident.ident, expr_output))
        else:
            if self.expression.expr_type == "float":
                return context.append_instruction(QuadInstruction("RASN", self.ident.ident, expr_output))
            else:
                # float := int assignment means we have to perform an ITOR on the expr_output
                conversion_output = context.get_temp_var()
                itor_index = context.append_instruction(QuadInstruction("ITOR", conversion_output, expr_output))
                rasn_index = context.append_instruction(QuadInstruction("RASN", self.ident.ident, conversion_output))

                return itor_index

class NWriteStatement(NStatement):
    def __init__(self, expression):
        self.expression = expression

    def codegen(self, context):
        expr_index = self.expression.codegen(context)
        expr_output = context.get_instruction(expr_index).a

        if self.expression.expr_type == "int":
            return context.append_instruction(QuadInstruction("IPRT", expr_output))
        else:
            return context.append_instruction(QuadInstruction("IPRT", expr_output))

class NReadStatement(NStatement):
    def __init__(self, ident):
        self.ident = ident

    def codegen(self, context):
        if self.ident.expr_type == "int":
            return context.append_instruction(QuadInstruction("IPRT", self.ident.ident))
        else:
            return context.append_instruction(QuadInstruction("IPRT", self.ident.ident))

class NTypeConversionStatement(NStatement):
    def __init__(self, ident, dest_type, expression):
        self.ident = ident
        self.dest_type = dest_type
        self.expression = expression

    def codegen(self, context):
        expr_index = self.expression.codegen(context)
        expr_output = context.get_instruction(expr_index)

        if self.dest_type == "int":
            return context.append_instruction(QuadInstruction("RTOI", self.ident.ident, expr_output))
        else:
            return context.append_instruction(QuadInstruction("ITOR", self.ident.ident, expr_output))


class NIfStatement(NStatement):
    def __init__(self, test_expression, then_statements, otherwise_statements):
        self.test_expression = test_expression
        self.then_statements = then_statements
        self.otherwise_statements = otherwise_statements

    def codegen(self, context):
        # Generate code for evaluating the test expression
        expr_index = self.test_expression.codegen(context)
        expr_output = context.get_instruction(expr_index).a

        # Generate a conditional jump that tests the expression output
        jmpz_index = context.append_instruction(QuadInstruction("JMPZ", -1, expr_output))

        # Generate code for then statements
        then_statements_indices = []
        for stmt in self.then_statements:
            then_statements_indices.append(stmt.codegen(context))

        otherwise_statements_indices = []
        for stmt in self.otherwise_statements:
            otherwise_statements_indices.append(stmt.codegen(context))

        # Backpatch the JMPZ instruction
        # If the 'then' block has instructions, the jump should be to the instruction directly after the last one
        if then_statements_indices:
            context.get_instruction(jmpz_index).b = then_statements_indices[-1] + 1
        else:
            context.get_instruction(jmpz_index).b = jmpz_index + 1

        # Always return the index of the first instruction generated
        return expr_index


class NWhileStatement(NStatement):
    def __init__(self, test_expression, body_statements):
        self.test_expression = test_expression
        self.body_statements = body_statements

    def codegen(self, context):
        # Generate code for evaluating the test expression
        expr_index = self.test_expression.codegen(context)
        expr_output = context.get_instruction(expr_index).a

        # Generate a conditional jump that tests the expression output
        jmpz_index = context.append_instruction(QuadInstruction("JMPZ", -1, expr_output))

        # Generate code for loop body
        body_statements_indices = []
        for stmt in self.body_statements:
            body_statements_indices.append(stmt.codegen(context))

        # Unconditionally jump to test expression evaluation
        jump_index = context.append_instruction(QuadInstruction("JUMP", expr_index))

        # Backpatch the jmpz instruction
        context.get_instruction(jmpz_index).b = jump_index + 1

        # Always return index of first inst.
        return expr_index

class NFromStatement(NStatement):
    def __init__(self, start_assignment, test_expression, step_statement, body_statements):
        self.start_assignment = start_assignment
        self.test_expression = test_expression
        self.step_statement = step_statement
        self.body_statements = body_statements

    def codegen(self, context):
        # Generate code for the start assignment
        start_index = self.start_assignment.codegen(context)

        # Generate code for evaluating the test expression
        expr_index = self.test_expression.codegen(context)
        expr_output = context.get_instruction(expr_index).a

        # Generate a conditional jump that tests expression output
        jmpz_index = context.append_instruction(QuadInstruction("JMPZ", -1, expr_output))

        # Generate code for loop body
        body_statements_indices = []
        for stmt in self.body_statements:
            body_statements_indices.append(stmt.codegen(context))

        # Generate the step statement
        step_index = self.step_statement.codegen(context)

        # Unconditionally jump to the test expression
        jump_index = context.append_instruction(QuadInstruction("JUMP", expr_index))

        # Backpatch the jmpz instruction
        context.get_instruction(jmpz_index).b = jump_index + 1

        return expr_index