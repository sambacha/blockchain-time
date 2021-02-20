#!/bin/bash
# Convert the "yyyymmddhh" string in argument $1 to "yyyy-mm-dd hh:00" and
# pass the result to 'date --rfc-3339=seconds' to normalize the date.
# The date is interpreted in the timezone specified by the value that
# the "TZ" environment variable was at first invocation of the script.
#
# Example 1: 2015-12-10 10:00 PST (UTC-0800)
#    $ env TZ='America/Los_Angeles' ./utcdate 2015121010
#    2015121018
#
# Example 2: 2015-10-10 10:00 PDT (UTC-0700; PST with DST in effect)
#    $ env TZ='America/Los_Angeles' ./utcdate 2015101010
#    2015101017

# Raw YYYYMMDDHH converted to YYYY-MM-DD HH:00.
convldt="$(echo "$1" | awk '
$1 ~ /^[0-9]{10}/
{
    year = substr($0, 1, 4)
    mon = substr($0, 5, 2)
    day = substr($0, 7, 2)
    hour = substr($0, 9, 2)
    printf("%s-%s-%s %s:00\n", year, mon, day, hour)
    exit
}
{ print "errorfmt" ; exit 1 }
')"
if test x"$convldt" = xerrorfmt ; then
    echo "note: Format must be YYYYMMDDHH." >&2
    exit 1
fi

# The converted time is then normalized to include a timezone.
normldt="$(env TZ="$TZ" date -d "$convldt" --rfc-3339=seconds || echo error)"
test x"$normldt" = xerror && exit 2

# Convert to UTC.    
date -u -d "$normldt" +'%Y%m%d%H'
