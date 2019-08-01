import requests
from db import db


def get_dad_joke():
    resp = requests.get('https://icanhazdadjoke.com/',
                        headers={'Accept': 'text/plain'})
    return resp.content.decode('utf-8')


def handle_response(body):
    if body == 'stop':
        return

    handler = {
        'dad': get_dad_joke(),
        'daily': 'Thank you for signing up for your daily dose of dad jokes. '
                 'To opt out at any time, reply 9 or STOP',

        # Twilio's API handles STOP and HELP responses, so these will do
        '9': 'You are unsubscribed from the daily dad jokes. Reply 7 for help',
        '7': 'Dad Jokes:\n\nYou may reply DAD for one random dad joke. If you\'d like to receive an automated dad joke'
             ' once a day, reply DAILY. To stop receiving messages completely, reply STOP'
    }

    return handler.get(body, handler['7'])


def send_daily_message(message_client, outgoing_number):
    joke = get_dad_joke()
    message = f'Daily Dad Joke:\n\n{joke}'

    for sub in db.sub_list.find():
        subscriber_number = sub['number']
        message_client.messages \
            .create(
                body=message,
                from_=outgoing_number,
                to=subscriber_number
            )
