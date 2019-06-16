#!/usr/bin/env python3


import sys
import os
import requests
import logging
import json
# from requests.packages.urllib3.exceptions import HTTPError


BADGR_ACCESS_TOKEN = 'WMyG6DHCpBzdZmdiwHPer5DB4zsadt'


BADGR_BASE_URL = 'https://badgr.firstcontactcrypto.com/'
BADGR_BADGECLASS_PATH = 'v2/issuers/{}/badgeclasses'
BADGR_BADGECLASS_DELETE_PATH = 'v2/badgeclasses/{}'
BADGR_ASSERTION_PATH = 'v2/badgeclasses/{}/assertions'
BADGR_ASSERTION_DELETE_PATH = 'v2/assertions/{}'
BADGR_ASSERTION_PATH_BY_ISSUER = 'v2/issuers/{}/assertions'
BADGR_ISSUER_ID = 'rGy5MNWtQgSs1vfnLyPlmg'
BADGR_EPIPHANY_BADGE_ID = 'V_MaSinhQJeKGOtZz6tDAQ'
BADGR_COURSE_BADGE_ID = '2gnNK3RZSlOutOrVeQlD_A'
BADGR_TIMEOUT = 5000
LOGGER = logging.getLogger(__name__)


BADGR_BITCOIN5_PRIZE_ID = 'Me1G2ABUQDe9mE3pF-xlgg'
BADGR_KEEPKEY_PRIZE_ID = 'Jgcj5qnsS--hD49XOXtZ-A'
BADGR_AMAZON5_PRIZE_ID = 'JDLH_d5QTz-LzUPYH-5eDw'


all_badgeclasses = {}
badgeclass_list = []
prize_badge_id = 0
prize_badge = {}
all_assertions = {}


def get_base_headers():
  ret = {
    'Authorization': 'Bearer {}'.format(BADGR_ACCESS_TOKEN)
  }
  return ret


def get_post_headers():
  """
  Headers to send along with the request-- used for authentication.
  """
  ret = {
    'Authorization': 'Bearer {}'.format(BADGR_ACCESS_TOKEN),
    'Content-Type': 'application/json'
  }
  return ret

def log_if_raised(response, data):
  """
  Log server response if there was an error.
  """
  # LOGGER.info("In _log_if_raised.. RESPONSE: headers: {}, text: {}".format(response.headers, response.text))
  if response.status_code < 200 or response.status_code >= 300:
    LOGGER.error("http request failed: {}, {}, {}".format(response.status_code, response.msg, response.text))
  return False


def get_badgeclasses():
  global all_badgeclasses
  global badgeclass_list
  r = requests.get(BADGR_BASE_URL + BADGR_BADGECLASS_PATH.format(BADGR_ISSUER_ID), headers=get_base_headers())
  if r.status_code >= 200 and r.status_code <= 300:
    # print(r.json())
    # print("In list_badgeclasses.. r.json() return type is: {}".format(type(r.json())))
    all_badgeclasses = r.json()
    badgeclass_list = all_badgeclasses['result']
    return all_badgeclasses
  else:
    LOGGER.error("In get_headers.. ERROR: respone: {} msg: {}".format(r.status_code, r.text))


# def filter_badgeclasses(bc_list):
#   ret_list = []
#   for i in range(len(bc_list)):
#     bc = bc_list[i]
#     if bc['entityId'] == BADGR_EPIPHANY_BADGE_ID or bc['entityId'] == BADGR_COURSE_BADGE_ID:
#       # print("FOUND: {}".format(bc['entityId']))
#       continue
#     else:
#       ret_list.append(bc)
#   return ret_list

def filter_badgeclasses():
  """
  """
  global prize_badge
  global prize_badge_id
  retlist = []

  if not all_badgeclasses:
    get_badgeclasses()
  for b in badgeclass_list:
    if b['entityId'] == BADGR_BITCOIN5_PRIZE_ID or b['entityId'] == BADGR_KEEPKEY_PRIZE_ID or b['entityId'] == BADGR_AMAZON5_PRIZE_ID:
      # print(json.loads(b['description'])[0]['prize'])
      # for d in json.loads(b['description']):
        # print(d)
      retlist.append(b)
  # print("TYPE: {} LIST: {}".format(type(retlist[0]), retlist))
  return retlist
  #   if b[k] == v:
  #     if not inverse:
  #       retlist.append(b)
  #   else:
  #     if inverse and b['description'].startswith('[{'):
  #       retlist.append(b)
  # # print(len(filtered))
  # if len(retlist) == 1:
  #   prize_badge = retlist[0]
  #   prize_badge_id = prize_badge['entityId']
  # return retlist



