class InstructionInterpreter(object):
    def __init__(self):
        self.stack = []
        self.environment = {}

    def ASSIGN(self, name):
        value = self.stack.pop()
        self.environment[name] = value

    def LOOKUP_AND_PUSH_VALUE(self, name):
        value = self.environment[name]
        self.stack.append(value)

    def PUSH_VALUE(self, value):
        self.stack.append(value)

    def ADD_TWO_VALUES(self):
        second = self.stack.pop()
        first = self.stack.pop()
        result = first + second
        self.stack.append(result)

    def SUBTRACT_TWO_VALUES(self):
        first = self.stack.pop()
        second = self.stack.pop()
        result = first - second
        self.stack.append(result)

    def MULTIPLY_TWO_VALUES(self):
        first = self.stack.pop()
        second = self.stack.pop()
        result = first * second
        self.stack.append(result)

    def DIVIDE_TWO_VALUES(self):
        first = self.stack.pop()
        second = self.stack.pop()
        result = first / second
        self.stack.append(result)

    def PRINT(self):
        print self.stack[-1]

    def parse_argument(self, instruction, argument, code_object):
        """ Understand what the argument to each instruction means."""
        numbers = ["PUSH_VALUE"]
        names = ["LOOKUP_AND_PUSH_VALUE", "ASSIGN"]

        if instruction in numbers:
            argument = code_object.number_stack[argument]
        elif instruction in names:
            argument = code_object.name_stack[argument]

        return argument

    def run_code(self, code_object):
        instructions = code_object.instructions[::-1]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, code_object)

            if instruction == "PUSH_VALUE":
                self.PUSH_VALUE(argument)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "SUBTRACT_TWO_VALUES":
                self.SUBTRACT_TWO_VALUES()
            elif instruction == "MULTIPLY_TWO_VALUES":
                self.MULTIPLY_TWO_VALUES()
            elif instruction == "DIVIDE_TWO_VALUES":
                self.DIVIDE_TWO_VALUES()
            elif instruction == "PRINT":
                self.PRINT()
            elif instruction == "ASSIGN":
                self.ASSIGN(argument)
            elif instruction == "LOOKUP_AND_PUSH_VALUE":
                self.LOOKUP_AND_PUSH_VALUE(argument)
