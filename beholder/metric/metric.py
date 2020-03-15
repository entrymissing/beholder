"""Metric holds the base classes in beholder."""
import abc

class Metric(object):
    """Base class for all metrics."""
    _REQUIRED_PARAMETERS = []

    def __init__(self, base_name, parameters):
        self._base_name = base_name
        self._parameters = parameters
        self._validate_parameters()

    def __str__(self):
        return self._base_name

    def _validate_parameters(self):
        if not self._base_name:
            raise ValueError('base_name may not be empty')

        if not self._base_name.endswith('.'):
            raise ValueError('base_name must end with a dot')

        for required_param in self._REQUIRED_PARAMETERS:
            if required_param not in self._parameters:
                raise ValueError('parameter {} is required for this {}'.format(required_param, self.__class__.__name__))

    @abc.abstractmethod
    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        pass
