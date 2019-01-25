import collections
from datetime import datetime, timedelta

class DateError(Exception):
    pass

N = 7 # how many days

def root_users():
    today = datetime.now().date()
    start_date = today - timedelta(days=N)
    this_year = datetime.now().year
    last_year = this_year - 1
    days = collections.defaultdict(collections.Counter) # A.1. a defaultdict that maps objects (dates) to counters.

    with open("/var/log/auth.log", "r") as txt: 
        for line in txt:
            fields = line.split() 
            date_str = " ".join(fields[0:2]) + " " 
            # makes sure that the log date is correct; if current date is January 01 2020 and looking a line in log with date Dec 31 that was logged in 2019, the date would = Dec 31 2020. Lines below prevent this.
            try:
                date = datetime.strptime(date_str + str(this_year), "%b %d %Y").date()
                if date > today: raise DateError
            except DateError:
                date = datetime.strptime(date_str + str(last_year), "%b %d %Y").date()
              # will skip any abnormal/non-regular text in /var/log/auth.log that could produce an Error, and then prints out a message telling the user to check out the line in the file.
            except ValueError:
                print("There was an abnormality on a line. Please take a look inside /var/log/auth.log at the line matching this: {}".format(line))
                continue

            if (date < start_date):
                # too old for interest
                continue 
            # "user : TTY=tty/1 ; PWD=/home/user ; USER=root ; COMMAND=/bin/su"
            if fields[4] == "sudo:":
                user = fields[5]
                # successful
                conditions = user != "root" and (fields[8] != "incorrect" if len(fields) >= 9 else None) and fields[-4] == "USER=root" and fields[-2] == "COMMAND=/bin/su"
                # unsuccessful
                conditions2 = user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and fields[-4] == "USER=root" and fields[-2] == "COMMAND=/bin/su"
                # `sudo su`...
                conditions3 =  fields[-3] == "USER=root" and fields[-1] in ("COMMAND=/bin/bash", "COMMAND=/bin/sh", "COMMAND=/bin/su")

                # "..."; identifies users who are not in the sudoers file and tried to execute a command with root privilege
                if user != "root" and (fields[8] == "NOT" and fields[10] == "sudoers" and fields[16] == "USER=root" and fields[18].startswith("COMMAND=") if len(fields) >= 9 else None): 
                    days[date]["~" + user] += 1
                # "..."; identifies users who successfully became root using `sudo su`
                if user != "root" and (fields[8] != "incorrect" if len(fields) >= 9 else None) and conditions3:
                    days[date]["+" + user] += 1 # A.2. The defaultdict key becomes the date and its value, which is the counter, is the user, which gains a plus 1 in the counter
                # "..."; identifies users who unsuccessfully became root using `sudo su`
                elif user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and conditions3:
                    days[date]["*" + user] += 1 # A.2.
                # "..."; identifies users who successfully became root using `sudo su root`
                elif conditions and fields[-1] == "root":
                    days[date]["+" + user] += 1 # A.2.
                # "..."; identifies users who unsuccessfully became root using `sudo su root`
                elif conditions2 and fields[-1] == "root":
                    days[date]["*" + user] += 1 # A.2.
                # "..."; identifies users who successfully switched users using `sudo su <username>`
                elif conditions and fields[-1] != "root": 
                    days[date]["-" + user] += 1 # A.2.
                # "..."; identifies users who unsuccessfully switched users using `sudo su <username>`
                elif conditions2 and fields[-1] != "root":
                    days[date]["/" + user] += 1 # A.2.

            if fields[4].startswith("su["):
                # root by <username>
                conditions4 = fields[-3] == "root" and fields[-1] != "root"
                # <username> by <username>
                conditions5 = fields[-3] != "root" and fields[-1] != "root"

                ### when a way is found, make it so that the severity level is greater with the ones below. "Change your password...<> knows your password"
                # "Successful su for root by <username>"; identifies users who've successfully became root using `su` and/or `su root`
                if fields[5] == "Successful" and conditions4:
                    user = fields[-1]
                    days[date]["+" + user] += 1 # A.2.
                # "FAILED su for root by <username>"; identifies users who've unsuccessfully became root using `su` and/or `su root`
                elif fields[5] == "FAILED" and conditions4:
                    user = fields[-1]
                    days[date]["*" + user] += 1 # A.2.
                # "Successful su for <username> by <username>"; identifies users who've successfully switched users using `su <username>`
                elif fields[5] == "Successful" and conditions5:
                    user = fields[-1]
                    days[date]["-" + user] += 1 # A.2. 
                # "FAILED su for <username> by <username>"; identifies users who've unsuccessfully switched users using `su <username>`
                elif fields[5] == "FAILED" and conditions5:
                    user = fields[-1]
                    days[date]["/" + user] += 1 # A.2.

    while start_date <= today:
        print(start_date.strftime("On %b %d:"))
        users = days[start_date]
        if users:
            for user, count in users.items(): # user, count is used because we're reading from a counter; which is a dict that maps username to count of occurrences
                end_of_sentence = str(count) + (" time" if count == 1 else " times")

                if "~" in user:
                    print("   ", user, "is not in the sudoers file and tried to execute a command with root privilege", end_of_sentence)
                elif "+" in user:
                    print("   ", user, "became root", end_of_sentence)
                elif "-" in user:
                    print("   ", user, "switched users", end_of_sentence)
                elif "*" in user:
                    print("   ", user, "tried to become root", end_of_sentence)
                elif "/" in user:
                    print("   ", user, "tried to switch users", end_of_sentence)
        else:
            print("    No one became root")
        start_date += timedelta(days=1)

root_users()