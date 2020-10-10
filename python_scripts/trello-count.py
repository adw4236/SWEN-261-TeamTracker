"""

Usage instructions:

Install the following dependencies:
pip install matplotlib
pip install requests

1. Log into Trello
2. Navigate to https://trello.com/app-key
3. The key you are presented is the "key" argument
4. Click on "Token" to generate a token
5. The token you are presented is the "token" argument
6. Run the following command to view a graph

python trello.py -k <key from step 3> -t <token from step 5> -b <name of the board> [--team <team name>] [-o <start date>] [-l <end date>]

E.g.
python trello.py -k ******************************** -t **************************************************************** -b "2191-swen-261-06-d-shadow" -o 11/5/2019 -l 11/25/2019

Dates are formatted mm/dd/yyyy, the format can be changed by including a --format parameter
https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior

Reference: https://developers.trello.com/reference

"""

import argparse
import datetime
import requests
import matplotlib.pyplot as plot

parser = argparse.ArgumentParser(description="Count the number of messages sent by a team member")
parser.add_argument("--key", "-k", help="The api key from your trello account", required=True)
parser.add_argument("--token", "-t", help="The access token generated from your trello account", required=True)
parser.add_argument("--board", "-b", help="The name of the board to show statistics for", required=True)
parser.add_argument("--team", help="The name of the team that the board exists in")
parser.add_argument("--oldest", "-o", help="The date of the earliest message to start counting at")
parser.add_argument("--latest", "-l", help="The date of the latest message to stop counting at")
parser.add_argument("--increment", "-i", help="The amount of time activity will be grouped in (hours)", default="24")
parser.add_argument("--format", help="The format for date/time strings", default="%m/%d/%Y")
args = parser.parse_args()

oldest_time = None
if args.oldest:
    oldest_time = datetime.datetime.strptime(args.oldest, args.format)
latest_time = None
if args.latest:
    latest_time = datetime.datetime.strptime(args.latest, args.format)
time_delta = datetime.timedelta(hours=int(args.increment))

team = ""
if args.team:
    response = requests.get(url="https://api.trello.com/1/members/me", params={"key": args.key, "token": args.token})
    for organizationId in response.json()["idOrganizations"]:
        organizaiton = requests.get(url="https://api.trello.com/1/organizations/" + organizationId, params={"key": args.key, "token": args.token})
        if organizaiton.json()["displayName"] == args.team:
            team = organizationId

response = requests.get(url="https://api.trello.com/1/members/me/boards", params={"key": args.key, "token": args.token})
board_id = ""
for board in response.json():
    if team and board["idOrganization"] != team:
        continue
    if board["name"] == args.board:
        board_id = board["id"]
if not board_id:
    print("Cannot find board " + args.board)
    exit()

messages = {}
first = datetime.datetime.now()

options = {
    "key": args.key,
    "token": args.token,
    "limit": 1000
}
if oldest_time:
    options["since"] = oldest_time.isoformat()
if latest_time:
    options["before"] = latest_time.isoformat()

response = requests.get(url="https://api.trello.com/1/boards/" + board_id + "/actions", params=options)
for action in response.json():
    # Note: this datetime is in UTC while the arguments would be local, possibly with daylight savings
    user = action["memberCreator"]["fullName"]
    if user not in messages:
        messages[user] = []

    time = datetime.datetime.strptime(action["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    messages[user] += [time]
    if time < first:
        first = time

if not oldest_time:
    oldest_time = first
if not latest_time:
    latest_time = datetime.datetime.now()

increments = []
time = oldest_time
while time < latest_time:
    increments += [time]
    time += time_delta

total = 0
for user in messages:
    total += len(messages[user])
    print(user, ": ", len(messages[user]), sep="")

    messages[user].sort()
    activity = [ 0 for _ in range(len(increments)) ]
    message_index = 0
    for chart_index in range(len(increments)):
        increment = increments[chart_index]
        while message_index < len(messages[user]) and messages[user][message_index] < increment + time_delta:
            activity[chart_index] += 1
            message_index += 1

    plot.plot(increments, activity, label=user)

if total == 1000:
    print("\nMaximum total contributions reached (1000) consider providing a oldest and latest date")
else:
    print("\nTotal Contributions:", total)

plot.legend()
plot.xticks(increments, rotation="vertical")
plot.margins(0)
plot.subplots_adjust(bottom=0.2)
plot.show()
