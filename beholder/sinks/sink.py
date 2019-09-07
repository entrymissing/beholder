import abc

class Sink(object):

    def __init__(self, parameters = {}):
        self._parameters = parameters
        self.setup()

    def setup(self):
        pass

    def dump(self, data):
        print(data)
