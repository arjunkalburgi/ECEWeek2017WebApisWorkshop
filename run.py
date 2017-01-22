# We have to import os to access env vars
import os

# Load our secret pieces of information in from
# our .env file which is not tracked in our
# source control
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Load the twilio SDK
from twilio.rest import TwilioRestClient

# Taken from https://www.twilio.com/docs/quickstart/python/sms/sending-via-rest
# Find these values at https://twilio.com/user/account
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
to_phone_number = os.environ.get("MY_PHONE_NUMBER")
from_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to=to_phone_number,
    from_=from_phone_number,
    body="Hello there!")
