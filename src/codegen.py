__author__ = 'iravid'

class CodegenContext(object):
    def __init__(self):
        self.symbols = {}
        self.root = None

    def install_symbol(self, ident, value):
        self.symbols[ident] = value

    def has_symbol(self, ident):
        return ident in self.symbols

    def get_symbol(self, ident):
        return self.symbols[ident]

context = CodegenContext()