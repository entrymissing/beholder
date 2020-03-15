""" app.py is the main module holding the cental loop for the beholder service
"""

import argparse
import logging
import sys
import time

from monitor.monitor_factory import monitor_factory

def main(_):
  """The main function.:"""
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--carbon_server', type=str, default='localhost',
                      help="DNS of the server that carbon is running on. Default is localhost.")
  parser.add_argument('-p', '--carbon_port', type=int, default=2004,
                      help='Pickle port of the carbon server. Default is 2004.')
  parser.add_argument('-c', '--config', type=str,
                      help='Configuration file to use')
  parser.add_argument('-d', '--daemon', type=bool, default=False,
                      help='Run as daemon and take care of scheduling. If false all probes will '
                           'be run just once ignoring frequency.')
  args = parser.parse_args()

  logging.basicConfig(filename='logs/debug.log', level=logging.ERROR)

  monitors = monitor_factory(args.config)

  # Run as one-shot
  if not args.daemon:
    for monitor in monitors:
      monitor.collect()

  # Run scheduler
  else:
    monitor_queue = []
    for monitor in monitors:
      monitor_queue.append((monitor.next_run(), monitor))
    monitor_queue = sorted(monitor_queue)
    while True:
      next_run, monitor = monitor_queue.pop(0)
      if  next_run - time.time() < 0:
        logging.error('Got negative wait time')
      time.sleep(max(0, next_run - time.time()))
      monitor.collect()
      monitor_queue.append((monitor.next_run(), monitor))
      monitor_queue = sorted(monitor_queue)


if __name__ == '__main__':
  main(sys.argv)
