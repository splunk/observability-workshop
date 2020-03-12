#!/usr/bin/env python

import argparse
import requests
import urllib
import json
import click

parser = argparse.ArgumentParser(description='SignalFx - Bulk Delete Detectors ')
parser.add_argument('-t', '--token', help='SignalFx Access Token', required=True)
parser.add_argument('-r', '--realm', help='SignalFx Realm - eu0, us0, us1, ap0', required=True)
parser.add_argument('-s', '--search', help='Search Detector name', required=True)
args = vars(parser.parse_args())

# SignalFx
endpoint = 'https://api.' + args['realm'] + '.signalfx.com/v2/detector/'

# Set headers
headers = {
    'Content-Type': 'application/json',
    'X-SF-TOKEN': args['token']
}

search = urllib.quote_plus(args['search'])
r = requests.get(endpoint + '?name=' + search, headers=headers)

detectors = json.loads(r.text)

for v in detectors['results']:
    print (v['id'] + ' - ' + v['name'])

if click.confirm('Do you want to delete?', default=True):
    for v in detectors['results']:
        r = requests.delete(endpoint + v['id'], headers=headers)
        print ('Deleting - ' + v['id'])
