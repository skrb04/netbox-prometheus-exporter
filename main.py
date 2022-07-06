import time
import os

from prometheus_client import start_http_server, Metric, REGISTRY
from prometheus_client.metrics_core import InfoMetricFamily
from prometheus_client.core import CounterMetricFamily
from environs import Env

import pynetbox

env = Env()
env.read_env()

class NetboxCollector(object):
    def __init__(self):
        pass

    def collect(self):
        netbox_url = env("NETBOX_API")
        netbox_token = env("NETBOX_API_TOKEN")
        netbox_threading = env.bool("NETBOX_THREADING", True)
        metrics_port = env.int("NETBOX_METRICS_PORT", 8000)

        netbox = pynetbox.api(
            netbox_url, netbox_token, threading=netbox_threading
        )

        devices = netbox.dcim.devices.count()
        metric = CounterMetricFamily("netbox_devices_total", "Total netbox device count", labels='metric')
        metric.add_metric(["netbox_devices_total"], devices)
        yield metric



if __name__ == "__main__":
    print("Starting netbox exporter")
    start_http_server(8000)
    REGISTRY.register(NetboxCollector())

    while True:
        time.sleep(1)