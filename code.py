class Code(object):
    def __init__(self):
        self.instructions = []
        self.name_stack = []
        self.number_stack = []
        self.global_names = {}
        self.local_names ={}
