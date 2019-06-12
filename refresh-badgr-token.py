#!/usr/bin/env python

import json
import requests
import logging
import sys

# LOGGER CONFIGURATION
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
fh = logging.FileHandler('/home/prodatalab/.local/logs/refresh-badgr-token.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
LOG.addHandler(fh)
LOG.addHandler(ch)
# END


FILE_PATH = '/home/prodatalab/.local/share/tutor/data/lms/uploads/badgr/badgr.json'
access_token = refresh_token = None
token_pair = None

with open(FILE_PATH, 'r') as f:
    token_pair = json.load(f)
    LOG.info("here is the token pair: {}".format(token_pair))

access_token = token_pair['badgr_access_token']
refresh_token = token_pair['badgr_refresh_token']
LOG.info("access_token: {} refresh_token: {}".format(access_token, refresh_token))

# curl -X POST 'https://api.badgr.io/o/token' -d "grant_type=refresh_token&refresh_token=wdISNqjogRN0eu4WN5HcyDnuseopPF"

try:
    resp = requests.post('https://api.badgr.io/o/token', data={'grant_type':'refresh', 'refresh_token':refresh_token})
    resp.raise_for_status()
except HTTPError as http_err:
    LOG.error("HTTP error occurred: {http_err}")
except Exception as err:
    LOG.error("Other error occurred: {err}")access_token = token_pair['access_token']
refresh_token = token_pair['refresh_token']
LOG.info("access_token: {} refresh_token: {}".format(access_token, refresh_token))
else:
    LOG.info("Successful request sent and received!")

tokens = resp.json()


with open(FILE_PATH, 'w') as f:
    json.dump(resp.json(), f)
    LOG.info("the resp was just dumped: {}".format(resp.json()))
