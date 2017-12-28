from database_struct import Member, structure

def deserialize(path_to_file):
    list_of_members = []

    f = open(path_to_file,'r')
    lines = f.readlines()
    for line in lines:
        if line[0] != "#":
            line = line[:-1]
            args = line.split(',')
            member = Member(args)
            list_of_members.append(member)
    f.close()
    return list_of_members

def add_to_database(member, path_to_file):
    if type(member) is Member:
        line = member.serialize()
        f = open(path_to_file, 'a+')
        f.writelines(line)

def add_attribute(member, value, attribute, path_to_file):
    if type(member) is Member:
        if attribute != "mail" or attribute != "teams":
            member.__setattr__(attribute, value)
        else:
            member.__setattr__(attribute).append(value)
        remove_from_database(member.id, "id", path_to_file)
        add_to_database(member, path_to_file)

def get_from_database(index, attribute, path_to_file):
    members = deserialize(path_to_file)
    match = None
    for member in members:
        if member.__getattribute__(attribute) == index:
            match = member
        elif index in member.__getattribute__(attribute):
            match = member
    return match

def remove_from_database(index, attribute, path_to_file):
    indexarr = structure.index(attribute)
    f = open(path_to_file,'r')
    lines = f.readlines()
    f.close()
    match = ""
    for line in lines:
        arr = line.split(',')
        if arr[indexarr] == index:
            match = line
            print "Deleting " + index
        # elif type(arr[]) ==
    lines.remove(match)

    f = open(path_to_file,'w')
    f.writelines(lines)
    f.close()
