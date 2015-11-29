#!/usr/bin/python
#
# Copyright 2015 Joseph Landry All Rights Reserved
#

import os
import httplib
import datetime
import time
import sys

# 1073741824 bytes at a time
SERVER = 'bglive-a.bitgravity.com'
SERVER_PATH = '/twit/live/high'
URL = 'http://bglive-a.bitgravity.com/twit/live/high'
WORKING_DIR = '/var/dvr/recordings'
FFMPEG = '/usr/local/bin/ffmpeg'
RECORD_HOURS = 10

# globals
START_TIME = 0
END_TIME = 1
LAST_UPDATE = datetime.datetime.now()

def pacify():
    global START_TIME
    global END_TIME
    global LAST_UPDATE

    now = datetime.datetime.now()
    if now - LAST_UPDATE > datetime.timedelta(seconds=5):
        LAST_UPDATE = now
        try:
            with open('/var/dvr/pr0n', 'w') as f:
                print >>f, "Time remaining:", END_TIME - now
        except:
            # don't stop recording because of the pacifier.
            pass

def record(until):
    filelist = []
    done = False
    while 1:
        if done:
            break
        d = datetime.datetime.now()
        d_str = d.strftime("%Y%m%d_%H%M%S")
        filename = 'out_%s.flv' % (d_str, )
        filelist.append(filename)
        with open(filename, 'wb') as fout:
            http = httplib.HTTPConnection('bglive-a.bitgravity.com', 80)
            http.request('GET', '/twit/live/high')
            response = http.getresponse()
            while 1:
                data = response.read(1024 * 16)
                if len(data) > 0:
                    fout.write(data)
                else:
                    break
                now = datetime.datetime.now()
                if until <= now:
                    done = True
                    break
                pacify()
    return filelist

def transcode(filelist, out_filename):
    ts_filelist = []
    for filename in filelist:
        ts_filename = os.path.splitext(filename)[0] + '.ts'
        ts_filelist.append(ts_filename)
        fmt = '%s -i "%s" -c copy -bsf:v h264_mp4toannexb -f mpegts "%s"'
        cmd = fmt % (FFMPEG, filename, ts_filename)
        os.system(cmd)
        print cmd
    filelist_str = "|".join(ts_filelist)
    fmt = '%s -i "concat:%s" -c copy -bsf:a aac_adtstoasc "%s"'
    cmd = fmt % (FFMPEG, filelist_str, out_filename)
    os.system(cmd)
    for ts_file in ts_filelist:
        os.remove(ts_file)
    print cmd

def main():
    global START_TIME
    global END_TIME
    os.chdir(WORKING_DIR)
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    delta = datetime.timedelta(0, RECORD_HOURS * 60 * 60)
    until = now + delta
    START_TIME = now
    END_TIME = until
    filelist = record(until)
    transcode(filelist, now_str + '.mp4')

if __name__ == '__main__':
    if "-h" in sys.argv:
        print "./record.py [ -l hours] [ -d hours]"
        print "\t -l: record time in hours (default 10)"
        print "\t -d: delay time in hours (default 0)"
        sys.exit(1)
    if "-d" in sys.argv:
        i = sys.argv.index("-d")
        if i + 1 < len(sys.argv):
            delay_hours = sys.argv[i+1]
            print "Waiting for: ", delay_hours, "Hours"
            sys.stdout.flush()
            time.sleep(float(delay_hours) * 60.0 * 60.0)
        else:
            print "./record.py -d [hours]"
            sys.exit(1)
    if "-l" in sys.argv:
        i = sys.argv.index("-l")
        if i + 1 < len(sys.argv):
            record_hours = sys.argv[i+1]
            RECORD_HOURS = float(record_hours)
        else:
            print "./record.py -l [hours]"
    print "Start recording at ", datetime.datetime.now()
    sys.stdout.flush()
    main()