def list_assertions():
  path = BADGR_BASE_URL + BADGR_ASSERTION_PATH_BY_ISSUER.format(BADGR_ISSUER_ID)
  r = requests.get(path, headers = get_base_headers())
  if r.status_code >=200 and r.status_code <= 300:
    return r.json()
  else:
    LOGGER.error('In list_assertions.. ERROR: RESPONSE: {} HEADERS: {}'.format(r.status_code, r.headers))


def delete_all_assertions(ba_list):
  for ba in ba_list:
    ba_id = ba['entityId']
    # print("ba_id: {}", ba_id)
    data = json.dumps({"revocation_reason": "House Cleaning"})
    r = requests.delete(BADGR_BASE_URL + BADGR_ASSERTION_DELETE_PATH.format(ba_id), headers=get_post_headers(), json=data)
    sc = r.status_code
    # print(r.status_code)
    if sc >= 200 and sc < 300:
      print("SUCCESS: {} DELETED".format(ba['entityId']))
    else:
      print("In delete_all_assertions.. http error: status: {} .. msg: {}".format(r.status_code, r.text))


def delete_all_badges(bc_list):
  for i in range(len(bc_list)):
    bc_id = bc_list[i]['entityId']
    r = requests.delete(BADGR_BASE_URL + BADGR_BADGECLASS_DELETE_PATH.format(bc_id), headers=get_post_headers())
    if r.status_code >= 200 and r.status_code < 300:
      print("SUCCESS: deleted all badge classes")
    else:
      LOGGER.error("In delete_all_badges.. ERROR: {} .. {}".format(r.status_code, r.text))


# def dumpPrizeAssertions(filtered_descriptions):
#   # print("In dumpPrizeAssertions")
#   # print(json.loads(filtered_descriptions[0]))
#   with open('./prize-assertions.csv', 'a+') as f:
#     for fd in filtered_descriptions:

#     prize_assertion_list = json.loads(filtered_descriptions[0])
#     newpl = []
#     for row in prize_assertion_list:
#       # print(row)
#       line = str(row['timestamp'])+','+row['name']+','+row['email']+','+row['prize']+','+str(row['numEPSpent']+'\n')
#       newpl.append(line)
#     f.writelines(newpl)


def delete_badgeclass_description():
  if not prize_badge:
    LOGGER.info("There are no prize assertions to delete, it seems.")
    return
  prize_badge['description'] = "No Assertions yet"
  all_badgeclasses['result'] = prize_badge
  data = prize_badge
  # print("+++++")
  # print(json.dumps(data))
  # print("BADGE CLASS ID: {}".format(prize_badge_id))
  rep = requests.put("https://badgr.firstcontactcrypto.com/v2/badgeclasses/{}".format(prize_badge_id), headers=get_base_headers(), json=data)
  if not log_if_raised(rep, data):
    LOGGER.info('SUCCESS the prize badgclass has been updated')

# Epiphany
# Course
# 5-amazon-gift-card
# 5-usd-of-bitcoin
# keepkey-hardware-wallet

def my_init():
  cron_dir = '/home/prodatalab/.local/share/cron'
  if not os.path.exists(cron_dir):
    try:
      os.makedirs(cron_dir)
    except FileExistsError:
      pass
  os.chdir(cron_dir)

def toCSVFile(filtered_badges):
  lines = []
  for fb in filtered_badges:
    prizeAssertions = json.loads(fb['description'])

    for pa in prizeAssertions:
      line = str(pa['timestamp']) + "," + pa['name'] + "," + pa['email'] + "," + pa['prize'] + "," + str(pa['numEPSpent']) + '\n'
      # print(type(line))
      lines.append(line)
  return lines
  # print(lines)




if __name__ == '__main__':
  my_init()
  filtered_badges = filter_badgeclasses()
  lines = toCSVFile(filtered_badges)[0]
  f = open('./prize-assertions.csv', 'w')
  for line in lines:
    print(type(line))
    # f.write(line)


  f.flush()
  f.close()
  # f.writelines(lines)
  # f.flush()
  # f.close()
  # dumpPrizeAssertions(lines)
  # delete_badgeclass_description()

