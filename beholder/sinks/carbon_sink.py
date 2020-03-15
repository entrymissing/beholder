import logging
import pickle as pkl
import socket
import struct
import time

from sinks.sink import Sink

class CarbonSink(Sink):
    _MAX_RETRIES = 3
    def setup(self):
        self._carbon_server = self._parameters['carbon_server']
        self._carbon_port = int(self._parameters['carbon_port'])

    def dump(self, data_points):
        sub_data = []
        for data in data_points:
            key = data.metric_name
            value = data.value
            timestamp = data.timestamp
            sub_data.append((key, (timestamp, value)))

        payload = pkl.dumps(sub_data, protocol=2)
        header = struct.pack("!L", len(payload))
        message = header + payload

        for _ in range(self._MAX_RETRIES):
            try:
                sock = socket.socket()
                sock.connect((self._carbon_server,
                              self._carbon_port))
                sock.sendall(message)
                sock.close()
            except ConnectionRefusedError:
                time.sleep(30)
                continue
            else:
                logging.warning('Succesfully sent the pickle')
                break
