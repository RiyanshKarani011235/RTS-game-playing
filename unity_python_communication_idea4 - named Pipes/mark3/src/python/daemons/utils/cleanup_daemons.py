#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import os

for root,dirs,files in os.walk('/tmp/unity/') : 
	for file in files : 
		if '.pid' in file : 
			PID = 0
			with open(file,'r') : 
				os.kill(int(file.read()),signal.SIGTERM)
