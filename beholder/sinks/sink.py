class Sink(object):

    def __init__(self, parameters=False):
        self._parameters = parameters
        self.setup()

    def setup(self):
        pass

    def dump(self, data_points):
        print(data_points)
