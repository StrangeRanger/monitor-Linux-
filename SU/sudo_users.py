import re

user = str(input("What user are you looking for?\n"))
txt = open("/etc/group", "r") # opens the group file in read mode

for line in txt:
    if line.startswith("sudo"): # finds the sudo group
        if re.match("sudo.+(:|,)%s(,|$)" % user, line): # checks if the given user is in the sudo group
            print(user + " is in the sudo group")
        else:
            print(user + " is NOT in the sudo group")
