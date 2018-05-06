from pirc522 import RFID
import signal
import time
import request
rdr = RFID()
util = rdr.util()
util.debug = True

print("No Card Detected")
card_uid = ""

while True:
    global card_uid
    card_uid = ""
    for i in range(10):
        rdr.wait_for_tag()
        (error, data) = rdr.request()
        if not error:
            time.sleep(0.1)
            (error, uid) = rdr.anticoll()
            if not error:
                card_uid_new = "-".join(map(str, uid))
                if card_uid != card_uid_new:
    		        # Action
                    card_uid = card_uid_new
                    print(card_uid)
                    #request.send_request("localhost", 9090, "door_clearance", card_uid)
