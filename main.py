from server.socket_server import BasicChatServer
import database.python_database.object_xml_operations as o2x
import thread
import json
import time
import server.debug as debug

database_path = "/database/database.xml"

class TCPParser(object):
    """Doc"""

    dispatch = {
        'add_member': o2x.add_member
        # TODO: Add all functions
    }


def mes(client, message):
    # Message will be sent to TCPParser
    # To check with dispatcher and execute function.
    # FIXME: Each function has differrent attributes, Cant execute them together.

    # TODO: Execute Authentication Test here. Check is user allowed
    # IDEA: Different user types to execute group of functions. Allow some users to execute some etc. remove_member
    debug.INFO("Socket: " + str(client) + " Message is: " + str(message))
    data = None
    try:
        data = json.loads(message)
    except ValueError, e:
        return
    id = data["id"]
    type = data["request_type"]
    content = data["content"]

    if type == "door_clearance":
        level = o2x.get_level(content, "rfid", "database/python_database/database.xml")
        has_clearance = False
        found = level != -1

        if found:
            has_clearance = level <= 3

        _dict = {"id":id, "result":has_clearance}

        if not found:
            _dict["status"] = "ERROR"
        else:
            _dict["status"] = "OK"

        json_str = json.dumps(_dict)
        send_to_client(client, json_str)
    file = open("request_log.txt", 'a')
    file.write(json.dumps(data) + "\n")
    file.close()

def send_to_client(client, message):
    client.send(message + "\n")
    debug.INFO("Sending Back: " + message)


def main():
    server = BasicChatServer(mes)
    thread.start_new_thread(server.run,())
    # send_to_client(server)
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
