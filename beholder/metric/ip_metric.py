"""IPMetric grabs the external IP for this device and returns it a number."""
import time
from urllib import request

from metric.metric import Metric
from metric.datapoint import DataPoint


class IPMetric(Metric):
  """Base class for all metrics."""

  def collect(self):
    """Collect grabs and returns a set of DataPoints."""
    external_ip = request.urlopen('https://api.ipify.org').read().decode('ASCII')
    split_ip = [int(i) for i in external_ip.split('.')]
    split_ip.reverse()
    res = 0
    for i, ip_part in enumerate(split_ip):
      res += ip_part * (1000 ** i)
    metric_name = self._base_name + self._parameters['location']
    return [DataPoint(time.time(), metric_name, res)]
