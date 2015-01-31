__author__ = 'iravid'

from codegen import QuadInstruction

class Node(object):
    pass

class NExpression(Node):
    # Codegen interface should return (index_of_first_instruction, output_variable_name)
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
        lhs_index, lhs_output = self.lhs.codegen(context)
        rhs_index, rhs_output = self.rhs.codegen(context)

        output = context.get_temp_var()

        # Generate code according to expression types
        if self.lhs.expr_type == "int" and self.rhs.expr_type == "int":
            inst = NBinaryExpression.op_inst_map[self.op][0]
            context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "float":
            inst = NBinaryExpression.op_inst_map[self.op][1]
            context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "int" and self.rhs.expr_type == "float":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, lhs_output))

            inst = NBinaryExpression.op_inst_map[self.op][1]
            context.append_instruction(QuadInstruction(inst, output, conversion_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "int":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, rhs_output))

            inst = NBinaryExpression.op_inst_map[self.op][1]
            context.append_instruction(QuadInstruction(inst, output, lhs_output, conversion_output))

        # Return index of last instruction and output variable
        return lhs_index, output


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
        lhs_index, lhs_output = self.lhs.codegen(context)
        rhs_index, rhs_output = self.rhs.codegen(context)

        output = context.get_temp_var()

        # Generate code according to expression types
        if self.lhs.expr_type == "int" and self.rhs.expr_type == "int":
            inst = NRelExpression.op_inst_map[self.op][0]
            context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "float":
            inst = NRelExpression.op_inst_map[self.op][1]
            context.append_instruction(QuadInstruction(inst, output, lhs_output, rhs_output))

        elif self.lhs.expr_type == "int" and self.rhs.expr_type == "float":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, lhs_output))

            inst = NRelExpression.op_inst_map[self.op][1]
            context.append_instruction(QuadInstruction(inst, output, conversion_output, rhs_output))

        elif self.lhs.expr_type == "float" and self.rhs.expr_type == "int":
            conversion_output = context.get_temp_var()
            context.append_instruction(QuadInstruction("ITOR", conversion_output, rhs_output))

            inst = NRelExpression.op_inst_map[self.op][1]
            context.append_instruction(QuadInstruction(inst, output, lhs_output, conversion_output))

        return lhs_index, output

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
        lhs_index, lhs_output = self.lhs.codegen(context)
        rhs_index, rhs_output = self.rhs.codegen(context)

        add_output = context.get_temp_var()
        add_index = context.append_instruction(QuadInstruction("IADD", add_output, lhs_output, rhs_output))

        and_output = context.get_temp_var()
        and_index = context.append_instruction(QuadInstruction("IEQL", and_output, add_output, 2))

        return lhs_index, and_output

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
        lhs_index, lhs_output = self.lhs.codegen(context)
        rhs_index, rhs_output = self.rhs.codegen(context)

        add_output = context.get_temp_var()
        add_index = context.append_instruction(QuadInstruction("IADD", add_output, lhs_output, rhs_output))

        or_output = context.get_temp_var()
        or_index = context.append_instruction(QuadInstruction("IGRT", or_output, add_output, 0))

        return lhs_index, or_output


class NNegationExpression(NExpression):
    def __init__(self, expression):
        self.expression = expression
        self.expr_type = expression.expr_type

    def codegen(self, context):
        expr_index, expr_output = self.expression.codegen(context)

        output = context.get_temp_var()

        if self.expression.expr_type == "int":
            context.append_instruction(QuadInstruction("ISUB", output, 0, expr_output))
        elif self.expression.expr_type == "float":
            context.append_instruction(QuadInstruction("RSUB", output, 0, expr_output))

        return expr_index, output

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

        return index, output_var

class NInteger(NExpression):
    def __init__(self, value):
        assert(type(value) in (int, long))
        self.value = value
        self.expr_type = "int"

    def __repr__(self):
        return "<NInteger %d>" % self.value

    def codegen(self, context):
        output_var = context.get_temp_var()
        return context.append_instruction(QuadInstruction("IASN", output_var, self.value)), output_var


class NFloat(NExpression):
    def __init__(self, value):
        assert(type(value) is float)
        self.value = value
        self.expr_type = "float"

    def __repr__(self):
        return "<NFloat %d>" % self.value

    def codegen(self, context):
        output_var = context.get_temp_var()
        return context.append_instruction(QuadInstruction("RASN", output_var, self.value)), output_var

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
    # Codegen on statements returns (first instruction index, last instruction index)
    pass

