# Purpose/What It Does
The script was created for the purpose of identifing users, on a linux based system, who have have successfully and unsuccessfully logged into/switch to the root user account as well as those who have successfully and unsuccessfully switched to a different user on the system. It does this by looking for a hard coded pattern/string/set of lines that are written to `/var/log/auth.log`. These patterns can be looked at in `identifying-patterns.odt`.

## Specifics
- There are two versions of the script. One is designed for manual execution. The other is designed to be executed as a CronJob.
- When executing either versions of the script, you **must** use `sudo` or else an error will be produced tellig you that you do not have permission to read the log. 

## Security Features/Notes:
- This script identifies user who have used `sudo bash`, `sudo -i`, `sudo su`, and `su`/`su root`
- If a user on the system created a temporary account in order to log in as root, then deletes the account after he or she is done with it, the temporary account will still show up in the scan results.
- Any and all users who use `sudo su` to change to another user will be marked/identified. This makes it easier to identify a user who tries to blame a different user for logging in as root. (see Script Notes/Faults below)
- Any and all users who attempt to either log into the root account or switch users, and are unsuccessful, will be identified and marked down.
- Users who are not in the sudoers file and try to execute a command with root privilege, will be identified.

## Script Notes/Faults:
- If a user with sudo power, call him Mal, switches to another user who may or may not have sudo power, call him Vic, then uses `sudo` or `su`, will cause Vic to be blamed for executing the commands instead of Mal. Though, Mal must know Vic's password in order successfully use sudo. The best way to verify who actually did it is 
  - Semi-built in helper: Becuase the script will identify users who use `su` and `sudo su`, Mal will be identified as an individual who switched users.
  - Method of weeding out true culprit: Look through the auth.log at the logs taken on the given day that the incident took place... To know what to look for, please refer to "dentifying-patterns.odt"; it contains all auth.log logs that are created in relation to the given commands and there relative success or failure...

## Flaws (that will be fixed in the future):
- If a user inputs their sudo password correctly when executing `sudo su {username}`, but the username does not exist, they will still be marked as `{username} has switched users {X} time(s)`.

## Requirements
- Python 3.x

## Linux Distros That The Script Works On:
- Ubuntu
  - Trusty Tahr: Unkown
  - Xenial Xerus: Works
  - Bionic Beaver: Unkown
- Debian
  - Jessie: Unkown
  - Stretch: Works
- "More will be tested in the future"

### Quick Note
Anywhere, inside of this README.md, that you see `{}` with text inside, are things that you substitute with whatever is described between the curly brackets: `{username}` will be replaced with the your username such as `StrangeRanger`.
