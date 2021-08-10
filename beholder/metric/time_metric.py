"""TimeMetric sends current clocktime as metric."""
import time

from metric.metric import Metric
from metric.datapoint import DataPoint


class TimeMetric(Metric):
    """Reads clock of the machine it is running on."""

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        metric_name = self._base_name + 'time'
        return [DataPoint(time.time(), metric_name, time.time())]

