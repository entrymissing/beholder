"""Metric holds the base classes in beholder."""
import sys
import time

from metric.metric import Metric
from metric.datapoint import DataPoint
from libs.google_api import build_service, list_mails_matching_query, get_message

class GMailLengthOfQueriesMetric(Metric):
    """Base class for all metrics."""
    _REQUIRED_PARAMETERS = ['queries', 'suffixes']

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        service = build_service('gmail', 'v1')
        data_points = []
        for query, suffix in zip(self._parameters['queries'], self._parameters['suffixes']):
            metric_name = self._base_name + suffix
            mails = list_mails_matching_query(service, query)
            data_points.append(DataPoint(time.time(), metric_name, len(mails)))
        return data_points

class GMailOldestInInboxMetric(Metric):
    """Base class for all metrics."""

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        service = build_service('gmail', 'v1')
        metric_name = self._base_name + 'inbox_oldest'
        mails = list_mails_matching_query(service, 'in:inbox')
        thread_age = {}
        now = time.time()

        if not mails:
            return [DataPoint(time.time(), metric_name, 0)]

        for mail in mails:
            thread_id = mail['threadId']
            msg = get_message(service, mail['id'])
            age = now - (int(msg['internalDate'])/1000)
            if thread_id not in thread_age:
                thread_age[thread_id] = age
            else:
                if age < thread_age[thread_id]:
                    thread_age[thread_id] = age

        return [DataPoint(time.time(), metric_name, max(thread_age.values()))]

class GMailAgeMetric(Metric):
    """Base class for all metrics."""
    _REQUIRED_PARAMETERS = ['queries', 'suffixes']

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        service = build_service('gmail', 'v1')
        data_points = []
        for query, suffix in zip(self._parameters['queries'], self._parameters['suffixes']):
            mails = list_mails_matching_query(service, query)
            newest_age = sys.maxsize
            oldest_age = 0
            now = time.time()
            for mail in mails:
                msg = get_message(service, mail['id'])
                age = now - (int(msg['internalDate'])/1000)
                newest_age = min(newest_age, age)
                oldest_age = max(oldest_age, age)

            metric_name_oldest = self._base_name + suffix + '_oldest'
            metric_name_newest = self._base_name + suffix + '_newest'
            data_points.append(DataPoint(time.time(), metric_name_oldest, oldest_age))
            data_points.append(DataPoint(time.time(), metric_name_newest, newest_age))
        return data_points
