import json

from metric.metric_factory import metric_factory
from monitor.monitor import Monitor
from sinks.sink_factory import sink_factory

def monitor_factory(config_file):
    with open(config_file) as file_handle:
        configs = json.loads(file_handle.read())

    monitors = []
    for monitor_config in configs:
        validate_config(monitor_config)
        metrics = []
        for metric_config in monitor_config["metrics"]:
            metrics.append(metric_factory(metric_config))

        sinks = []
        for sink_config in monitor_config["sinks"]:
            sinks.append(sink_factory(sink_config))

        monitors.append(Monitor(metrics, sinks, monitor_config["frequency"]))
    return monitors


def validate_config(monitor_config):
    for required_field in ("metrics", "sinks", "frequency"):
        if not required_field in monitor_config:
            raise KeyError("{} field missing in monitor config".format(required_field))
