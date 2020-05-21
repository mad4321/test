#!/usr/bin/env python3

import os
import re
import asyncio
import sys
from subprocess import Popen, STDOUT, PIPE
import time
import logging

cmd = 'ls -la'
hosts_list = ['192.168.254.103','192.168.254.26']

async def do_task(host,cmd):
    ssh_proc = Popen("ssh %s '%s'"%(host,cmd),shell=True,stdin=PIPE, stdout=PIPE,stderr=PIPE)
    out, err = ssh_proc.communicate()
    rc = ssh_proc.returncode
    print("Host: %s\ncmd: %s\nRC: %d\n%s"%(host,cmd,rc,out.decode('ascii')))

async def main(hosts_list):
   await asyncio.gather(*[do_task(host,cmd) for host in hosts_list])

if __name__ == '__main__':
    if len(sys.argv)<3:
        print("Usage: task2.py <command> <host ip 1> [host ip 2] ... [host ip 3]")
        sys.exit(2)

    cmd = sys.argv[1]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[2:]))
