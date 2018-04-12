from flask import Flask
from flask_ask import Ask, statement, question
import requests


app = Flask(__name__)
ask = Ask(app, '/')


@app.route('/')
def homepage():
    return "hi there"

@ask.launch
def start_skill():
    welcome_message = 'Hello, would you like to relax?'

    return question(welcome_message)


@ask.intent("YesIntent")
def share_headlines():
    requests.get('http://4f4b9b9c.ngrok.io ')
    return statement('relaxing you now')


@ask.intent("NoIntent")
def noIntent():
    requests.get('http://4f4b9b9c.ngrok.io ')
    return statement('turning music off')


if __name__ == '__main__':
    app.run(debug=True)

