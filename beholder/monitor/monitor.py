"""Monitor holds the base classes for monitors in beholder.

Monitors hold lists of metrics and lists of sinks and a timespec.
They return when they should be called next and when called they
collect all the metrics and dump them into the sinks.
"""
import logging
import time
from random import random

class Monitor(object):
    """Base class for all metrics."""

    def __init__(self, metrics, sinks, frequency):
        self._metrics = metrics
        self._sinks = sinks
        self._frequency = frequency
        self._next_run = time.time() + random() * frequency

    def next_run(self):
        return self._next_run

    def collect(self):
        data_points = []
        for metric in self._metrics:
            # print(metric.__class__.__name__)
            try:
                data_points.extend(metric.collect())
            except Exception as e:
                print('Failed to collect metric {}'.format(e))
                logging.error('Failed to collect metric {}'.format(e))

        for sink in self._sinks:
            sink.dump(data_points)

        self._next_run += self._frequency
