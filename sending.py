#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools to send the data
"""
from collections import defaultdict
import warnings


def group_by_mail(results, config):
    """
    TODO: Handle wildcards and subdomains
    """
    retval = defaultdict(list)
    for result in results:
        addresses = set()
        for domain in result['DNS Name']:
            domain = domain.strip('*.')
            if domain in config:
                addresses.add(config[domain])
            else:
                warnings.warn('Could not map domain %r to an address.' % domain)
        for address in addresses:
            retval[address].append(result)
    return retval
