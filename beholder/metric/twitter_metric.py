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
            statuses = api.GetUserTimeline(screen_name=user,
                                           count=200, include_rts=False)
            if len(statuses) < 1:
              print(user)
              print(statuses)
            base_name = self._base_name + suffix + '.'

            created_times = [now - s.created_at_in_seconds for s in statuses]

            dp.append(DataPoint(time.time(),
                                base_name + 'time_since_last',
                                min(created_times)))
            created_times = [t for t in created_times if t < 60*60*24*7]
            dp.append(DataPoint(time.time(),
                                base_name + 'count.7d',
                                len(created_times)))
            created_times = [t for t in created_times if t < 60*60*24*1]
            dp.append(DataPoint(time.time(),
                                base_name + 'count.1d',
                                len(created_times)))
        return dp
