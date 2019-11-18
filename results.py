#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:31:28 2019

@author: sebastian
"""


def read_string(string):
    result = {}
    for line in string.splitlines():
        if not line:
            continue
        if line.startswith('\t'):
            key, value = line.split('=', maxsplit=1)
            key = key.strip()
            value = value.strip()
            if key == 'DNS Name':
                if key in result:
                    result[key].append(value)
                else:
                    result[key] = [value]
            else:
                result[key] = value
        else:
            if result:
                yield result
            result = {}
            result['id'] = line.strip(' :')
    yield result
