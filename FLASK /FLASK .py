from flask import Flask
from flask import jsonify
from flask import request
from phue import Bridge
from datetime import datetime
from datetime import timedelta
from TrafficChecker import send_request
import os
import time
import requests
import json
import pygame


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.remote_addr
    # print(ip)
    return jsonify({'ip': request.remote_addr}), 200, main(ip)


def main(ip):
    pingstatus = check_ping(ip)
    if pingstatus == 'Network Error':
        # print('User offline!')
        time_until_home = send_request()
        time_seconds = (time_until_home - 5) * 60
        time.sleep(time_seconds)
        check_motion()

    else:
        print('************ \nTRYING AGAIN \n************')
        time.sleep(15)
        main(ip)



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


@app.route("/turn_music_on", methods=["GET"])
def turn_music_on():
    print('i just turned music on')


@app.route("/turn_music_off", methods=["GET"])
def turn_music_off():
    pygame.mixer.music.stop()


if __name__ == '__main__':
    app.run(host='0.0.0.0')



