""" app.py is the main module holding the cental loop for the beholder service
"""

import argparse
import logging
import os
import sys
import time

from datetime import datetime

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
  parser.add_argument('-f', '--frequency', type=int, default=-1,
                      help='How often (in seconds) the metrics should be collected.')
  args = parser.parse_args()

  # Enable logging
  log_filename = 'logs/debug.log'
  os.makedirs(os.path.dirname(log_filename), exist_ok=True)
  logging.basicConfig(filename='logs/debug.log', level=logging.ERROR)

  # Create the monitors
  monitors = monitor_factory(args.config)

  next_run = time.time()

  while True:
    time.sleep(max(0, next_run - time.time()))
    next_run = time.time() + args.frequency

    # Run the monitors
    for monitor in monitors:
      monitor.collect()

    if args.frequency < 0:
      break

if __name__ == '__main__':
  main(sys.argv)
