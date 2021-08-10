"""RandomMetric get a random value for testing purposes."""
import time
from random import random

from metric.metric import Metric
from metric.datapoint import DataPoint


class RandomMetric(Metric):
    """Random metric for testing purposes."""

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        metric_name = self._base_name + 'rand_float'
        return [DataPoint(time.time(), metric_name, random())]

