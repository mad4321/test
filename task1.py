#!/usr/bin/env python3

import os
import re
import asyncio
import sys
from subprocess import Popen, STDOUT, PIPE
import time
import logging

#X = needed space
#Z = files count
#Y = file size

X = 2048000000
Z = 10
Y = 1024000
Data = 'Test string'

async def create_file(filename,size):
    try:
#        with open(filename,'wb') as f:
#            f.seek(size-1)
#            f.write(b'\0')
#            f.close()
        echo_proc = Popen(['yes', Data], stdout=PIPE)
        dd_proc = Popen(['dd','of='+filename,'bs='+str(size),'count=1','iflag=fullblock'],stdin=echo_proc.stdout, stdout=PIPE,stderr=PIPE)
        out, err = dd_proc.communicate()
        rc = dd_proc.returncode
    except (OSError, IOError) as err:
        logging.error('File error: %s'%(err))
        sys.exit(2)

async def main(path):
   await asyncio.gather(*[create_file(path+'file'+str(num),Y) for num in range(Z)])

def find_path(size):
    with open('/proc/mounts','r') as f:
        mounts = {line.split()[0]:line.split()[1]+','+line.split()[3] for line in f.readlines()}
    for (mount,s) in mounts.items():
        flags = {f:1 for f in s.split(',')}
        if (re.match(r'/dev/',mount) and flags.get('rw')):
            path = s.split(',')[0]
            st = os.statvfs(path)
            freesize = st.f_bavail*st.f_frsize
            if (freesize>=X):
                return path
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - [%(process)d]:%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d - %(message)s')
    logging.info('Try to find mountpoint with %d bytes free'%(X))
    path = find_path(X)
    if (not path):
        logging.error("No suitable path found")
        sys.exit(2)
    logging.info("Found path '%s'"%(path))
    logging.info("Create %d files with size %d bytes"%(Z,Y))
    start_time=round(time.time()*1000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(path))
    end_time=round(time.time()*1000)
    logging.info('Time took: %dms'%(end_time-start_time))
