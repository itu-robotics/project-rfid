from database.json_database.json_database_operations import PersonObjectManager
from database.json_database.database_struct import Member

manager = PersonObjectManager()
manager.load()

input = raw_input("Database Terminal\n-$ ")
selected_person = None
while input != "exit":
    if "ls" in input.split(" ")[0]:
        args = input.split(" ")
        list = None
        status = True
        if len(args) < 2:
            list = manager.find_all("", "")
        elif len(args) > 2:
            list = manager.find_all(args[2], args[1])
        elif len(args) == 4:
            pass
        else:
            status = False
        if status:
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
    elif input == "debug":
        manager.load_json()
    elif input == "save":
        manager.save()
    elif input.split(" ")[0] == "cd":
        selected_person = manager.find_all(input.split(" ")[1], "id")[0]
        print selected_person.serialize()
    input = raw_input("-$ ")
