import unittest

from beholder.monitor.monitor import Monitor

class TestMonitor(unittest.TestCase):

  def test_monitor_base(self):
    base_monitor = Monitor('metrics', 'sinks')
    self.assertEqual(base_monitor._metrics, 'metrics')
    self.assertEqual(base_monitor._sinks, 'sinks')
