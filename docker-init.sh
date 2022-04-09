#!/bin/bash

# Create comic-dl homedir
mkdir -p /home/comic-dl

# Set UID/PID of user that youtube-dl will be run as
COMICDLPGID=${PGID:-1000}
COMICDLPUID=${PUID:-1000}

# Check to see if group/user already exist, if so, delete
EXISTINGGROUPNAME=$(getent group "$COMICDLPGID" | cut -d ':' -f 1)
EXISTINGUSERNAME=$(getent passwd "$COMICDLPUID" | cut -d ':' -f 1)
if [[ -n "$EXISTINGGROUPNAME" ]]; then
    groupdel -f "$EXISTINGGROUPNAME"
fi
if [[ -n "$EXISTINGUSERNAME" ]]; then
    userdel -f "$EXISTINGUSERNAME"
fi

# Create user/group
addgroup --quiet --gid "$COMICDLPGID" comic-dl
chown -R "$COMICDLPUID":"$COMICDLPGID" /home/comic-dl
adduser --quiet --system --disabled-password --uid "$COMICDLPUID" --gid "$COMICDLPGID" --home /home/comic-dl comic-dl
HOME=/home/comic-dl
export HOME

# Set UMASK if required
if [[ -n "$UMASK" ]]; then
    umask "$UMASK"
fi

# Run comic-dl with remainder of command line arguments
setpriv --reuid comic-dl --regid comic-dl --keep-groups python3 /opt/comic-dl/cli.py "$@"

