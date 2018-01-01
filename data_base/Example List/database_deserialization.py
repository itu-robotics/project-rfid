from database_struct import Member
list_of_members = []

f = open("example.dat",'r')
lines = f.readlines()
for line in lines:
    if line[0] != "#":
        line = line[:-1]
        args = line.split(',')
        member = Member(args)
        list_of_members.append(member)
f.close()

print list_of_members[0].print_info()
print ""
print list_of_members[1].print_info()


from database_operations import *
get_from_database("senceryazici2@gmail.com", "mail", "example.dat").print_info()
add_attribute(list_of_members[0], "SENCER YAZICI", "name", "example.dat")

# remove_from_database("senceryazici2@gmail.com", "mail", "example.dat")
