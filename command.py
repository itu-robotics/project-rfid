from database.json_database.json_database_operations import PersonObjectManager
from database.json_database.database_struct import Member

manager = PersonObjectManager()
manager.load()

input = raw_input("Database Terminal\n-$ ")

while input != "exit":
    if input == "ls":
        list = manager.find_all("", "")
        for l in list:
            print l.serialize()
    elif input == "add":
        manager.add()
    elif "rm -rf" in input:
        s = input.split(' ')[2]
        manager.remove(s)
    elif input == "add -s":
        _s = raw_input("Enter string\n")
        manager.addS(_s)
    input = raw_input("-$ ")
