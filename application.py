"""Dad joke generator"""
from apscheduler.schedulers.background import BackgroundScheduler
from controllers import handle_response, is_number_valid, send_daily_message
from db import add_to_sub_list, does_number_exist, remove_from_sub_list
from flask import Flask, request
from settings import account_sid, auth_token, outgoing_number
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

client = Client(account_sid, auth_token)


def send():
    send_daily_message(client, outgoing_number)
    print("Daily jokes sent to subscribers")


scheduler = BackgroundScheduler(timezone="UTC", daemon=True)
scheduler.start()

scheduler.add_job(send, trigger="cron", hour="16", minute="00")

application = Flask(__name__)


@application.route("/dad", methods=["GET", "POST"])
def incoming_sms():
    incoming_msg = str(request.values.get("Body", type=str)).strip().lower()
    incoming_number = str(request.values.get("From", type=str))
    resp = MessagingResponse()

    opt_out_keywords = ["stop", "stopall", "unsubscribe", "cancel", "end", "quit"]
    help_keywords = ["help", "info"]

    # only supported for US users. example: '+15551234567'
    if not is_number_valid(incoming_number):
        return ""

    # Twilio handles help keywords
    if incoming_msg in help_keywords:
        return ""

    if incoming_msg == "dad":
        # check if number is already on sub list
        if does_number_exist(incoming_number):
            resp.message("You've already subscribed to daily dad jokes.")
        else:
            add_to_sub_list(incoming_number)
            resp.message(handle_response(incoming_msg))
    elif incoming_msg in opt_out_keywords or incoming_msg == "9":
        # remove from db if number exists
        if does_number_exist(incoming_number):
            remove_from_sub_list(incoming_number)

        # Twilio handles 'stop' commands, so responses won't be sent
        if incoming_msg == "9":
            resp.message(handle_response(incoming_msg))
        else:
            return ""
    else:
        resp.message(handle_response(incoming_msg))

    return str(resp)


@application.route("/call", methods=["GET", "POST"])
def incoming_call():
    """Respond to incoming calls with a brief message"""
    resp = VoiceResponse()
    resp.say(
        "Thanks for calling! Text dad for your daily does of dad jokes!", voice="alice"
    )

    return str(resp)


if __name__ == "__main__":
    application.run(debug=True, use_reloader=False)
