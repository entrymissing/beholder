"""UptimeMetric reads /proc/uptime as metric."""
import time

from metric.metric import Metric
from metric.datapoint import DataPoint


class UptimeMetric(Metric):
    """Reads uptime of the machine it is running on."""

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        metric_name = self._base_name + 'uptime'
        with open('/proc/uptime', 'r') as fp:
          uptime = fp.read().split(" ")[0]
          return [DataPoint(time.time(), metric_name, uptime)]

