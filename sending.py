#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools to send the data
"""
import argparse
import configparser
import json
import logging
import os
from collections import defaultdict

import rt

from config import DomainTreeNode, read_string_to_tree
from results import read_data

HOME = os.environ['HOME']


__all__ = ['group_by_mail', 'send_results_via_rtir']


def group_by_mail(results: list, config: DomainTreeNode) -> dict:
    """
    Group results by contact with a configuration
    """
    retval = defaultdict(list)
    for result in results:
        addresses = set()
        for domain in result['DNS Name']:
            addresses = addresses.union(config.get_all_addresses(domain))
        for address in addresses:
            retval[address].append(result)
    return retval


def send_results_via_rtir(resultfile, watchlistfile, configfile):
    config = configparser.ConfigParser()
    config.read_file(configfile)

    ticketing = rt.Rt(config['rt']['uri'], config['rt']['username'],
                      config['rt']['password'])
    if not ticketing.login():
        raise ValueError('Login to RT not successful.')

    logging.debug('Grouping results by mail address...')
    grouped = group_by_mail(read_data(resultfile),
                            read_string_to_tree(watchlistfile.read()))

    for address, data in grouped.items():
        logging.debug('Creating ticket for %s...', address)
        text = '\n\n'.join(['\n'.join(['%s: %s' % row for row in block.items()]) for block in data])
        ticket_id = ticketing.create_ticket(Queue=config['rt']['queue'],
                                            Subject='Certificate Transparency Log Information',
                                            Owner=config['rt']['username'],
                                            Requestor=address,
                                            Status='resolved',
                                            Text=text)
        if not ticket_id:
            raise ValueError('Creating RT ticket not successful.')
        logging.debug('Created ticket %d.', ticket_id)
    else:
        logging.debug('Empty input data.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['group', 'send-rt'],
                        default='group')
    parser.add_argument('results', type=argparse.FileType('r'))
    parser.add_argument('watchlist', type=argparse.FileType('r'),
                        default='%s/.certspotter/watchlist' % HOME)
    parser.add_argument('--config', type=argparse.FileType('r'),
                        default='%s/.config/certspotter_processing.ini' % HOME)
    parser.add_argument('--verbose', action='store_true',
                        help='Output debugging information')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(message)s', level='DEBUG')

    if args.mode == 'group':
        retval = group_by_mail(read_data(args.results),
                               read_string_to_tree(args.watchlist.read()))
        print(json.dumps(retval))
    if args.mode == 'send-rt':
        send_results_via_rtir(args.results, args.watchlist, args.config)
