import requests
import bs4
import math
import json
import re
from twilio.rest import Client
from keys import *


def main():
    twilioCli = Client(accountSID, authToken)
    warnings_list = []
    grouped_warnings = []
    traffic_report = []

    response = requests.get(
        'http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=OX75NR&wp.1=S14TJ&avoid=minimizeTolls&key=MeG3LZS'
        + 'XpGIxVRJgbYAo~1hPHwHTUWQRN5tDvlDqelg~Aq3GKZpkh6ZmOCy3Zwm_8BqWRwEePyz6mbFzcGpxbABBPHP49bbKBsDKulkBvrgB')
    sample = response.content
    soup = bs4.BeautifulSoup(sample, "html5lib")

    traffic_time = soup.select('route traveldurationtraffic')
    normal_time = soup.select('travelduration')
    warnings = soup.select('warning')

    strip_normal = ''.join(normal_time[0])
    int_normal = math.ceil(int(strip_normal) / 60)

    strip_traffic = ''.join(traffic_time[0])
    int_traffic = math.ceil(int(strip_traffic) / 60)

    for i in warnings:
        warnings_list.extend((i['severity'], i['origin'], i['warningtype']))

    for i in range(0, len(warnings_list), 3):
        grouped_warnings.append((warnings_list[i:i + 3]))

    for i in grouped_warnings:
        something = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + i[
            1] + '&key=AIzaSyA2TMFAQryqMs9Wdk95q0qTEGAZ_P0QzrU').content
        parsed = json.loads(something.decode())
        location = parsed['results'][0]['address_components'][0]['short_name'] + ' ' + \
                   parsed['results'][0]['address_components'][1]['short_name']
        i[1] = location

    for i in grouped_warnings:
        for item in i:
            if item == 'Moderate':
                traffic_list = re.findall('[A-Z][^A-Z]*', i[2])
                joint_reason = ''.join(' on the' + ' ' + i[1] + ' is the cause of traffic')
                traffic_list = ' '.join(traffic_list)
                joint_list = traffic_list + joint_reason
                traffic_report.append(joint_list)

    if int_traffic > int_normal:
        division = str(math.ceil(((int_traffic - int_normal) / int_traffic) * 100))
        # if division >= 19:
        if True:
            # print('Your quickest route is ' + division + ' minutes late, this is because of ' + traffic_report[0] +
            #  '. I\'d suggest going a different way.')
            textContent = 'Your quickest route home is delayed by ' + division + ' minutes. ' + traffic_report[
                0] + '. I\'d suggest going a different way.'
            message = twilioCli.messages.create(body=textContent, from_=myTwilioNumber, to=myCellPhone)


main()
