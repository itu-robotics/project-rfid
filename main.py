from server.socket_server import BasicChatServer
import database.python_database.object_xml_operations as o2x

database_path = "/database/database.xml"

class TCPParser(object):
    """Doc"""

    dispatch = {
        'add_member': o2x.add_member
        # TODO: Add all functions
    }


def mes(message):
    # Message will be sent to TCPParser
    # To check with dispatcher and execute function.
    # FIXME: Each function has differrent attributes, Cant execute them together.

    # TODO: Execute Authentication Test here. Check is user allowed
    # IDEA: Different user types to execute group of functions. Allow some users to execute some etc. remove_member

    pass

def main():
    server = BasicChatServer(mes)
    server.run()

if __name__ == "__main__":
    main()