class NAssignStatement(NStatement):
    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

    def codegen(self, context):
        expr_index, expr_output = self.expression.codegen(context)

        # This assumes that incorrect assignments (int := float) have been discarded in the parsing stage
        if self.ident.expr_type == "int":
            last_index = context.append_instruction(QuadInstruction("IASN", self.ident.ident, expr_output))
        else:
            if self.expression.expr_type == "float":
                last_index = context.append_instruction(QuadInstruction("RASN", self.ident.ident, expr_output))
            else:
                # float := int assignment means we have to perform an ITOR on the expr_output
                conversion_output = context.get_temp_var()
                itor_index = context.append_instruction(QuadInstruction("ITOR", conversion_output, expr_output))
                last_index = context.append_instruction(QuadInstruction("RASN", self.ident.ident, conversion_output))

        return expr_index, last_index

class NWriteStatement(NStatement):
    def __init__(self, expression):
        self.expression = expression

    def codegen(self, context):
        expr_index, expr_output = self.expression.codegen(context)

        if self.expression.expr_type == "int":
            last_index = context.append_instruction(QuadInstruction("IPRT", expr_output))
        else:
            last_index = context.append_instruction(QuadInstruction("RPRT", expr_output))

        return expr_index, last_index


class NReadStatement(NStatement):
    def __init__(self, ident):
        self.ident = ident

    def codegen(self, context):
        if self.ident.expr_type == "int":
            index = context.append_instruction(QuadInstruction("IINP", self.ident.ident))
        else:
            index = context.append_instruction(QuadInstruction("RINP", self.ident.ident))

        return index, index

class NTypeConversionStatement(NStatement):
    def __init__(self, ident, dest_type, expression):
        self.ident = ident
        self.dest_type = dest_type
        self.expression = expression

    def codegen(self, context):
        expr_index, expr_output = self.expression.codegen(context)

        if self.dest_type == "int":
            last_index = context.append_instruction(QuadInstruction("RTOI", self.ident.ident, expr_output))
        else:
            last_index = context.append_instruction(QuadInstruction("ITOR", self.ident.ident, expr_output))

        return expr_index, last_index

class NIfStatement(NStatement):
    def __init__(self, test_expression, then_statements, otherwise_statements):
        self.test_expression = test_expression
        self.then_statements = then_statements
        self.otherwise_statements = otherwise_statements

    def codegen(self, context):
        # Generate code for evaluating the test expression
        expr_index, expr_output = self.test_expression.codegen(context)

        # Generate a conditional jump that tests the expression output
        jmpz_index = context.append_instruction(QuadInstruction("JMPZ", -1, expr_output))

        # Generate code for then statements
        then_statements_indices = []
        for stmt in self.then_statements:
            then_statements_indices.append(stmt.codegen(context))

        # Add a jump that'll skip the otherwise block
        skip_otherwise_jump_index = context.append_instruction(QuadInstruction("JUMP", -1))

        otherwise_statements_indices = []
        for stmt in self.otherwise_statements:
            otherwise_statements_indices.append(stmt.codegen(context))

        # Backpatch the JMPZ instruction
        context.get_instruction(jmpz_index).a = skip_otherwise_jump_index + 1

        # Backpatch the JUMP that skips the otherwise block
        # If there's an 'otherwise' block, the jump should be to the instruction directly after the last one
        if otherwise_statements_indices:
            context.get_instruction(skip_otherwise_jump_index).a = otherwise_statements_indices[-1][1] + 1
        else:
            context.get_instruction(skip_otherwise_jump_index).a = skip_otherwise_jump_index + 1

        # Always return the index of the first instruction generated
        return expr_index


class NWhileStatement(NStatement):
    def __init__(self, test_expression, body_statements):
        self.test_expression = test_expression
        self.body_statements = body_statements

    def codegen(self, context):
        # Generate code for evaluating the test expression
        expr_index, expr_output = self.test_expression.codegen(context)

        # Generate a conditional jump that tests the expression output
        jmpz_index = context.append_instruction(QuadInstruction("JMPZ", -1, expr_output))

        # Generate code for loop body
        body_statements_indices = []
        for stmt in self.body_statements:
            body_statements_indices.append(stmt.codegen(context))

        # Unconditionally jump to test expression evaluation
        jump_index = context.append_instruction(QuadInstruction("JUMP", expr_index))

        # Backpatch the jmpz instruction
        context.get_instruction(jmpz_index).a = jump_index + 1

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
        assign_start_index, assign_last_index = self.start_assignment.codegen(context)

        # Generate code for evaluating the test expression
        expr_index, expr_output = self.test_expression.codegen(context)

        # Generate a conditional jump that tests expression output
        jmpz_index = context.append_instruction(QuadInstruction("JMPZ", -1, expr_output))

        # Generate code for loop body
        body_statements_indices = []
        for stmt in self.body_statements:
            body_statements_indices.append(stmt.codegen(context))

        # Generate the step statement
        step_start_index, step_last_index = self.step_statement.codegen(context)

        # Unconditionally jump to the test expression
        jump_index = context.append_instruction(QuadInstruction("JUMP", expr_index))

        # Backpatch the jmpz instruction
        context.get_instruction(jmpz_index).a = jump_index + 1

        return expr_index