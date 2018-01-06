from lxml import objectify as obj
from database_struct import Member
import lxml.etree as serializer

# iturobotics_id,name_surname,mail,phone,itu-id,rfid,date_entred,level,team1

def _get_string_from_xml(path):
    # read the text
    f = open(path, 'r+')
    lines = f.readlines()
    lines_wanted = []
    for line in lines:
        if "<!--" in line:
            lines.remove(line)

    xml = ""
    for line in lines:
        xml += line
    f.close()
    return xml

def _construct_member_object(xml_object):
    array = ["id","name","mail","phone","itu_id","rfid","date_entered","level","team"]
    member = Member(array)
    for attr in array:
        member.__setattr__(attr, xml_object.__getattr__(attr))
    return member

def _generate_xml(member_array):
    xml = ["<main>"]
    for member in member_array:
        for member_line in to_xml(member):
            xml.append("    " + member_line)

    xml.append("</main>")
    return xml

def from_xml(path):
    xml = _get_string_from_xml(path)
    main = obj.fromstring(xml)
    members_array = []
    for member in main.member:
        member_obj = _construct_member_object(member)
        members_array.append(member_obj)
    return members_array

def to_xml(member):
    if type(member) is Member:
        item = obj.Element("member")
        item.id = member.id
        item.name = member.name
        item.mail = member.mail
        item.phone = member.phone
        item.itu_id = member.itu_id
        item.rfid = member.rfid
        item.date_entered = member.date_entered
        item.level = member.level
        item.team = member.team
        xml = serializer.tostring(item, pretty_print=True).replace("  ", "    ")
        return xml.split('\n')

def update_file(member_array, path):
    xml = _generate_xml(member_array)
    f = open(path, 'r')
    all_lines = f.readlines()
    comment_lines = []
    for line in all_lines:
        if "<!--" in line:
            comment_lines.append(line)

    f.close()
    total = []
    for line in comment_lines:
        total.append(line)
    for line in xml:
        total.append(line)

    text = ""
    for i in total:
        text += i + '\n'

    open(path, 'w').close()
    f = open(path, 'w')
    f.write(text)
    f.close()

def check_existance(query, attribute, path):
    member_list = from_xml(path)
    match = False
    count = 0
    member_exist = []
    for members in member_list:
        if query == members.__getattribute__(attribute):
            count += 1
            match = True
            member_exist.append(members)

    return member_exist

def add_member(member, path):
    member_array = from_xml(path)
    match = False
    for members in member_array:
        if member.id == members.id:
            match = True
    if not match:
        print "Adding member id: " + member.id + " " + member.name
        member_array.append(member)
        update_file(member_array, path)
    else:
        print "id with "  + member.id +  " already exists. Exiting adding sequence."

def remove_member(query, attribute, path):
    list_of_existance = check_existance(query, attribute, path)
    count = len(list_of_existance)
    user_i = "y"
    if count > 1:
        print "Found " + str(count) + " instances on database with query = " + attribute
        for i in list_of_existance:
            print "Name :" + i.name + " " + attribute + ": " + str(i.__getattribute__(attribute))
        user_i = raw_input("Would you like to delete all instances Answer (y/n)\n")

        if "n" in user_i:
            print "Cancelling deleting sequence"
            return
    member_list = from_xml(path)
    for mathces in list_of_existance:
        for members in member_list:
            if mathces.id == members.id:
                member_list.remove(members)
                print "Removing member: " + members.name + " " + members.id
    update_file(member_list, path)

def update_member(member, path):
    count = len(check_existance(member.id,"id",path))
    if count == 0:
        print "No member fount, Exiting..."
    elif count == 1:
        remove_member(member.id, "id", path)
        add_member(member, path)

def update_by_attribute(id, value, attribute, path):
    member_found = check_existance(id, "id", path)
    mem_temp = member_found[0]
    mem_temp.__setattr__(attribute, value)
    mem_temp.print_info()
    update_member(mem_temp, path)

def count_members(path):
    return len(from_xml(path))

def search(query, attr, path):
    string = "***INFORMATION***\n\n"

    for i in check_existance(query, attr, path):
        string += i.get_info() + "\n\n"
    string += "***END OF INFORMATION***\n"
    return "Found " + str(len(check_existance(query, attr, path))) + " members with search query of, " + attr + ": " + query + "\n" + string

# IDEA: define global path, remove path argument from ecach function
# IDEA: New functions added ? To sort etc..


# TEMP: TEST AREA - To be deleted! >
# array = ["040160427","Sencer Yazici","senceryazici@gmail.com","05xxxxxxxxx","040160427","XXX-XXX-XXX","20.09.2016","2","rover"]
# mem = Member(array)
# print count_members("database.xml")
#to_xml(mem)
#update_file(member_list, "database.xml")
# add_member(mem, "database.xml")
# remove_member("12345676", "id", "database.xml")
# update_member(mem, "database.xml")
# update_by_attribute("040160027", "000-000-000", "rfid", "database.xml")
# print search("2", "level", "database.xml")
# TEMP: TEST AREA - To be deleted! <
