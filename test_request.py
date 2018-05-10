import socket
import json
import random, string
import time
import sys
host = "0.0.0.0"
port = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
_dict = {"id":id, "request_type":"singleuse_door_clearance", "content":sys.argv[1]}

client.send(json.dumps(_dict))
print "SENDING " + json.dumps(_dict)
print "RECEIVED " + client.recv(100).split("\n")[0]
client.close()
