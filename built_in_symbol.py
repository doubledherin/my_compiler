from symbol import Symbol

class BuiltInSymbol(Symbol):
    def __init__(self, name):
        super(BuiltInSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )
