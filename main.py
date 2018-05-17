from server.socket_server import BasicChatServer
import thread
import json
import time
import server.debug as debug
from database.json_database.json_database_operations import PersonObjectManager
from database.json_database.database_struct import Member
import datetime
from response.ubidots.send_main import send_request
from response.ubidots.receive_main import get_var as receive_request


manager = None

def load_members(path="object.pkl"):
    global manager
    list = []
    manager = PersonObjectManager(list)
    manager.load()


def mes(client, message):
    global manager
    debug.INFO("Socket: " + str(client) + " Message is: " + str(message))

    # Load Json Data
    data = None
    try:
        data = json.loads(message)
    except ValueError, e:
        return

    type = data["request_type"]
    if type == "idle":
        return

    id = data["id"]
    content = data["content"]

    if type == "door_clearance":
        person = manager.find(content, "id")

        #print person.serialize()
        has_clearance = False

        print "123"
        _dict = {"id":id, "result":has_clearance}

        if person is None:
            _dict["status"] = "ERROR"
            _dict["content"] = "User Not Found"
        else:
            _dict["status"] = "OK"
            _dict["content"] = str(person.name)
            has_clearance = int(person.level) <= 3
            _dict["result"] = has_clearance

        json_str = json.dumps(_dict)
        client.send(json_str + "\n")

    elif type == "door_clearance_request":
        person = manager.find(content, "id")
        send_request(id, str(person.name), str(person.id), str(person.rfid))
        print "[ INFO ] Request Sent."
        data = None
        is_request_success = False
        while not is_request_success:
            temp = receive_request()
            if not temp is None:
                print temp
                if temp["id"] == id:
                    is_request_success = True
                    data = temp
                    break
        clearance = data["clearance"]

        _dict = {"id":id, "result":clearance, "content":str(person.name)}
        json_str = json.dumps(_dict)
        client.send(json_str + "\n")
    file = open("database/request_log.log", 'a')
    file.write(datetime.datetime.now().isoformat() + " > [ " + json.dumps(data) + ", " + json_str + " ]\n")
    file.close()

def main():
    global manager
    load_members()
    server = BasicChatServer(mes)
    thread.start_new_thread(server.run,())
    # send_to_client(server)
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
