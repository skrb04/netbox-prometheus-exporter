import time
import re

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
        metric = CounterMetricFamily("netbox_devices_total", "Total netbox device count")
        metric.add_metric(["netbox_devices_total"], devices)
        yield metric

        # This is unique to our netbox env, you may need to customize these
        device_type = netbox.dcim.devices.all()
        labels = ['site_group', 'manufacturer', 'name', 'tenant']
        metric2 = InfoMetricFamily("netbox_device", "Netbox Device", labels=labels)
        for device in device_type:
            # regex substitution for the site_group
            site_group = re.sub('^(.*)/.*$', r'\1', device.site.name)
            manufacturer = device.device_type.manufacturer
            name = device.name
            try:
                tenant = device.tenant.name
            except:
                tenant = "unknown"

            metric2.add_metric(
                labels=labels,
                value={"site_group": str(site_group), "manufacturer": str(manufacturer), "name": str(name), "tenant": str(tenant)},
            )
        yield metric2

if __name__ == "__main__":
    print("Starting netbox exporter")
    start_http_server(8000)
    REGISTRY.register(NetboxCollector())

    while True:
        time.sleep(1)
