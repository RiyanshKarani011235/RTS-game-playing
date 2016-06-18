#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import os,signal

for root,dirs,files in os.walk('/tmp/unity/') : 
	for file in files : 
		if '.pid' in file : 
			with open(root + file,'r') as file:
				pid = int(file.read())
				print(pid) 
				try : 
					os.kill(pid,signal.SIGTERM)
				except ProcessLookupError : 
					pass

os.system('rm -r /tmp/unity')
os.system('mkdir /tmp/unity')
