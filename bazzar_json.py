#!/usr/bin/env python3
import argparse

import requests

__author__ = "Corsin Camichel"
__copyright__ = "Copyright 2020, Corsin Camichel"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "cocaman@gmail.com"

parser = argparse.ArgumentParser(description='Query sample information by tag or signature on Malware Bazaar by abuse.ch')
parser.add_argument('-t', '--type', help='Query type (tag or signature)', type=str, metavar="TYPE", default="tag", choices=["tag", "signature"], required=True)
parser.add_argument('-q', '--query', help='Query value (e.g. trickbot, exe)', type=str, metavar="QUERY", required=True)
parser.add_argument('-f', '--field', help='Single field you want', type=str, metavar="FIELD", required=False, choices=['sha256_hash', 'sha1_hash', 'md5_hash', 'file_name', 'signature', 'imphash'])

args = parser.parse_args()

if (args.type == "tag"):
    data = {
        'query': 'get_taginfo',
        'tag': '' + args.query + '',
    }
else:
    data = {
        'query': 'get_siginfo',
        'signature': '' + args.query + '',
    }

response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15)
json_response = response.content.decode("utf-8", "ignore")

if (args.field):
    query = ".data[]." + args.field
    json_response = jq(query).transform(text=json_response, text_output=True)

print(json_response)
