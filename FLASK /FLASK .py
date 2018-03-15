import os
import time
import requests
import json
import pygame
import datetime
import pygame
from flask import Flask
from flask import request
from phue import Bridge
from datetime import datetime
from TrafficChecker import send_request
from GoogleCalendar import getMeetings


app = Flask(__name__)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.remote_addr
    print(ip)
    timer(ip)
    return('okay')


def timer(ip):
    time.sleep(28800) #8 hours in seconds
    main(ip)

def main(ip):
    pingstatus = check_ping(ip)
    if pingstatus == 'Network Error':
        # print('User offline!')

        # check the time
        # is it late?
        # run motion sensor stuff
        # if it isnt, have they had a busy day?
        # have they tweeted?
        amountOfMeetings = getMeetings()
        now = datetime.datetime.now()
        homeTime = now.replace(hour=17, minute=30, second=0, microsecond=0)
        if homeTime > now:
            stressed_user()
        elif amountOfMeetings > 5:
            stressed_user()
        else:
            '''keywords tweeted'''
            pass
    else:
        print('************ \nTRYING AGAIN \n************')
        time.sleep(15)
        main(ip)


def stressed_user():
    time_until_home = send_request()
    time_seconds = (time_until_home - 5) * 60
    time.sleep(time_seconds)
    check_motion()


def check_ping(ip):
    response = os.system("ping -c 1 " + ip)
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus


def check_motion():
    r = requests.get('http://192.168.0.51/api/2-6pUVqx5SJMC7yXhzdOZGP74U5Ha4jw5i-WGgCV/sensors/6').content
    parsed = json.loads(r.decode())
    if parsed:
        turn_lights_on()
        turn_music_on()
    else:
        time.sleep(5)
        check_motion()

def turn_lights_on():
    b = Bridge('192.168.0.51')
    b.connect()
    b.get_api()
    command = {'hue': 25500, 'on': True}
    b.set_light(3, command)

#
# @app.route("/turn_music_on", methods=["GET"])
def turn_music_on():
    # print('i just turned music on')
    # files = []
    # file_index = 0
    # for filename in os.listdir("/musicplaylist"):
    #     if filename.endswith(".mp3"):
    #         files.append(filename)
    # # files.sort() # do this if you want them in name order
    #
    # pygame.mixer.init()
    # pygame.mixer.music.load(files[file_index])
    # pygame.mixer.music.play(15.0)

    pygame.mixer.init()
    pygame.mixer.music.load('song mp3')
    pygame.mixer.music.play(0)

    return 'music turned on'

@app.route("/turn_music_off", methods=["GET"])
def turn_music_off():
    pygame.mixer.music.stop()
    return 'music turned off'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



