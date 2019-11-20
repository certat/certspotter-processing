#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to work with certspotter's configuration
"""
from collections import defaultdict
import warnings


class DomainTreeNode(defaultdict):
    def __init__(self, *args, **kwargs):
        self.addresses = list()
        super().__init__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        if args[0] == '*':
            raise ValueError('Wildcards are not supported in the configuration')
        super().__setitem__(*args, **kwargs)

    def add_domain(self, domain, addresses=None):
        domain = domain.strip('.').split('.')
        domain.reverse()

        last_leaf = self
        for part in domain:
            if part not in last_leaf:
                last_leaf[part] = DomainTreeNode()
            last_leaf = last_leaf[part]

        if addresses:
            last_leaf.addresses = addresses

    def get_all_addresses(self, domain):
        orig_domain = domain
        domain = domain.split('.')
        domain.reverse()

        addresses = set()

        last_leaf = self
        addresses.update(set(last_leaf.addresses))
        for index, part in enumerate(domain):
            if part == '*':
                if index != len(domain) -1:
                    warnings.warn('Wildcard must be most minor part of a domain (%r).'
                                  '' % orig_domain)
                for subdomain, next_leaf in last_leaf.items():
                    addresses.update(set(next_leaf.addresses))
                break
            if part not in last_leaf:
                if last_leaf is self:
                    warnings.warn('Could not attribute domain %r to a '
                                  'configured domain. Failing at %r.'
                                  '' % (orig_domain, part))
                break
            last_leaf = last_leaf[part]
            addresses.update(set(last_leaf.addresses))

        return addresses


setattr(DomainTreeNode, 'default_factory', DomainTreeNode)


def read_string(string: str) -> dict:
    """
    Reads a configuration string and returns a dictionary of domain -> comment mapping
    Leading and trailing dots are removed from domains

    Parameters:
        string: the configuration as string

    Returns:
        result: the resulting dict
    """
    result = {}

    last_comment = ''
    for line in string.splitlines():
        line = line.strip().strip('.')
        if not line:
            continue
        if line.startswith('#'):
            last_comment = line.strip(' #')
            continue
        result[line] = last_comment

    return result
