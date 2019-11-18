#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:27:48 2019

@author: sebastian
"""


def read_string(string):
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
