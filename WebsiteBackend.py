# from flask import Flask
# import vlc
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def homepage():
#     return "hi there"
#
# @app.route('/hello')
# def hello():
#     p = vlc.MediaPlayer("Applause.mp3")
#     p.play()
#     return "Thanks, you have just played an annoying sound clip on my laptop."
#
#
# if __name__ == '__main__':
#     app.run(debug=True)




import socket


def Main():
    host = '127.0.0.1'
    port = 5001

    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = input(" -> ")

    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print('Received from server: ' + data)

        message = input(" -> ")

    mySocket.close()


if __name__ == '__main__':
    Main()