from pirc522 import RFID
import signal
import time

rdr = RFID()
util = rdr.util()
util.debug = True

print("No Card Detected")
rdr.wait_for_tag()

#while True:
(error, data) = rdr.request()
if not error:
    print("Card Detected")
    (error, uid) = rdr.anticoll()
    if not error:
        kart_uid = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])+" "+str(uid[4])
        print(kart_uid)
