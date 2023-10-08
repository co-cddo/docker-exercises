#!/bin/bash

# Set a sensible default if no variable has been passed in
USERID=${USERID:-1000}
GROUPID=${GROUPID:-1000}

groupmod -o -g "$GROUPID" runuser
usermod -o -u "$USERID" runuser

echo "
User uid:    $(id -u runuser)
User gid:    $(id -g runuser)
-----------------------------
"
chown runuser:runuser /home/runuser
chown runuser:runuser /dev/stdout
