# We have to import os to access env vars
import os
# We're going to do some things with datetimes, so need that module
import time
import datetime
# Import our debugger so it can help us debug our program
import pdb

# Load our secret pieces of information in from
# our .env file which is not tracked in our
# source control
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Load the twilio SDK
from twilio.rest import TwilioRestClient

# Load the GitHub SDK
from github import Github

################
# TWILIO SECTION
################
# Taken from https://www.twilio.com/docs/quickstart/python/sms/sending-via-rest
# Find these values at https://twilio.com/user/account
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
to_phone_number = os.environ.get("MY_PHONE_NUMBER")
from_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")

twilio_client = TwilioRestClient(account_sid, auth_token)

# Reference the twilio-python docs to figure out how
# to write the send_message function:
# http://twilio-python.readthedocs.io/en/latest/usage/messages.html
def send_message(message):
    return twilio_client.messages.create(to=to_phone_number,
        from_=from_phone_number,
        body=message)

################
# GITHUB SECTION
################
github_username = os.environ.get("GITHUB_USERNAME")
github_password = os.environ.get("GITHUB_PASSWORD")
github_repo_name = os.environ.get("GITHUB_REPO_NAME")

github_client = Github(github_username, github_password)

# This method will need to do three things:
# 1. Fetch the repo object
# 2. Fetch the issues on that repo
# 3. Find the timestamp for the most recently modified issue
# Docs on fetching a repo:
# http://pygithub.readthedocs.io/en/latest/github.html#github.MainClass.Github.get_repo
# Docs on fetching issues from a repo:
# http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_issues
# Docs about the issue object:
# http://pygithub.readthedocs.io/en/latest/github_objects/Issue.html
def get_most_recent_issue_timestamp():
    # Default to Jan 1, 1970
    timestamp = datetime.datetime.fromtimestamp(0)
    repo = github_client.get_repo(github_repo_name)
    issues = repo.get_issues()
    # Look for the maximum updated_at timestamp
    for issue in issues:
        timestamp = max(timestamp, issue.updated_at)

    return timestamp

################
# MAIN SECTION
################
print "Running..."

most_recent_timestamp = get_most_recent_issue_timestamp()

while True:
    fetched_timestamp = get_most_recent_issue_timestamp()
    print "Checking for new or modified issues..."
    if fetched_timestamp > most_recent_timestamp:
        print "Sending alert!"
        most_recent_timestamp = fetched_timestamp
        send_message("Update on issues for " + github_repo_name)
    time.sleep(15)
