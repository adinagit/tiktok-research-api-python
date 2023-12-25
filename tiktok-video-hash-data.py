import requests
import json
import time
import sys

"""
GET PARAMETERS
---
(1) hashtag
(2) start date
(3) end date
(4) output file
(5) [optional] search id
(6) [optional] cursor
"""
HASH_SEARCH = str(sys.argv[1])
START_DATE = str(sys.argv[2])
END_DATE = str(sys.argv[3])
DATA_FILE = str(sys.argv[4])
if len(sys.argv) > 5: # if picking up from a past search...
    SEARCH_ID = str(sys.argv[5])
    CURSOR = int(sys.argv[6])

"""
FUNCTION TO GET ACCESS TOKEN
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

"""
START DATA COLLECTION
"""

T = time.process_time() # get new access token every hour (good for 2 hours)

ALL_FIELDS = 'id,video_description,create_time, region_code,share_count,view_count,like_count,\
comment_count, music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text'

ACCESS_TOKEN = get_access_token()

"""
QUERY: all videos with hashtags provided in argument list
..feel free to customize!
"""

QUERY = {
    'and':[{
    'operation':'EQ',
    'field_name':'hashtag_name',
    'field_values':[HASH_SEARCH]
    }]
}

"""
MAKE INITIAL QUERY
"""

if len(sys.argv) > 5: # picking up from a past search
    D = requests.post('https://open.tiktokapis.com/v2/research/video/query/?fields=%s'%ALL_FIELDS,
                            headers = {'authorization':'bearer '+ACCESS_TOKEN},
                            data = {'query':json.dumps(QUERY),
                                   'start_date':START_DATE,
                                   'end_date':END_DATE,
                                   'max_count':100,
                                   'cursor':CURSOR,
                                   'search_id':SEARCH_ID}
    )
else: # not picking up from a past search
    D = requests.post('https://open.tiktokapis.com/v2/research/video/query/?fields=%s'%ALL_FIELDS,
                            headers = {'authorization':'bearer '+ACCESS_TOKEN},
                            data = {'query':json.dumps(QUERY),
                                   'start_date':START_DATE,
                                   'end_date':END_DATE,
                                   'max_count':100}
    )

    SEARCH_ID = D.json()['data']['search_id']

CURSOR = D.json()['data']['cursor']
DATA_LIST = [D.json()]

"""
MAKE UP TO A TOTAL OF 1000 REQUESTS
(stop if/when there's no more data)
"""

i = 0
if not D.json()['data']['has_more']: # if no more data, cut to end of script
    i == 1000

while i < 999:

    # update access token every hour
    ELAPSED = time.process_time() - T
    ELAPSED_HOURS = time.gmtime(ELAPSED).tm_hour
    if ELAPSED_HOURS > 0:
        ACCESS_TOKEN = get_access_token()
        T = time.process_time()

    try:
        D = requests.post('https://open.tiktokapis.com/v2/research/video/query/?fields=%s'%ALL_FIELDS,
                            headers = {'authorization':'bearer '+ACCESS_TOKEN},
                            data = {'query':json.dumps(QUERY),
                                   'start_date':START_DATE,
                                   'end_date':END_DATE,
                                   'max_count':100,
                                   'cursor':CURSOR,
                                   'search_id':SEARCH_ID}
        )

        DATA_LIST.append(D.json())

        i += 1
        CURSOR = D.json()['data']['cursor']

        if not D.json()['data']['has_more']:
            break

    except Exception as e: # just in case! sometimes things happen!
        i += 1
        continue

"""
WRITE DATA TO FILE
"""

with open(DATA_FILE, 'w') as f:
    json.dump(DATA_LIST, f, indent=2)
