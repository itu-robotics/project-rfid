import json
import cPickle as pickle
from database_struct import Member
_structure = ["id","name","mail","phone","rfid","date_entered","level","team"]

def _save_object(obj, name="object.pkl"):
    try:
        file = open(name, 'wb')
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)
        file.close()
        return True
    except:
        return False

def _load_object(name="object.pkl"):
    try:
        file = open(name, 'rb')
        s = pickle.load(file)
        file.close()
        return s
    except:
        return None

class PersonObjectManager():
    def __init__(self, person_array=[]):
        self.persons = person_array
        self.path = "database/database.pkl"

    def find(self, query, attr):
        for i in self.persons:
            if str(i.__getattribute__(attr)) == str(query):
                return i
        return None

    def find_all(self, query, attr):
        if query == "":
            return self.persons
        return [x for x in self.persons if x.__getattribute__(attr) == query ]

    def load(self):
        _data = _load_object(self.path)
        if not _data is None:
            self.persons =_data

    def load_json(self):
        file = open("database/database.json", 'r')
        json_str = file.read()
        json_str = "".join(json_str.split("\n"))
        json_str = json_str.replace("]", "")
        json_str = json_str.replace("[", "")

        json_arr = json_str.split("||")
        database_arr = []
        for jstr in json_arr:
            direc = json.loads(jstr)
            arr = []
            for attr in _structure:
                val = direc[attr]
                arr.append(val)
            database_arr.append(Member(arr))
        self.persons = database_arr

    def save_json(self):
        json_str = "[ "
        count = 0
        for member in self.persons:
            count += 1
            person_dir = {}
            for attribute in _structure:
                person_dir[attribute] = member.__getattribute__(attribute)
            if count == len(self.persons):
                json_str += json.dumps(person_dir)
            else:
                json_str += json.dumps(person_dir) + "|| \n"

        json_str += " ]"
        file = open("database/database.json", 'w')
        file.write(json_str)
        file.close()


    def save(self):
        _save_object(self.persons, self.path)
        self.save_json()

    def addS(self, string_to_parse, delimeter=","):
        self.persons.append(Member(string_to_parse.split(delimeter)))
        self.save()

    def add(self):
        values = []
        for i in range(len(_structure)):
            input = raw_input(_structure[i] + ":\n")
            values.append(input)
        self.persons.append(Member(values))
        self.save()

    def remove(self, id):
        obj = self.find(id, "id")
        if obj is None:
            print "No User Found with ID:" + id
            return
        self.persons.remove(obj)
        self.save()
