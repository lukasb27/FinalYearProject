from flask import Flask
import vlc

app = Flask(__name__)


@app.route('/')
def homepage():
    return "hi there"

@app.route('/hello')
def hello():
    p = vlc.MediaPlayer("Applause.mp3")
    p.play()
    return "Thanks, you have just played an annoying sound clip on my laptop."


if __name__ == '__main__':
    app.run(debug=True)