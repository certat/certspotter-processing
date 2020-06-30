#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some unit tests
"""
import io
import os
import unittest
from collections import OrderedDict

import config
import results
import sending

with open(os.path.join(os.path.dirname(__file__),
                       'tests/config-with-recipients.txt')) as handle:
    config_string = handle.read()
with open(os.path.join(os.path.dirname(__file__),
                       'tests/results.txt')) as handle:
    result_string = handle.read()

result_expected = [
    OrderedDict({
        'id': 'ahPhe7audomoalejaku5LiweNoish5shee3WioW2ahg4cee6Kie5kongih0eiwae',
        'DNS Name': ['www.example.com'],
        'Pubkey': 'ThooGh1ahgehae6um4Veik6pofexeeTohmahgeechae0ui1thae6thuzie6gahj1',
        'Issuer': 'C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 International Server CA - G3',
        'Not Before': '2014-01-01 00:00:00 +0000 UTC',
        'Not After': '2015-01-01 23:59:59 +0000 UTC',
        'Log Entry': '123 @ https://ct.googleapis.com/pilot (Certificate)',
        'crt.sh': 'https://crt.sh/?sha256=ahPhe7audomoalejaku5LiweNoish5shee3WioW2ahg4cee6Kie5kongih0eiwae',
    }),
    OrderedDict({'id': 'oe2ga3ShahThiebeing9ookeece9seivae5ciChaa3ooLaew9luoLoh6uyozish7',
                 'DNS Name': ['*.example.at', 'example.at'],
                 'Pubkey': 'XobeLeud1gie3eetaicheiPhamus2Cah4iNohw7OV5gohgu8eiQuei9OoJ7suim1',
                 'Issuer': 'C=DE, O=EUNETIC GmbH, CN=EuropeanSSL Server CA',
                 'Not Before': '2015-01-01 00:00:00 +0000 UTC',
                 'Not After': '2016-01-01 23:59:59 +0000 UTC',
                 'Log Entry': '124 @ https://ct.googleapis.com/pilot (Certificate)',
                 'crt.sh': 'https://crt.sh/?sha256=oe2ga3ShahThiebeing9ookeece9seivae5ciChaa3ooLaew9luoLoh6uyozish7'})
]
config_expected = {'example.com': 'abc@example.com',
                   'example.net': 'abc@example.com',
                   'example.at': 'abc@example.com',
                   'cert.at': 'reports@cert.at',
                   'nic.at': 'reports@cert.at',
                   }
sending_expected = {
    'abc@example.com': result_expected,
}


class TestCertspotterConfig(unittest.TestCase):

    def test_config_reader(self):
        result = config.read_string_to_dict(config_string)
        self.assertEqual(result, config_expected)

    def test_config_tree(self):
        result = config.read_string_to_tree(config_string)
        self.assertEqual(result.get_all_addresses('www.example.com'),
                         {'abc@example.com'})
        self.assertEqual(result.get_all_addresses('www.cert.at'),
                         {'reports@cert.at'})


class TestCertspotterResult(unittest.TestCase):
    maxDiff = None

    def test_result_reader_no_data(self):
        result = list(results.read_data(''))
        self.assertEqual(result, [])

    def test_result_reader_string(self):
        result = list(results.read_data(result_string))
        self.assertEqual(result, result_expected)

    def test_result_reader_fileobj_bytes(self):
        result = list(results.read_data(io.BytesIO(result_string.encode())))
        self.assertEqual(result, result_expected)

    def test_result_reader_fileobj_string(self):
        result = list(results.read_data(io.StringIO(result_string)))
        self.assertEqual(result, result_expected)


class TestCertspotterSending(unittest.TestCase):
    maxDiff = None

    def test_sending_grouping(self):
        config_tree = config.read_string_to_tree(config_string)
        result = sending.group_by_mail(result_expected, config_tree)
        self.assertEqual(dict(result), sending_expected)


class TestDomainTree(unittest.TestCase):

    def test_basics(self):
        tree = config.DomainTreeNode()
        tree['com'] = config.DomainTreeNode()
        tree['com']['example'] = config.DomainTreeNode()
        tree['com']['example'].addresses.append('user@example.com')
        tree['com']['another'] = config.DomainTreeNode()
        tree['com']['another'].addresses.append('user@another.com')

        self.assertEqual(tree['com'].addresses, [])
        self.assertEqual(tree['com']['example'].addresses, ['user@example.com'])
        tree['com'].addresses.append('com@example.com')

    def test_add_domain(self):
        tree = config.DomainTreeNode()
        tree.add_domain('.example.com', addresses=['foo'])
        self.assertEqual(tree['com']['example'].addresses, ['foo'])
        tree.add_domain('another.com', addresses=['bar'])
        self.assertEqual(tree['com']['example'].addresses, ['foo'])
        self.assertEqual(tree['com']['another'].addresses, ['bar'])

    def test_get_all_addresses(self):
        tree = config.DomainTreeNode()
        tree.add_domain('com', addresses=['com@'])
        tree.add_domain('example.com', addresses=['example@'])
        tree.add_domain('www.example.com', addresses=['www@'])
        tree.add_domain('another.com', addresses=['another@'])
        self.assertEqual(tree.get_all_addresses('example.com'),
                         {'com@', 'example@'})
        self.assertEqual(tree.get_all_addresses('www.example.com'),
                         {'com@', 'example@', 'www@'})
        with self.assertWarns(UserWarning):
            tree.get_all_addresses('something.abc')

    def test_get_all_addresses_wildcard(self):
        tree = config.DomainTreeNode()
        tree.add_domain('www.example.com', addresses=['www@'])
        tree.add_domain('sub.example.com', addresses=['sub@'])
        tree.add_domain('sub.www.example.com', addresses=['subwww@'])
        self.assertEqual(tree.get_all_addresses('*.example.com'),
                         {'sub@', 'www@'})


if __name__ == '__main__':
    unittest.main()
