from symbol import Symbol

class FunctionSymbol(Symbol):
    def __init__(self, name, parameters=None):
        super(FunctionSymbol, self).__init__(name)
        self.parameters = parameters if parameters is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={parameters})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            parameters=self.parameters,
        )

    __repr__ = __str__
