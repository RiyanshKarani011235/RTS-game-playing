#!/usr/bin/python

import os,time

print('opening pipe')
r = open('/tmp/test','r')
print('reading from the pipe')
time.sleep(10)
print(r.read())
print('closing pipe')
print('done reading')
print(r.read())