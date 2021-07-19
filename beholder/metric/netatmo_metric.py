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

    # zzz = [{'_id': '70:ee:50:65:28:ac', 'date_setup': 1605789095, 'last_setup': 1605789095, 'type': 'NAMain', 'last_status_store': 1607369299, 'firmware': 179, 'wifi_status': 58, 'reachable': True, 'co2_calibrating': False, 'data_type': ['Temperature', 'CO2', 'Humidity', 'Noise', 'Pressure'], 'place': {'altitude': 460, 'city': 'Dietlikon', 'country': 'CH', 'timezone': 'Europe/Zurich', 'location': [8.610825, 47.425205]}, 'station_name': 'Tanis (Indoor)', 'home_id': '5fb665a76f56a846bc53a94b', 'home_name': 'Tanis', 'dashboard_data': {'time_utc': 1607369296, 'Temperature': 22.4, 'CO2': 620, 'Humidity': 44, 'Noise': 42, 'Pressure': 999.4, 'AbsolutePressure': 946.1, 'min_temp': 21.3, 'max_temp': 28.6, 'date_max_temp': 1607344457, 'date_min_temp': 1607316446, 'temp_trend': 'stable', 'pressure_trend': 'stable'}, 'modules': [{'_id': '02:00:00:65:76:46', 'type': 'NAModule1', 'module_name': 'Outdoor', 'last_setup': 1605789097, 'data_type': ['Temperature', 'Humidity'], 'battery_percent': 100, 'reachable': True, 'firmware': 50, 'last_message': 1607369293, 'last_seen': 1607369261, 'rf_status': 75, 'battery_vp': 6030, 'dashboard_data': {'time_utc': 1607369261, 'Temperature': 2.9, 'Humidity': 81, 'min_temp': 2.5, 'max_temp': 5.4, 'date_max_temp': 1607343949, 'date_min_temp': 1607313083, 'temp_trend': 'stable'}}, {'_id': '03:00:00:09:e8:aa', 'type': 'NAModule4', 'module_name': 'Office', 'last_setup': 1607344439, 'data_type': ['Temperature', 'CO2', 'Humidity'], 'battery_percent': 100, 'reachable': True, 'firmware': 50, 'last_message': 1607369294, 'last_seen': 1607369281, 'rf_status': 82, 'battery_vp': 6355, 'dashboard_data': {'time_utc': 1607369281, 'Temperature': 22.7, 'CO2': 975, 'Humidity': 44, 'min_temp': 22.6, 'max_temp': 27, 'date_max_temp': 1607344454, 'date_min_temp': 1607366871, 'temp_trend': 'stable'}}]}]
    # station = zzz[0]

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
