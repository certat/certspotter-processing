#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some unit tests
"""
import io
import os
import unittest

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
{
    'id': 'ahPhe7audomoalejaku5LiweNoish5shee3WioW2ahg4cee6Kie5kongih0eiwae',
    'DNS Name': ['www.example.com'],
    'Pubkey': 'ThooGh1ahgehae6um4Veik6pofexeeTohmahgeechae0ui1thae6thuzie6gahj1',
    'Issuer': 'C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 International Server CA - G3',
    'Not Before': '2014-01-01 00:00:00 +0000 UTC',
    'Not After': '2015-01-01 23:59:59 +0000 UTC',
    'Log Entry': '123 @ https://ct.googleapis.com/pilot (Certificate)',
    'crt.sh': 'https://crt.sh/?sha256=ahPhe7audomoalejaku5LiweNoish5shee3WioW2ahg4cee6Kie5kongih0eiwae',
     'Filename': '/home/user/.certspotter/certs/ah/ahPhe7audomoalejaku5LiweNoish5shee3WioW2ahg4cee6Kie5kongih0eiwae.cert.pem',
     },
    {'id': 'oe2ga3ShahThiebeing9ookeece9seivae5ciChaa3ooLaew9luoLoh6uyozish7',
     'DNS Name': ['*.example.at', 'example.at'],
     'Pubkey': 'XobeLeud1gie3eetaicheiPhamus2Cah4iNohw7OV5gohgu8eiQuei9OoJ7suim1',
     'Issuer': 'C=DE, O=EUNETIC GmbH, CN=EuropeanSSL Server CA',
     'Not Before': '2015-01-01 00:00:00 +0000 UTC',
     'Not After': '2016-01-01 23:59:59 +0000 UTC',
     'Log Entry': '124 @ https://ct.googleapis.com/pilot (Certificate)',
     'crt.sh': 'https://crt.sh/?sha256=oe2ga3ShahThiebeing9ookeece9seivae5ciChaa3ooLaew9luoLoh6uyozish7',
     'Filename': '/home/user/.certspotter/certs/oe/oe2ga3ShahThiebeing9ookeece9seivae5ciChaa3ooLaew9luoLoh6uyozish7.cert.pem'}
     ]
config_expected = {'example.com': 'abc@example.com',
                   'example.net': 'abc@example.com',
                   'example.at': 'abc@example.com',
                   'cert.at': 'reports@cert.at',
                   'nic.at': 'reports@cert.at',
                   }
sending_expected = {
    'abc@example.com': [result_expected[0]],
    }


class TestCertspotterProcessing(unittest.TestCase):
    maxDiff = None

    def test_config_reader(self):
        result = config.read_string(config_string)
        self.assertEqual(result, config_expected)

    def test_result_reader_string(self):
        result = list(results.read_data(result_string))
        self.assertEqual(result, result_expected)

    def test_result_reader_fileobj_bytes(self):
        result = list(results.read_data(io.BytesIO(result_string.encode())))
        self.assertEqual(result, result_expected)

    def test_result_reader_fileobj_string(self):
        result = list(results.read_data(io.StringIO(result_string)))
        self.assertEqual(result, result_expected)

    def test_sending_grouping(self):
        result = sending.group_by_mail(result_expected, config_expected)
        import pprint
        pprint.pprint(result)
        self.assertEqual(dict(result), sending_expected)


if __name__ == '__main__':
    unittest.main()
