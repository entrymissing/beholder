"""TwitterMetric holds the base classes in beholder."""
import json
import os
import time
import twitter

from metric.metric import Metric
from metric.datapoint import DataPoint


class TwitterMetric(Metric):
  """Base class for all metrics."""

  _REQUIRED_PARAMETERS = ['users', 'suffixes']

  def collect(self):
    """Collect grabs and returns a set of DataPoints."""
    home_dir = os.path.expanduser('~')
    json_path = os.path.join(home_dir, '.credentials', 'twitter_credentials.json')
    with open(json_path) as json_file:
      creds = json.load(json_file)

    api = twitter.Api(consumer_key=creds['consumer_key'],
                      consumer_secret=creds['consumer_secret'],
                      access_token_key=creds['access_token_key'],
                      access_token_secret=creds['access_token_secret'])

    now = time.time()
    dp = []
    for user, suffix in zip(self._parameters['users'],
                            self._parameters['suffixes']):
      new_statuses = api.GetUserTimeline(screen_name=user,
                                         count=200, include_rts=False)
      previous_statuses = self._data.setdefault(user, [])

      merged_statuses = []
      merged_status_ids = []
      for status in new_statuses:
        age = now - status.created_at_in_seconds
        if age < 60*60*24*30:
          merged_statuses.append(status)
          merged_status_ids.append(status.id)

      for status in previous_statuses:
        age = now - status.created_at_in_seconds
        if age < 60*60*24*30 and status.id not in merged_status_ids:
          merged_statuses.append(status)
          merged_status_ids.append(status.id)

      print(len(new_statuses))
      print(len(previous_statuses))
      print(len(merged_statuses))

      self._data[user] = merged_statuses
      statuses = merged_statuses

      base_name = self._base_name + suffix + '.'

      created_times = [now - s.created_at_in_seconds for s in statuses]

      dp.append(DataPoint(time.time(),
                          base_name + 'time_since_last',
                          min(created_times)))
      created_times = [t for t in created_times if t < 60*60*24*30]
      dp.append(DataPoint(time.time(),
                          base_name + 'count.30d',
                          len(created_times)))
      created_times = [t for t in created_times if t < 60*60*24*7]
      dp.append(DataPoint(time.time(),
                          base_name + 'count.7d',
                          len(created_times)))
      created_times = [t for t in created_times if t < 60*60*24*1]
      dp.append(DataPoint(time.time(),
                          base_name + 'count.1d',
                          len(created_times)))
      created_times = [t for t in created_times if t < 60*60*1]
      dp.append(DataPoint(time.time(),
                          base_name + 'count.1h',
                          len(created_times)))
    return dp
