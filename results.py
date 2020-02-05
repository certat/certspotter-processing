#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to work with certspotter's results
"""
import argparse
from collections import OrderedDict
import io
import json
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

    ToDo: Keep "raw" data
    """
    if isinstance(input_data, str):
        iterator = input_data.splitlines()
    elif isinstance(input_data, (io.IOBase, argparse.FileType)):
        iterator = input_data
    else:
        raise TypeError('Could not detect how to handle input of type '
                        '%r.' % type(input_data))

    result = OrderedDict()
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
            elif key == 'Filename':
                pass
            else:
                result[key] = value
        else:
            if result:
                yield result
            result = OrderedDict()
            result['id'] = line.strip(' :')
    if result:
        yield result  # final block


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certspotter_results', type=argparse.FileType('r'),
                        help="certspotter's results file, - for stdin")
    parser.add_argument('parsing_results', type=argparse.FileType('w'),
                        help="parsed results as JSON, - for stdout")
    args = parser.parse_args()
    json.dump(list(read_data(args.certspotter_results)), args.parsing_results)
