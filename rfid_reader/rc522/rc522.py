from pirc522 import RFID
import signal
import time

rdr = RFID()
util = rdr.util()
util.debug = True

print("No Card Detected")
card_uid = ""
while True:
    global card_uid
    rdr.wait_for_tag()
    (error, data) = rdr.request()
    if not error:
        time.sleep(0.1)
        (error, uid) = rdr.anticoll()
        if not error:
            card_uid_new = "-".join(map(str, uid))
            print card_uid_new
            if card_uid != card_uid_new:
		# Action
                card_uid = card_uid_new
                #print(card_uid)
