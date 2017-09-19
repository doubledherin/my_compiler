from symbol import Symbol

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super(VariableSymbol, self).__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type
        )

    __repr__ = __str__
