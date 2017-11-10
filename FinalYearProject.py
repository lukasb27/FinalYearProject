from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import json
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, '/redditreader')

def get_headlines():
    user_pass_dict = {'user': 'lilywhitelukas',
                      'passwd': '',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
    sess.post('https://www.reddit.com/api/login', data= user_pass_dict)
    time.sleep(0.5)
    url = 'https://reddit.com/r/coys/.json?limit=3'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '...'.join(i for i in titles)
    return titles


@app.route('/')
def homepage():
    return "hi there"

@ask.launch
def start_skill():
    welcome_message = 'I think hes a useless cunt. Hes a ginger, pube head little fuck boy. Alexa Stop He is from Derby, he is not a yorkshire man. He is a posh midlands accent. He is shit at league of legends, in fact he is shit at every game he has ever played. He also suports Sheffield Wednesday and Arsenal, probably.'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'the current tottenham news is {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'fuck off you fucking cunt, i fucking hate you. '
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)