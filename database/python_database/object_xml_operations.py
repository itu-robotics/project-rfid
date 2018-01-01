from lxml import objectify as obj
from database_struct import Member
import lxml.etree as serializer

# iturobotics_id,name_surname,mail,phone,itu-id,rfid,date_entred,level,team1

def _get_string_from_xml(path):
    # read the text
    f = open(path, 'r+')
    lines = f.readlines()
    for line in lines:
        if "#" in line:
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
        if "#" in line:
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


def add_member(member, path):
    member_array = from_xml(path)
    match = False
    for members in member_array:
        if member.id == members.id:
            match = True
    if not match:
        member_array.append(member)
        update_file(member_array, path)

def remove_member(member, path):
    member_array = from_xml(path)
    match = False
    found_member = None
    for members in member_array:
        if member.id == members.id:
            match = True
            found_member = members
    if match:
        member_array.remove(found_member)
        update_file(member_array, path)

array = ["123456","Sencer Yazici","senceryazici@gmail.com","0531XXXXXXX","040160XXX","XXX-XXX-XXX","01.01.2001","1","rover"]
mem = Member(array)
#to_xml(mem)
#update_file(member_list, "database.xml")
add_member(mem, "database.xml")
