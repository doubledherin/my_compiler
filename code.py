import json

class Code(object):
    def __init__(self):
        self.instructions = []
        self.name_stack = []
        self.number_stack = []
        self.global_names = {}
        self.local_names = {}

    def toJSON(self):
        # return json.dumps(self, default=lambda o: o.__dict__,
        #     sort_keys=True, indent=4)
        return json.dumps(self.__dict__)
