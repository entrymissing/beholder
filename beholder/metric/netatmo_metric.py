"""NetatmoMetric grabs data from the Netatmo stations."""
import time
import netatmo
import pickle as pkl
from random import random

from metric.metric import Metric
from metric.datapoint import DataPoint


class NetatmoMetric(Metric):
  """Netatmo class for collecting the metrics."""



  def collect(self):
    """Collect grabs and returns a set of DataPoints."""
    creds = pkl.load(open('/home/entrymissing/.credentials/netatmo.pkl', 'rb'))
    weather_station = netatmo.WeatherStation(creds)
    weather_station.get_data()
    station = weather_station.devices[0]

    data = []
    now = time.time()
    for metric_type in station['data_type']:
      metric_name = self._base_name + 'basis.' + metric_type.lower()
      data.append(DataPoint(now, metric_name, station['dashboard_data'][metric_type]))
    for module_data in station['modules']:
      module_name = module_data['module_name'].lower()
      data.append(DataPoint(
          now, self._base_name + module_name + '.battery', module_data['battery_percent']))
      for metric_type in module_data['data_type']:
        metric_name = self._base_name + module_name + '.' + metric_type.lower()
        data.append(DataPoint(now, metric_name, module_data['dashboard_data'][metric_type]))


    return data
