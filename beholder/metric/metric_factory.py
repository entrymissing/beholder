"""Metric Factory holds a regisry of all available metrics and builds the needed calsses."""

from metric.calendar_metric import CalendarMetric
from metric.gmail_metric import GMailLengthOfQueriesMetric, GMailOldestInInboxMetric, GMailAgeMetric
from metric.gfit_metric import GFitMetric
from metric.random_metric import RandomMetric
from metric.reddit_metric import RedditMetric
from metric.test_metric import TestMetric
from metric.twitter_metric import TwitterMetric

METRIC_REGISTRY = {
    'CalendarMetric': CalendarMetric,
    'GMailLengthOfQueriesMetric': GMailLengthOfQueriesMetric,
    'GMailOldestInInboxMetric': GMailOldestInInboxMetric,
    'GMailAgeMetric': GMailAgeMetric,
    'GFitMetric': GFitMetric,
    'RandomMetric': RandomMetric,
    'RedditMetric': RedditMetric,
    'TestMetric': TestMetric,
    'TwitterMetric': TwitterMetric,
}

def get_metric(name, base_name, parameters):
    """Factory function that returns a metric."""
    return METRIC_REGISTRY[name](base_name, parameters)

def metric_factory(metric_config):
    for required_field in ("class", "base_name", "parameters"):
        if not required_field in metric_config:
            raise KeyError("{} field missing in metric config".format(required_field))

    return get_metric(metric_config["class"],
                      metric_config["base_name"],
                      metric_config["parameters"])