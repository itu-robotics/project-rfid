from server.socket_server import BasicChatServer
import thread
import json
import time
import server.debug as debug
from database.json_database.json_database_operations import PersonObjectManager
from database.json_database.database_struct import Member
import datetime
import mailing.mail as mail
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
    id = data["id"]
    type = data["request_type"]
    content = data["content"]

    if type == "door_clearance":
        person = manager.find(content, "id")

        #print person.serialize()
        has_clearance = False


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
    elif type == "singleuse_door_clearance":
        person = manager.find(content, "id")
        directorate = manager.find_all("2", "level")
        directorate = [x.mail for x in directorate]
        print directorate
        directorate = ["yazicis16@itu.edu.tr", "sencer_yazici98@hotmail.com"]
        mail.login()
        if not mail.mail_for_request("QTR" + id, person, directorate):
            return

        (return_id, req_result) = mail.read_email_from_gmail(directorate, "QTR" + id)
        while req_result is None:
            (return_id, req_result) = mail.read_email_from_gmail(directorate, "QTR" + id)

        _dict = {"id":id, "result":req_result, "status":"OK", "content":person.name}
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
