################
# IMPORTS
################
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

# This method will need to take a message argument, and send that
# message to the correct phone number, from our twilio phone number.
# Docs on sending a message with the twilio client:
# http://twilio-python.readthedocs.io/en/latest/usage/messages.html
def send_message(text):
    #>>>>>>>>>>> YOUR CODE STARTS HERE
	message = twilio_client.messages.create(
	    body=text,
	    to=to_phone_number,
	    from_=from_phone_number,
	)
	print message.sid
    #<<<<<<<<<<< YOUR CODE ENDS HERE

# send_message("Sent from your Twilio trial account - Hello there!")

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
    #>>>>>>>>>>> YOUR CODE STARTS HERE
    repo = github_client.get_repo(github_repo_name)
    issues = repo.get_issues(sort="updated")
    # print(issues[0])
    return issues[0].updated_at
    #<<<<<<<<<<< YOUR CODE ENDS HERE

################
# MAIN SECTION
################
print "Running..."

most_recent_timestamp = get_most_recent_issue_timestamp()
while True:
    #>>>>>>>>>>> YOUR CODE STARTS HERE
    if most_recent_timestamp < get_most_recent_issue_timestamp(): 
    	send_message("You just got a new issue on " + github_repo_name + "!\n\nCheck on it here: https://github.com/" + github_repo_name + "/issues ")
    time.sleep(30)
    #<<<<<<<<<<< YOUR CODE ENDS HERE
