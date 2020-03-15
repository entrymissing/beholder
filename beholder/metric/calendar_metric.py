"""Metric holds the base classes in beholder."""
import time
import datetime
from dateutil.parser import parse

from metric.metric import Metric
from metric.datapoint import DataPoint
from libs.google_api import build_service, get_calendar_entries_by_query

class CalendarMetric(Metric):
    """Base class for all metrics."""

    _REQUIRED_PARAMETERS = ['time_windows', 'suffixes']

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        service = build_service('calendar', 'v3')
        data = []

        for time_window, suffix in zip(self._parameters['time_windows'],
                                       self._parameters['suffixes']):
            # TODO: Get Search prefix and calendar from configs
            events = get_calendar_entries_by_query(service, "S-", time_window, "Tracking")

            seconds_since = []
            long_count = 0
            short_count = 0
            for event in events:
                start_time = parse(event['start'].get('dateTime'))
                end_time = parse(event['end'].get('dateTime'))
                seconds_since.append(
                    (datetime.datetime.now(datetime.timezone.utc) - start_time).total_seconds())
                event_length = end_time - start_time
                if event_length.seconds <= 30*60:
                    short_count += 1
                else:
                    long_count += 1

            data.append(DataPoint(time.time(), self._base_name + 's_count.' + suffix, len(events)))
            data.append(DataPoint(time.time(), self._base_name + 's_seconds_since.' + suffix, min(seconds_since)))
            data.append(DataPoint(time.time(), self._base_name + 's_short_count.' + suffix, short_count))
            data.append(DataPoint(time.time(), self._base_name + 's_long_count.' + suffix, long_count))
        return data
