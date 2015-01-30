__author__ = 'iravid'

class CodegenContext(object):
    def __init__(self):
        self.symbols = {}
        self.root = None
        self.instructions = []
        self._temp_counter = 0

    def install_symbol(self, ident, value):
        self.symbols[ident] = value

    def has_symbol(self, ident):
        return ident in self.symbols

    def get_symbol(self, ident):
        return self.symbols.get(ident, None)

    def get_temp_var(self):
        var = "_t%d" % self._temp_counter
        self._temp_counter += 1

        return var

    def get_instruction(self, index):
        return self.instructions[index - 1]

    def append_instruction(self, instruction):
        self.instructions.append(instruction)
        return len(self.instructions)

    def get_code(self):
        return "\n".join(map(lambda i: str(i), self.instructions))

class QuadInstruction(object):
    def __init__(self, inst, a="", b="", c=""):
        self.inst = inst
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return "%s %s %s %s" % (self.inst, self.a, self.b, self.c)

    def __repr__(self):
        return self.__str__()

context = CodegenContext()