"""Metric holds the base classes in beholder."""
import time
import datetime

from metric.metric import Metric
from metric.datapoint import DataPoint
from libs.google_api import build_service

class GFitMetric(Metric):
    """Base class for all metrics."""

    _REQUIRED_PARAMETERS = ['time_windows', 'suffixes']

    def collect(self):
        """Collect grabs and returns a set of DataPoints."""
        service = build_service('fitness', 'v1')
        data = []
        now = time.time()
        utcnow = datetime.datetime.utcnow()

        for time_window, suffix in zip(self._parameters['time_windows'], self._parameters['suffixes']):
            ndays = utcnow - datetime.timedelta(hours=time_window)
            start_time = ndays.isoformat("T") + "Z"
            response = service.users().sessions().list(userId='me', startTime=start_time).execute()

            num_workout = len(response['session'])
            long_workout_count = 0
            time_workout = 0
            for session in response['session']:
                delta_workout = ((int(session['endTimeMillis'])-int(session['startTimeMillis'])) / 1000)
                time_workout += delta_workout
                if delta_workout >= 30*60:
                    long_workout_count += 1

            data.append(DataPoint(now, self._base_name + 'num_workout.' + suffix, num_workout))
            data.append(DataPoint(now, self._base_name + 'num_long_workout.' + suffix, long_workout_count))
            data.append(DataPoint(now, self._base_name + 'time_workout.' + suffix, time_workout))
        return data
