#!/bin/bash
# A fake of the Zmbackup installer, for the Molecule tests. It saves its
# arguments and environment.
set -eu
[ -e /opt/zimbra/log/fake-running ] || { echo "Zimbra is not running" >&2; exit 1; }
# Like the real installer, stop with exit 3 when no cron daemon is running
grep -qxE 'cron|crond' /proc/[0-9]*/comm 2> /dev/null || { echo "No cron daemon is running" >&2; exit 3; }
mkdir -p /var/log/fake-zmbackup /usr/local/lib/zmbackup
echo "$*" >> /var/log/fake-zmbackup/calls
env | grep -E '^(OSE_|ZMBKP_|MAX_PARALLEL_PROCESS|ROTATE_TIME|LOCK_BACKUP)' | sort > /var/log/fake-zmbackup/env
touch /usr/local/lib/zmbackup/zmbackup.jar
