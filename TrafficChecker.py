import requests
import bs4
import math
import json
import re
from twilio.rest import Client
from keys import *


# Get the traffic and directions from address A  to address B. Parse the content using Beautiful
# Soup, extract traffic data, and normal route data.
def send_request():
    # GET request to bing API
    sample = requests.get(
        'http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=' + postcode_one +'&wp.1=' + postcode_two +
        '&avoid=minimizeTolls&key=MeG3LZS'
        + 'XpGIxVRJgbYAo~1hPHwHTUWQRN5tDvlDqelg~Aq3GKZpkh6ZmOCy3Zwm_8BqWRwEePyz6mbFzcGpxbABBPHP49bbKBsDKulkBvrgB').content
    soup = bs4.BeautifulSoup(sample, "html5lib")

    # Get the elements
    traffic_time = soup.select('route traveldurationtraffic')
    normal_time = soup.select('travelduration')
    warnings = soup.select('warning')

    # Bing gives native time as seconds, turn it into minutes.
    strip_normal = ''.join(normal_time[0])
    int_normal = math.ceil(int(strip_normal) / 60)

    strip_traffic = ''.join(traffic_time[0])
    int_traffic = math.ceil(int(strip_traffic) / 60)

    int_traffic, int_normal, traffic_report = severity_warning(warnings, int_normal, int_traffic)
    send_text(int_traffic, int_normal, traffic_report)


# Manipulate the lists and strings to form appropriate traffic report. Give the severity warning.
def severity_warning(warnings, int_normal, int_traffic):

    # Create empty lists for list manipulation.
    grouped_warnings = []
    traffic_report = []
    warnings_list = []

    # Extract data that we want from Bing XML.
    [warnings_list.extend((i['severity'], i['origin'], i['warningtype'])) for i in warnings]

    # Create lists with the necessary data, format [['a', 'b', 'c'] ['x', 'y', 'z'] for different traffic data.
    [grouped_warnings.append((warnings_list[i:i + 3])) for i in range(0, len(warnings_list), 3)]

    # GET request to google maps API, in order to convert coordinates to road names / town names.
    for i in grouped_warnings:
        something = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + i[
            1] + '&key=AIzaSyA2TMFAQryqMs9Wdk95q0qTEGAZ_P0QzrU').content
        parsed = json.loads(something.decode())
        location = parsed['results'][0]['address_components'][0]['short_name'] + ' ' + \
                   parsed['results'][0]['address_components'][1]['short_name']
        i[1] = location

    # Split the cause of traffic from TrafficFlow to Traffic Flow. If there is a moderate / major it will find that,
    # and then join the traffic report with the road name, make
    # a coherent sentence to be sent in the text message.
    for i in grouped_warnings:
        for item in i:
            # Traffic types are LowImpact Minor Moderate Serious
            if item == 'Major' or item == 'Moderate' or item == 'Minor':
                traffic_list = re.findall('[A-Z][^A-Z]*', i[2])
                joint_reason = ''.join(' on the' + ' ' + i[1] + ' is the cause of traffic')
                traffic_list = ' '.join(traffic_list)
                joint_list = traffic_list + joint_reason
                traffic_report.append(joint_list)

    return int_traffic, int_normal, traffic_report


# Does a bit of maths then sends the final text message.
def send_text(int_traffic, int_normal, traffic_report):

        # Do a bit of Maths, working out the difference between normal route time and the route time with traffic.
        twilioCli = Client(accountSID, authToken)
        if int_traffic > int_normal:
            division = str(math.ceil(((int_traffic - int_normal) / int_traffic) * 100))
            if int(division) >= 50:
            # Send the text message using Twilio to the client phone number.
                text_content = 'Your normal route home is delayed by ' + division + ' minutes. ' + traffic_report[
                    0] + '. I\'d suggest going a different way.'
                twilioCli.messages.create(body=text_content, from_=myTwilioNumber, to=myCellPhone)


send_request()
