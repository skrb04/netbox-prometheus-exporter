# netbox-prometheus-exporter
Netbox prometheus exporter to generate graphs/metrics from netbox data

Our security team was exporting this data into a spreadsheet on a regular basis, this exporter allows us to generate Grafana graphs.

Sample deployment for k8s included with Service and ServiceMonitor

Prometheus Metrics generated:
netbox_devices_total,
netbox_device_info
