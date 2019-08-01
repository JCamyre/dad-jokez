"""Dad joke generator"""
import os
from db import does_number_exist, add_to_sub_list, remove_from_sub_list
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from controllers import handle_response, send_daily_message
from apscheduler.schedulers.background import BackgroundScheduler
from settings import auth_token, outgoing_number, account_sid

client = Client(account_sid, auth_token)


def send():
    send_daily_message(client, outgoing_number)
    print('Daily jokes sent to subscribers')


scheduler = BackgroundScheduler(timezone='utc', daemon=True)
scheduler.add_job(send, trigger='cron', hour='16', minute='00')
scheduler.start()


application = Flask(__name__)


@application.route('/dad', methods=['GET', 'POST'])
def incoming_sms():
    body = str(request.values.get('Body', type=str)).strip().lower()
    incoming_number = str(request.values.get('From', type=str))

    # only supported for US users '+15551234567'
    if len(incoming_number) != 12 and incoming_number[:2] != '+1':
        return

    if body == 'daily' and does_number_exist(incoming_number) is False:
        # add to db
        add_to_sub_list(incoming_number)
    elif (body == 'stop' or body == '9') and does_number_exist(incoming_number) is True:
        # remove from db
        remove_from_sub_list(incoming_number)

    # send nothing on STOP
    if body == 'stop':
        return

    resp = MessagingResponse()
    resp.message(handle_response(body))

    return str(resp)


if __name__ == "__main__":
    application.run(debug=True, use_reloader=False)
