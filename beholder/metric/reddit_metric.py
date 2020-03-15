"""Metric holds the base classes in beholder."""
import json
import time
import requests

from metric.metric import Metric
from metric.datapoint import DataPoint

class RedditMetric(Metric):
    """Base class for all metrics."""

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        test_sub = 'worldnews'
        test_after = int(time.time()-600)
        url = ('https://api.pushshift.io/reddit/search/submission/?&subreddit='+str(test_sub)+'&size=10000&after='
               +str(test_after))
        r = requests.get(url)
        data = json.loads(r.text)
        metric_name = self._base_name + 'worldnews.10m'
        return [DataPoint(time.time(), metric_name, len(list(data.values())[0]))]
