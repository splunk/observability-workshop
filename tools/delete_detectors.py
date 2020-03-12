#!/usr/bin/env python

import argparse
import requests
import urllib
import json
import click

parser = argparse.ArgumentParser(description='SignalFx - Bulk Delete Detectors ')
parser.add_argument('-t', '--token', help='SignalFx Access Token', required=True)
parser.add_argument('-r', '--realm', help='SignalFx Realm - eu0, us0, us1, ap0', required=True)
parser.add_argument('-a', '--apiversion', help='SignalFx API Version (v1 or v2)', default="v2")
parser.add_argument('-s', '--search', help='Search Detector name', required=True)
args = vars(parser.parse_args())

# SignalFx
fetch = 'https://api.' + args['realm'] + '.signalfx.com/' + args['apiversion'] + '/detector/'
delete = 'https://api.' + args['realm'] + '.signalfx.com/v2/detector/'
# Set headers
headers = {
    'Content-Type': 'application/json',
    'X-SF-TOKEN': args['token']
}

search = urllib.quote_plus(args['search'])
if args['apiversion'] == "v2":
    r = requests.get(fetch + '?name=' + search, headers=headers)
else:
    r = requests.get(fetch + '?fields=sf_id, sf_detector&query=(sf_detector:*' + search + '*)', headers=headers)

detectors = json.loads(r.text)

if detectors['count'] != 0:
    if args['apiversion'] == 'v2':
        for v in detectors['results']:
            print (v['id'] + ' - ' + v['name'])
    else:
        for v in detectors['rs']:
            print (v['sf_id'] + ' - ' + v['sf_detector'])

    if click.confirm('Do you want to delete?', default=True):
        if args['apiversion'] == 'v2':
            for v in detectors['results']:
                r = requests.delete(delete + v['id'], headers=headers)
                print ('Deleting - ' + v['id'])
        else:
            for v in detectors['rs']:
                r = requests.delete(delete + v['sf_id'], headers=headers)
                print ('Deleting - ' + v['sf_id'])
else:
    print ('No matching detectors found!')
