from pirc522 import RFID
import signal
import time
import request
rdr = RFID()
util = rdr.util()
util.debug = True

print("No Card Detected")

while True:
    if True:
        rdr.wait_for_tag()
        (error, data) = rdr.request()
        if error:
            pass
        else:
            (error, uid) = rdr.anticoll()
            if not error:
                card_uid = "-".join(map(str, uid))
                if card_uid != "":
                    # Action
                    id, result = request.send_request("192.168.2.175", 9090, "door_clearance", card_uid)
                    if result != "":
                        if str(result["id"]) == str(id):
                            if result["result"]:
                                print "[ OK ] Door Opening."
                            else:
                                print "[ DENIED ] Access Denied!"
                    time.sleep(0.5)
