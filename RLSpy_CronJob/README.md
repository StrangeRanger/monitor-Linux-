-Version 1.0-

The two scripts work together in order to find out if a user has logged/used su to become root. This program is disigned to be executed as a cronjob. It is recommended to have this program executed every Saturday at 11:59 PM. When cronjob executes the program, all data/information collected will be reported to the root_login_log. (NOTE: More notes will be added soon... This program will be updated soon as well. Needs a few more things added...)

Important Notes:
- When creating the cronjob, create it in root's cronjob by entering `sudo corntab -e`. The recommended crontab preset/setting is `59 23 * * 6 cd {location of RLSpy_CronJob} && python3 root_login_search.py`. It is important that you include `cd {location fo RLSpy_CronJob}` or else the cronjob will not work.

Security Features/Notes:
- Say a user, let's call him Bob, wants to log into the root account but does not want anyone to know that is was him. If he executed `sudo su {another user}`, becoming a different user on the system, then logged in as root, Bob would still be flagged. But if Bob used `sudo -i`, the user he had logged into, would be flagged instead.
- The auth.log will be scanned up to 7 days worth of logs.

Program Notes/Faults:
- If this program is to work correctly, the hostname of the computer or server MUST NOT contain the name of any user on the system: if you have a user named bob, the hostname can not be "bob-computer" or anything containing "bob". This will cause the program to falsely flag bob as a user who logged in as root or will double up on the amount of times he logged in as root if he used "sudo su". (NOTE: This will only occure if a user has been flagged as someone who has logged in as root.)
- On some flavors of Linux, if not all, the necesary information to identify a user who logged in as root will not show up. The specific problem lies in a sentence that contains the username: "session opened for user root by {username}(uid=0)". Sometimes the username will not show up and the sentence will look like this: "session opened for user root by (uid=0)". Therefore the user cannot be identified. This problem has only been identified for times when "sudo su" has been used. This problem, so far as I can understand, only happens when you are using the gui terminal. This problem does not occure when remotely connectly to a server using ssh, or when using a headless/non-gui system: tty1.