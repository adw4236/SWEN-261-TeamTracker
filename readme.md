# SWEN-261 TeamTracker

This is a NodeJS app that uses the slack API to pull some information about team communication.

## Overview

### app.js

This file is incomplete and just exists as a skeleton for creating and actual web app with an
interface to collect team communication and participation statistics.

### count_messages.js

This file is a script that can be ran to count up messages that team members have sent in any
given channel.

Usage: `node count_messages.js -t <access token> [--from <start date>] [--to <end date>]`

See setup for retrieving an access token (Step 7).

Dates can be formatted in `mm/dd/yyyy`

The dates are passed directly into JavaScripts Date object.  See
[this reference](https://www.w3schools.com/js/js_date_formats.asp)
for more information about formatting.

Example: `node count_messages.js -t xoxp-************-************-************-******************************** --from 11/5/2019 --to 11/25/2019`

## Setup

This project requires [NodeJS](https://nodejs.org/en/) and NPM to run.

Run `npm install` in the projects root directory to install any dependencies.

### Creating a Slack App

In order to actually run this code on a slack workspace, an app must be set up on that workspace.
You must first log into the slack workspace you wish to run this on at least once on the machine you
are using.

Repeat these steps for each team you would like to run this on, this only needs to be done once per
team per semester.

1. Navigate to [The slack API](https://api.slack.com/apps) and create a new app.
2. Name the app anything specific to the semester and team
3. Choose the slack group you wish to add this app to and finish
4. In the apps settings, under features, choose OAuth & Permissions
5. Under the scopes section, add the following scopes
    - users:read
    - channels:history
    - channels:read
	- groups:history
	- groups:read
6. At the top of this page, click "Install App to Workspace" and Allow
7. Record the OAuth Access Token for use in count_messages.js