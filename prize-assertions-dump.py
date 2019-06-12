#!/bin/env python
import requests
import logging
LOGGER = logging.getLogger(__name__)

KEEPKEY_BADGE_ID = "Jgcj5qnsS--hD49XOXtZ-A"
BITCOIN5_BADGE_ID = "Me1G2ABUQDe9mE3pF-xlgg"
AMAZON5_BADGE_ID = "JDLH_d5QTz-LzUPYH-5eDw"


def get_prize_badgeclasses():
  response=requests.get(self._badgeclasses_url(), headers=self._get_headers(), timeout=settings.BADGR_TIMEOUT)
  response = requests.get(BADGR_BADGECLASS_URL, )

def get_prize_assertions():
  pass 

def dump_prize_assertions():
  pass 

def push_cleaned_badgeclass():
  pass


# helpers
def get_headers():
  """
  Headers to send along with the request-- used for authentication.
  """
  LOGGER.info("BADGE_CLASS: In _get_headers.. the BADGR_API_TOKEN length is: {} .. and the TOKEN is: {}".format(len(BadgrBackend.access_token_cls), BadgrBackend.access_token_cls))
  return {'Authorization': 'Bearer {}'.format(BadgrBackend.access_token_cls)}

def _badgeclasses_url(self, issuer_slug=BADGR_ISSUER_SLUG):
  """
  Badge Class centric functionality.
  """
  return "{}/issuers/{}/badgeclasses".format(self._base_url, issuer_slug)





if __name__ == '__main__':
