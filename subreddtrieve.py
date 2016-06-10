import praw
import requests
import time
import datetime
import sys
import os

def date_to_timestamp(d):
	"""Date must be in the format dd/mm/yyyy."""
	return int(time.mktime(datetime.datetime.strptime(d, "%d/%m/%Y").timetuple()))

## configurations
_USER_AGENT = "subreddtrieve by /u/dozzinale"
_CLIENT_ID = ""
_CLIENT_SECRET = ""
_GAP_IN_SECS = 60
_REQS_DATA = {'user-agent': 'subreddtrieve by /u/dozzinale'}

## args
if len(sys.argv) != 4:
	exit(1)
subreddit_name = sys.argv[1]
start_date = date_to_timestamp(sys.argv[2])
end_date = date_to_timestamp(sys.argv[3])

## login
## if you specify client_id and client_secret you must register
## an app as a developer in your reddit preferences
r = praw.Reddit(user_agent=_USER_AGENT, client_id=_CLIENT_ID, client_secret=_CLIENT_SECRET)
subreddit = r.get_subreddit(subreddit_name)

## check if the subreddit dir already exists and whether it
## does not exist create it
if not os.path.isdir(subreddit_name):
	os.makedirs(subreddit_name)

all_ids = set()
## retrieve all of the posts in the specified subreddit
for current_ts in range(start_date, end_date, _GAP_IN_SECS):
	submissions = subreddit.search("timestamp:{0}..{1}".format(start_date, end_date), syntax='cloudsearch', limit=1000)
	for submission in submissions:
		url = submission.permalink[:-18]
		if submission.id not in all_ids:
			req_json = requests.get(url + '.json', headers=_REQS_DATA)
			with open('/'.join((subreddit_name, submission.id)) + '.json', 'w') as out_file:
				out_file.write(req_json.text)
			all_ids.add(submission.id)
			time.sleep(1)




