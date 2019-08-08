import os
from dotenv import load_dotenv
load_dotenv()


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
outgoing_number = os.getenv("OUTGOING_NUMBER")
mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
