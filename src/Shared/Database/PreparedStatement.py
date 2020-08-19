class PreparedStatement:
    def __init__(self, query: str):
        self.query = query
        self.parameters = list()

    def add_param(self, index, value):
        self.parameters.insert(index, str(value))
