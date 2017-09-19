from collections import OrderedDict
from built_in_symbol import BuiltInSymbol

class SymbolTable():
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtins()

    def _init_builtins(self):
        self.insert(BuiltInSymbol('REAL'))
        self.insert(BuiltInSymbol('INTEGER'))

    def __str__(self):
        header = 'Symbol table contents'
        lines = ['\n', header, '_' * len(header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def insert(self, symbol):
        print('Inserting: %s into symbol table' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print 'Look up: {}'.format(name)
        return self._symbols.get(name)
