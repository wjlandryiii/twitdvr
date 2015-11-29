#!/usr/bin/python

import sys

TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.sourceflux.twitdvr</string>
	<key>ProgramArguments</key>
	<array>
		<string>/var/dvr/record.py</string>
	</array>
	<key>StandardErrorPath</key>
	<string>/var/dvr/logs/err.log</string>
	<key>StandardOutPath</key>
	<string>/var/dvr/logs/out.log</string>
	<key>StartCalendarInterval</key>
	<dict>
		<key>Weekday</key>
		<integer>{:d}</integer>
		<key>Minute</key>
		<integer>{:d}</integer>
		<key>Hour</key>
		<integer>{:d}</integer>
	</dict>
</dict>
</plist>
"""

days = [
        'sunday',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
]

print "What day should the recording run on?"
print ""
print "\t0: sunday"
print "\t1: monday"
print "\t2: tuesday"
print "\t3: wednesday"
print "\t4: thursday"
print "\t5: friday"
print "\t6: saturday"
print ""
day = raw_input("Choose day [0-6]: ")

day = int(day)
print "You chose: {:d}".format(day)
print ""

print "What hour should the recording run on?"
hour = raw_input("Choose hour [0-23]: ")
hour = int(hour)
if hour < 0 or 23 < hour:
    print "hour must be from 0 to 23"
    sys.exit(1)

print "You chose: {:d}".format(hour)
print ""

print "How many minutes past the hour should the recording start?"
minute = raw_input("Chose minute [0-59]: ")
minute = int(minute)
print "You chose: {:d}".format(minute)
print ""

print "How many hours would you like to record?"
length = raw_input("Choose hours: ")
length = int(length)
print "You chose: {:d}".format(length)
print ""

print "You chose: {:s} at {:02d}:{:02d} for {:d} hours".format(days[day], hour, minute, length)

confirm = raw_input("is this correct (y/n)? ")
if confirm != 'y':
    print "canceling..."
    sys.exit(1)

with open("com.sourceflux.twitdvr.plist", "w") as f:
    f.write(TEMPLATE.format(day, minute, hour))

print "SAVED!"
