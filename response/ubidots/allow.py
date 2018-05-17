import time
import requests
import math
import random
import sys

DEBUG = False
TOKEN = "A1E-BXteMpvKgoLgsq4eVwz1SWOnwsy2jd"  # Put your TOKEN here
DEVICE_LABEL = "rfid-door"  # Put your device label here
count = 0

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ ERROR ] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[ INFO ] request made properly, your device is updated")
    return True

def send_request(id, stat):
    data = {"id":id, "clearance":stat}
    payload = {"active_response": {"value":0, "context": data}}
    print("[ INFO ] Attemping to send data")
    post_request(payload)
    print("[ INFO ] finished")

send_request(sys.argv[1], sys.argv[2] == "True")
