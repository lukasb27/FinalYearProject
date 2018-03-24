import datetime
import json
import os
import time
import pygame
import random
import requests
from datetime import datetime
from TrafficChecker import send_request
from TwitterScraper import get_tweets
from GoogleCalendar import getMeetings
from os import listdir
from flask import Flask
from flask import request
from phue import Bridge


app = Flask(__name__)

# Defines the api endpoint to get the users IP address
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.remote_addr # Users IP address
    print(ip)
    timer(ip)
    return('okay')

def timer(ip):
    time.sleep(28800) #8 hours in seconds (Average work day)
    main(ip)

def main(ip):
    pingstatus = check_ping(ip)
    # Ping the IP address until we no longer get a response, which means they have left the office.
    if pingstatus == 'Network Error':

        # check the time
        # is it late?
        # run motion sensor modules
        # if it isnt, have they had a busy day?
        # have they tweeted?

        amountOfMeetings = getMeetings() #Runs the getMeetings function from GoogleCalendar
        now = datetime.datetime.now()
        homeTime = now.replace(hour=17, minute=35, second=0, microsecond=0)

        # Check the requirements for a stressed user
        if homeTime > now: # Check if the user has left later than normal, which is defined in line 45 as 17:30
            stressed_user()
        elif amountOfMeetings > 5: # Is the amount of meetings higher than 5?
            stressed_user()
        elif get_tweets(): # Check has the user tweeted any of the keywords defined in TwitterScraper
            stressed_user()
            pass
    else:
        # If you get a response, try again in 15 seconds (will keep trying until no response is gained)
        print('************ \nTRYING AGAIN \n************')
        time.sleep(15)
        main(ip)


def stressed_user():
    time_until_home = send_request() #Calculate the users time home
    # Convert to seconds, but start checking for motion 5 mins earlier
    # This is in case the user gets home earlier than normal (but has still left work late)
    time_seconds = (time_until_home - 5) * 60
    time.sleep(time_seconds)
    check_motion() #start checking whether there is motion, I.E the user is home


# Translates the response from the ping into variables
def check_ping(ip):
    response = os.system("ping -c 1 " + ip)
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus

# Checks whether there is motion detected on the motion sensor and follows appropriate actions
def check_motion():
    # Hit the motion sensor api for motion
    r = requests.get('http://192.168.0.51/api/2-6pUVqx5SJMC7yXhzdOZGP74U5Ha4jw5i-WGgCV/sensors/6').content
    parsed = json.loads(r.decode())  # Decode the JSON response and create a True or False variable
    if parsed:  # If motion is true, start to play music and turn the lights to relaxing colours
        relax()
    else:   # If motion is false, wait 5 seconds and start checking for motion again.
        time.sleep(5)
        check_motion()


# Turn the lights on by connecting to the Phillips Hue Bridge, and sending an API request to the specific light.
def turn_lights_on():
    b = Bridge('192.168.0.51')
    b.connect()
    b.get_api()
    command = {'hue': 25500, 'on': True}
    b.set_light(3, command)


# Start turning music on and relaxing user
def turn_music_on():
    # Insert code, try not to cry
    pass

# A function to allow communications with Alexa, it will turn the music off if a request is set to /turn_music_off
@app.route("/turn_music_off", methods=["GET"])
def turn_music_off():
    pygame.mixer.music.stop()
    return 'music turned off'

# A function to start relaxing the user when they get home, this is contained in one function to allow easy Alexa
# communications via the end point /relax.
@app.route("/relax", methods=["GET"])
def relax():
    turn_music_on()
    turn_lights_on()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



