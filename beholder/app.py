from metric.random_metric import RandomMetric
from sinks.sink import Sink
from metric.datapoint import DataPoint

rm = RandomMetric('test.random.', {}, [0])
si = Sink()

data = rm.collect()
print(DataPoint(123, 'test.random', 667))
si.dump(data)
