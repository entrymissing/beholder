"""sink.py is the template that also acts as an output option to STDOUT."""

class Sink(object):

  def __init__(self, parameters=False):
    self._parameters = parameters
    self.setup()

  def setup(self):
    """Any setup that needs to be done before running this sink."""
    pass

  def dump(self, data_points):
    """Dump the data points to the output."""
    print(data_points)
