import sys
sys.path.insert(0, '../')

from mail import mail_for_request, login, read_email_from_gmail
from database.json_database.json_database_operations import PersonObjectManager


manager = PersonObjectManager()
manager.path = "../database/database.pkl"
manager.load()

if sys.argv[2] == "send":
    login()
    print mail_for_request(sys.argv[1], manager.persons[0], ["yazicis16@itu.edu.tr", "sencer_yazici98@hotmail.com"])
elif sys.argv[2] == "get":
    print read_email_from_gmail(["yazicis16@itu.edu.tr", "sencer_yazici98@hotmail.com"], sys.argv[1])
