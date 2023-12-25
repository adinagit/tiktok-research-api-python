import requests
import json
import sys

"""
GET PARAMETERS
---
(1) username to search for
(2) output file - should be .json
"""

USER = str(sys.argv[1])
OUTPUT_F = str(sys.argv[2])

"""
GET ACCESS TOKEN, DETERMINE FIELDS
"""

def get_access_token():
    CLIENT_KEY = "PUT YOUR CLIENT KEY HERE" ## substitute with your client key
    CLIENT_SECRET = "PUR YOU SECRET KEY HERE"  ## substitute with your secret key
    r = requests.post('https://open.tiktokapis.com/v2/oauth/token/',
                      headers={'Content-Type': 'application/x-www-form-urlencoded',
                           'Cache-Control': 'no-cache'
                      },
                      data={'client_key':CLIENT_KEY,
                           'client_secret':CLIENT_SECRET,
                           'grant_type':'client_credentials'})
    ACCESS_TOKEN = r.json()['access_token']
    return ACCESS_TOKEN

ACCESS_TOKEN = get_access_token()

ALL_FIELDS = 'display_name,bio_description,avatar_url,is_verified,follower_count,\
following_count,likes_count,video_count'

"""
COLLECT DATA & SAVE OUTPUT
"""

D = requests.post('https://open.tiktokapis.com/v2/research/user/info/?fields=%s'%ALL_FIELDS,
                            headers = {'authorization':'bearer '+ACCESS_TOKEN},
                            data = {'username':USER})

DATA_LIST = [D.json()]
with open(OUTPUT_F, 'w') as f:
    json.dump(DATA_LIST, f, indent=2)
