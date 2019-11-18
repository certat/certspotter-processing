#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to work with certspotter's results
"""
import io
from typing import Generator, Union

__all__ = ['read_data']


def read_data(input_data: Union[str, bytes, io.IOBase]) -> Generator[int, None, None]:
    """
    Reads and interprets certspotter results from it's stdout output
    This is an iterator, yielding a dictionary for each certificate

    Parameters:
        input_data: string of results or file-like object (bytes or string)

    Returns:
        result: dictionary with the lines as key-value pairs
    """
    if isinstance(input_data, str):
        iterator = input_data.splitlines()
    elif isinstance(input_data, io.IOBase):
        iterator = input_data

    result = {}
    for line in iterator:
        if isinstance(line, bytes):
            line = line.decode()
        line = line.rstrip()
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
    yield result  # final block
