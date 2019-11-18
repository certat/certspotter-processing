#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:21:26 2019

@author: sebastian
"""

import os
import unittest

import config
import results


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


class TestCertspotterProcessing(unittest.TestCase):
    def test_config_reader(self):
        result = config.read_string(config_string)
        expected = {'example.com': 'abc@example.com',
                    'example.net': 'abc@example.com',
                    'cert.at': 'reports@cert.at',
                    'nic.at': 'reports@cert.at',
                    }
        self.assertEqual(result, expected)

    def test_result_reader(self):
        result = list(results.read_string(result_string))
        self.assertEqual(result, result_expected)


if __name__ == '__main__':
    unittest.main()
