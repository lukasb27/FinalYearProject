from flask import Flask
from flask_ask import Ask, statement, question, session
from phue import Bridge
import requests


app = Flask(__name__)
ask = Ask(app, '/')


@app.route('/')
def homepage():
    return "hi there"

@ask.launch
def start_skill():
    welcome_message = 'Are you sure you want to start a disco?'
    return question(welcome_message)


@ask.intent("YesIntent")
def share_headlines():
    b = Bridge('192.168.0.51')
    b.connect().get_api()
    # print(b.get_light(3, 'on'))
    command = {'effect': 'colorloop'}
    b.set_light(3, command)
    party = 'lets get this party started'

    return statement(party)


@ask.intent("StopIntent")
def no_intent():
    b = Bridge('192.168.0.51')
    b.connect()
    b.get_api()
    command = {'effect': 'none'}
    b.set_light(3, command)
    stop_party = 'okay'
    requests.get('http://linktoendmusichere')
    return statement(stop_party)

@ask.intent("PauseIntent")
def
if __name__ == '__main__':
    app.run(debug=True)

