#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prometheus Exporter to extract the data of Intellinet 19" Intelligent 8-Port PDUs and publish them in a format compatible for Prometheus.
"""

# Generic Imports.
from cProfile import label
import os
import sys
import logging
import yaml
import time
import argparse
import requests
import xmltodict
import prometheus_client

# Function to load and validate yml configuration.
def config_load(path):
    # Check if file exists.
    if os.path.exists(path):
        with open(path, 'r') as stream:
            # Try to decode yaml file.
            try:
                # Return configuration if valid.
                return(yaml.safe_load(stream))
            except yaml.YAMLError as exec:
                # Print execution if not valid.
                print(exec)
                return(False)
    else:
        # Files does not exist.
        return(False)

def convert_on_off(state):
    states = {
        'on': 1,
        'off': 0
    }
    return(states[state])

# Run exporter.
if __name__ == "__main__":
    # Initialize argparse.
    args_parser = argparse.ArgumentParser()

    # Add argument to specify the configuration file of the exporter.
    args_parser.add_argument(
        '--config',
        help='Path to configuration file.',
        default='configuration.yml',
        type=argparse.FileType('r', encoding='UTF-8')
    )

    # Parse configuratiion variables from CLI.
    args = args_parser.parse_args()

    # Check if config-file exists and validity.
    if args.config and config_load(args.config.name):
        # Load config-file.
        config = config_load(args.config.name)

        # Setup logging.
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=config['logging']['filename'],
            level=config['logging']['level']
        )

        # CLI outputs.
        print('Intellinet PDU Exporter started.')
        print('Listening on: ' + config['exporter']['address']  + ':' + str(config['exporter']['port']))
        print('Logs: ' + config['logging']['filename'])

        # Setup webserver.
        prometheus_client.start_http_server(
            addr=config['exporter']['address'],
            port=config['exporter']['port']
        )

        # Define metrics.
        intellinet_pdu_up = prometheus_client.Gauge(
            'intellinet_pdu_up',
            'Status',
            labelnames = ['pdu']
        )
        intellinet_pdu_cur0 = prometheus_client.Gauge(
            'intellinet_pdu_cur0',
            'Total Current',
            labelnames = ['pdu']
        )
        intellinet_pdu_tempBan = prometheus_client.Gauge(
            'intellinet_pdu_tempBan',
            'Temperature',
            labelnames = ['pdu']
        )
        intellinet_pdu_humBan = prometheus_client.Gauge(
            'intellinet_pdu_humBan',
            'Humidity',
            labelnames = ['pdu']
        )
        intellinet_pdu_outletStat = prometheus_client.Gauge(
            'intellinet_pdu_outletStat',
            'Power State',
            labelnames = ['pdu', 'socket']
        )

        # Never stop updating the values from the devices.
        while True:
            # Clear all metrics to .
            intellinet_pdu_up.clear()
            intellinet_pdu_cur0.clear()
            intellinet_pdu_tempBan.clear()
            intellinet_pdu_humBan.clear()
            intellinet_pdu_outletStat.clear()

            # Iterate through PDUs.
            for pdu in config['pdus']:
                try:
                    pdu_status = requests.get('http://' + pdu + '/status.xml', timeout=config['exporter']['timeout'])
                    if pdu_status.status_code == 200:
                        # HTTP code 200 looks like the query worked.
                        pdu_status = xmltodict.parse(pdu_status.content)
                        logging.info('Query of ' + pdu + ' was successfull and could be decoded.')

                        # Add metrics with label of PDU to exporter.
                        intellinet_pdu_up.labels(pdu).set(1)
                        intellinet_pdu_cur0.labels(pdu).set(pdu_status['response']['cur0'])
                        intellinet_pdu_tempBan.labels(pdu).set(pdu_status['response']['tempBan'])
                        intellinet_pdu_humBan.labels(pdu).set(pdu_status['response']['humBan'])

                        # Add state of all sockets to exporter.
                        for i in range(0,8):
                            intellinet_pdu_outletStat.labels(pdu, i).set(convert_on_off(pdu_status['response'][('outletStat' + str(i))]))

                        # Log state for happiness.
                        logging.info('Metrics updated for ' + pdu + '.')
                    else:
                        # In case HTTP code is not 200, add log message.
                        logging.error('Query of ' + pdu + ' failed with HTTP code: ' + pdu_status.status_code)

                        # Add metric for state.
                        intellinet_pdu_up.labels(pdu).set(0)
                except requests.RequestException:
                    # If HTTP request times out/failes, add log message.
                    logging.error('Query of ' + pdu + ' failed.')

                    # Add metric for state.
                    intellinet_pdu_up.labels(pdu).set(0)

            # Wait interval.
            logging.info('Wait ' + str(config['exporter']['interval']) + 's until next query.')
            time.sleep(config['exporter']['interval'])