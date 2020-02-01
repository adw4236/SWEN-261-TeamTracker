"""

Usage instructions: Set up a slack app as per the README

Install the following dependencies:
pip install slackclient

Usage:

python slack.py -t <OAuth access token from step 7> [-o <start date>] [-l <end date>]

E.g.
python slack.py -t xoxp-************-************-************-******************************** -o 11/5/2019 -l 11/25/2019

Dates are formatted mm/dd/yyyy, the format can be changed by including a --format parameter
https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior

"""

import argparse
import time
import datetime
import slack

parser = argparse.ArgumentParser(description="Count the number of messages sent by a team member")
parser.add_argument("--token", "-t", help="The access token from your slack app", required=True)
parser.add_argument("--oldest", "-o", help="The date of the earliest message to start counting at")
parser.add_argument("--latest", "-l", help="The date of the latest message to stop counting at")
parser.add_argument("--format", help="The format for date/time strings", default="%m/%d/%Y")
args = parser.parse_args()

client = slack.WebClient(token=args.token)

users = {}
oldest_time = None
if args.oldest:
    oldest_time = int(time.mktime(datetime.datetime.strptime(args.oldest, args.format).timetuple()))
latest_time = None
if args.latest:
    latest_time = int(time.mktime(datetime.datetime.strptime(args.latest, args.format).timetuple()))

response = client.users_list()
for member in response["members"]:
    users[member["id"]] = member["real_name"]

response = client.conversations_list()
for channel in response["channels"]:

    options = {
        "channel": channel["id"],
        "count": 1000
    }
    if oldest_time:
        options["oldest"] = oldest_time
    if latest_time:
        options["latest"] = latest_time

    count = {}
    response = client.channels_history(**options)
    for message in response["messages"]:
        if message["user"] not in count:
            count[message["user"]] = 0
        count[message["user"]] += 1

    print(channel["name"])
    for user in count:
        print("\t", users[user], ": ", count[user], sep="")
