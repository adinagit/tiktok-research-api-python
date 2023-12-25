# tiktok-research-api-python
A simple Python wrapper for querying video & user data with [TikTok's Research API](https://developers.tiktok.com/products/research-api/).

To use this code, you must first apply for and receive access to the Research API. 

# Querying Video Data
**For more general info, consult [TikTok's Research API Reference for querying videos](https://developers.tiktok.com/doc/research-api-specs-query-videos/).**

Script: `tiktok-video-hash-data.py`

This script is set up to query all videos with a given hashtag and write the data to a file in JSON format. The data includes all fields offered by TikTok.

It is easy to change/customize the query itself on `line 57`.

For the script to run, you must insert your **CLIENT KEY** and **CLIENT SECRET** in the `get_access_token` function on lines `29` and  `30` respectively. 

The script takes the following arguments: 
1. HASHTAG: the hashtag you want to search for
2. START DATE: start date of the query
3. END DATE: end date of the query (*Note: must be no more than 30 days after the START DATE)
4. OUTPUT FILE NAME/PATH: where you want the data to be saved (should be a `.json` file)
5. [optional] SEARCH ID: field associated with the API for if you are continuing a search; you must look into the data you already have to figure out what the value should be
6. [optional] CURSOR: same as in (5); to pick up where you left off, look for the final cursor returned

## Things to note 
* Access tokens are good for 2 hours, but the script is set up to generate a new one every hour. In my experience so far, rate limits run out far before an hour is up.
* The code will keep running even if a specific query failed.
* The code will run until either (a) the rate limit is reached or (b) there is no more data to be returned.

## Example
Here's what it would look like to _start_ a search for all videos with #TikTok between 10/12/2022 and 10/20/2022, and save it to `/tiktok-data/#tiktok.json`: 
<br>
`python3 tiktok-video-hash-data.py tiktok 20221012 20221020 /tiktok-data/#tiktok.json`

Now, let's say we want to continue that search. We would look in `/tiktok-data/#tiktok.json` and find that the `SEARCH_ID` = 12345 and the final `CURSOR` = 500. Then, we would run:
<br>
`python3 tiktok-video-hash-data.py tiktok 20221012 20221020 /tiktok-data/#tiktok.json 12345 500`

# Querying User Data
**For more general info, consult [TikTok's Research API Reference for querying users](https://developers.tiktok.com/doc/research-api-specs-query-user-info/).**

## Version 1: Search for List of Users
Script: `tiktok-user-list-data.py`

This script is set up to query user data from a list of usernames stored in a separate `.txt` file and write the output to a file in JSON format. The data includes all fields offered by TikTok.

For the script to run, you must insert your **CLIENT KEY** and **CLIENT SECRET** in the `get_access_token` function on lines `27` and  `28` respectively. 

The script takes the following arguments: 
1. INPUT USER LIST: path to the `.txt` file with the list of usernames to search for, written on separate lines. You can find a toy example in `user-list-example.txt`
2. OUTPUT FILE: where you want the data to be saved (should be a `.json` file)

### Things to note 
* If a query fails for some reason, the script will keep running.
* The API rate limit is 1000 user requests/day, so the script will stop running after 1000 queries even if the input list has >1000 usernames. In that case, it will print the username where the search left off. If the input list has <=1000 usernames, the script will stop running after querying the full list. 

### Example 
Here's what it would look like to search for users stored in `user-list.txt` and save it to `/tiktok-data/users.json`: 
<br>
`python3 tiktok-user-list-data.py user-list.txt /tiktok-data/users.json`

## Version 2: Search for Single User
Script: `tiktok-user-data.py`

This script is set up to query user data for a singular user and write the output to a file in JSON format. The data includes all fields offered by TikTok.

For the script to run, you must insert your **CLIENT KEY** and **CLIENT SECRET** in the `get_access_token` function on lines `20` and  `21` respectively. 

The script takes the following arguments: 
1. USERNAME: the username to search for (*Note: I'm not sure if usernames can include spaces.. if that's the case, this script probably needs to be tweaked!)
2. OUTPUT FILE: where you want the data to be saved (should be a .json file)

### Example 
Here's what it would look like to search for data on `tiktok-user-1` and save it to `/tiktok-data/users.json`: 
<br>
`python3 tiktok-user-data.py tiktok-user-1 /tiktok-data/users.json`
