#!/usr/bin/env sh
# For a local time option this representation 'makes' sense as it contains
#   the offset to UTC at that point in time.
# At DST changes, the trailing offset part will change making the representation unique.
# 
# Example:
# $ gdate --iso-8601=minutes
# > 2022-06-14T23:20-07:00
#

date() {
	if [ "$1" = "-I" ]; then
		command date "+%Y-%m-%dT%H:%M:%S%z"
    exit 0
	else
		date --iso-8601=minutes
    exit 0
	fi
}

# Note: TRAP could be used but this is portable (POSIX)
echo "ERROR: Command not found"
exit 127
