import requests
import random
import time

DEBUG = False
TOKEN = "A1E-BXteMpvKgoLgsq4eVwz1SWOnwsy2jd" # Assign your Ubidots Token
DEVICE = "rfid-door" # Assign the device label to obtain the variable
VARIABLE = "active_response" # Assign the variable label to obtain the variable value
DELAY = 1  # Delay in seconds

def get_var():
    global DEVICE, VARIABLE
    try:
        url = "http://things.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(DEVICE, VARIABLE)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['context']
    except:
        return None
        pass


if DEBUG:
    while True:
        print(get_var(DEVICE, VARIABLE))
        time.sleep(DELAY)
