structure = ["id","name","mail","phone","itu_id","rfid","date_entered","level","team"]
class Member(object):
    """ITU Robotics Member Structure"""
    def __init__(self, arg):
        self.id = arg[0]
        self.name = arg[1]

        self.mail = arg[2]

        self.phone = arg[3]
        self.rfid = arg[4]
        self.date_entered = arg[5]
        self.level = arg[6]
        self.team = arg[7]

    def print_info(self):
        print "id: " + self.id
        print "Name: " + self.name
        print "mail: " + str(self.mail)
        print "phone: " + self.phone
        print "rfid: " + self.rfid
        print "date_entered: " + self.date_entered
        print "level: " + self.level
        print "team: " + str(self.team)

    def get_info(self):
        string = ""
        string += "id: " + self.id
        string += "\nName: " + self.name
        string += "\nmail: " + str(self.mail)
        string += "\nphone: " + self.phone
        string += "\nrfid: " + self.rfid
        string += "\ndate_entered: " + self.date_entered
        string += "\nlevel: " + self.level
        string += "\nteam: " + str(self.team)
        return string


    def serialize(self):
        return self.id + "," + self.name + "," + self.mail + "," + self.phone + "," + self.rfid + "," + self.date_entered + "," + self.level + "," + self.team
