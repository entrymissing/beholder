"""Metric Factory holds a regisry of all available metrics and builds the needed calsses."""

from sinks.sink import Sink
from sinks.carbon_sink import CarbonSink

SINK_REGISTRY = {
    'Sink': Sink,
    'CarbonSink': CarbonSink
}

def get_sink(name, parameters):
    """Factory function that returns a metric."""
    return SINK_REGISTRY[name](parameters)

def sink_factory(metric_config):
    for required_field in ("class", "parameters"):
        if not required_field in metric_config:
            raise KeyError("{} field missing in sink config".format(required_field))

    return get_sink(metric_config["class"],
                    metric_config["parameters"])
