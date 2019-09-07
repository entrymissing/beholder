"""Metric holds the base classes in beholder."""
import abc
from typing import List

class Metric(object):
    """Base class for all metrics."""

    def __init__(self, metric_base_name, parameters, sinks):
        self._metric_base_name = metric_base_name
        self._parameters = parameters
        self._sinks = sinks
        self._validate_parameters()

    def _validate_parameters(self):
        if not self._metric_base_name:
            raise ValueError('metric_base_name may not be empty')

        if not self._metric_base_name.endswith('.'):
            raise ValueError('metric_base_name must end with a dot')

        if not self._sinks:
            raise ValueError('sinks may not be empty')

    @abc.abstractmethod
    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        pass
