# intellinet-pdu-exporter
Prometheus Exporter to extract the data of Intellinet 19" Intelligent 8-Port PDUs and publish them in a format compatible for Prometheus.

## Installation
Update the [configuration-file](configuration.yml) to include the IP-addresses to your PDUs and customize the other options in case needed. As the status-file is world-readable, there is no need to know the credentials of the PDU 🤦.

```
sudo nano /etc/systemd/system/intellinet-pdu-exporter.service
[Unit]
Description=Prometheus Exporter to extract the data of Intellinet 19 Intelligent 8-Port PDUs and publish them in a format compatible for Prometheus.
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/intellinet-pdu-exporter/
ExecStartPre=/opt/intellinet-pdu-exporter/initialize.sh
ExecStart=/opt/intellinet-pdu-exporter/intellinet-pdu-exporter.py --config /opt/intellinet-pdu-exporter/configuration.yml

[Install]
WantedBy=multi-user.target
```
