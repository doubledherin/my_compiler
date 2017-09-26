from collections import OrderedDict
from built_in_symbol import BuiltInSymbol

class ScopedSymbolTable():
    def __init__(self, scope_name, scope_level):
        self._symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self._init_builtins()

    def _init_builtins(self):
        self.insert(BuiltInSymbol('REAL'))
        self.insert(BuiltInSymbol('INTEGER'))

    def __str__(self):
            h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
            lines = ['\n', h1, '=' * len(h1)]
            for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
            ):
                lines.append('%-15s: %s' % (header_name, header_value))
            h2 = 'Scope (Scoped symbol table) contents'
            lines.extend([h2, '-' * len(h2)])
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
