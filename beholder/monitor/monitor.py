"""Monitor holds the class for monitors in beholder.

Monitors hold lists of metrics and sinks. When collect() is called
they collect all metrics and dump them into the sinks.
"""

class Monitor(object):
  """Base class for the monitor."""

  def __init__(self, metrics, sinks):
    self._metrics = metrics
    self._sinks = sinks

  def collect(self):
    """Collect all the metrics and submit them to the sinks."""
    data_points = []
    for metric in self._metrics:
      data_points.extend(metric.collect())
      metric.store_data()

    for sink in self._sinks:
      sink.dump(data_points)
