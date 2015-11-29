TWIT DVR
========

Depenancies
===========

```
brew install ffmpeg
brew install watch  # only to watch pr0n file
```

To edit plist, edit with text editor then run:

```
$ sudo ./install.sh
```

To change record length edit record.py `RECORD_HOURS` variable.

Manual Record
-------------

```
$ ./record.py [-d hours]
```


To watch status
---------------

```
$ cd /var/dvr
$ watch cat pr0n
```
