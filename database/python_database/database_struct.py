structure = ["id","name","mail","phone","itu_id","rfid","date_entered","level","team"]
class Member(object):
    """ITU Robotics Member Structure"""
    def __init__(self, arg):
        self.id = arg[0]
        self.name = arg[1]

        self.mail = arg[2].split(' ')

        self.phone = arg[3]
        self.itu_id = arg[4]
        self.rfid = arg[5]
        self.date_entered = arg[6]
        self.level = arg[7]
        self.team = arg[8].split(' ')

    def print_info(self):
        print "id: " + self.id
        print "Name: " + self.name
        print "mail: " + str(self.mail)
        print "phone: " + self.phone
        print "itu_id: " + self.itu_id
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
        string += "\nitu_id: " + self.itu_id
        string += "\nrfid: " + self.rfid
        string += "\ndate_entered: " + self.date_entered
        string += "\nlevel: " + self.level
        string += "\nteam: " + str(self.team)
        return string


    def serialize(self):
        mails = ""
        for mail in self.mail:
            mails += mail + " "
        mails = mails[:-1]

        team = ""
        for team in self.team:
            team += team + " "
        team = team[:-1]

        return self.id + "," + self.name + "," + mails + "," + self.phone + "," + self.itu_id + "," + self.rfid + "," + self.date_entered + "," + self.level + "," + team
