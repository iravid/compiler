__author__ = 'iravid'

class CodegenContext(object):
    def __init__(self):
        self.symbols = {}
        self.root = None
        self._temp_counter = 0

    def install_symbol(self, ident, value):
        self.symbols[ident] = value

    def has_symbol(self, ident):
        return ident in self.symbols

    def get_symbol(self, ident):
        return self.symbols[ident]

    def get_temp_var(self):
        var = "_t%d" % self._temp_counter
        self._temp_counter += 1

        return var

context = CodegenContext()