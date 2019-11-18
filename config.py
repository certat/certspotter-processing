#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to work with certspotter's configuration
"""


def read_string(string: str) -> dict:
    """
    Reads a configuration string and returns a dictionary of domain -> comment mapping

    Parameters:
        string: the configuration as string

    Returns:
        result: the resulting dict
    """
    result = {}

    last_comment = ''
    for line in string.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            last_comment = line.strip(' #')
            continue
        result[line] = last_comment

    return result
