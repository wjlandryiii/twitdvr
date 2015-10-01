#!/bin/sh

URL=http://bglive-a.bitgravity.com/twit/live/high
OUTPUTDIR=/Users/minidvr/Documents
RECORD_HOURS=8
RECORD_SECONDS=`expr $RECORD_HOURS \* 60 \* 60`
FLVFILE=$OUTPUTDIR/`date '+%Y_%m_%d__%H_%M_%S'`.flv
MP4FILE=$OUTPUTDIR/`date '+%Y_%m_%d__%H_%M_%S'`.mp4

curl -s -o $FLVFILE $URL &
CURLPID=$!
echo Curl pid: $CURLPID
sleep $RECORD_SECONDS
kill $CURLPID
/usr/local/bin/ffmpeg -nostats -loglevel 0 -i $FLVFILE $MP4FILE
