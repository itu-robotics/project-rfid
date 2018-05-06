import socket
import json
import random, string
import time

def send_request(host, port, type, content):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    _dict = {"id":id, "request_type":type, "content":content}

    client.send(json.dumps(_dict))
    received = client.recv(100).split("\n")[0]
    print "[ SENDING ] " + json.dumps(_dict)
    print "[ RECEIVED ] " + received
    data = json.loads(received)
    client.close()
    return id, data
