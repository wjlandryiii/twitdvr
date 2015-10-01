#!/bin/sh

SRC=com.sourceflux.twitdvr.plist
DST=/Library/LaunchDaemons/com.sourceflux.twitdvr.plist


echo removing from launchd \(may error if not installed\)
launchctl unload $DST

echo Removing old plist
rm -f $DST

echo Copying plist
cp $SRC $DST

echo loading into launchd
launchctl load $DST
