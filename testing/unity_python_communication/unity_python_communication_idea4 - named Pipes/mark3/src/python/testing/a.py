#!/usr/bin/python	

import os

try :
	os.mkfifo('/tmp/test')
except OSError : 
	pass
print('opening pipe')
w = open('/tmp/test','w')
print(help(w))
print('writing to the pipe')
w.write('hello there\n')
print('closing pipe')
w.close()
print('done writing')