#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

# import os
import sys,os
import time
time.sleep(5)

# for root,dirs,files in os.walk('/tmp/unity') : 
# 	object_names = []
# 	for file in files : 
# 		if '.pid' in file :
# 			object_name = '' 
# 			for element in file.split('.')[:-1] : 
# 				object_name += element + '.'
# 			object_names.append(object_name[:-1])

# # with open('/tmp/log.txt','w') as f : 
# # 	f.write('hallaleuja')

# objects = []
# for object_name in object_names :
# 	with open('/tmp/log.txt','w') as f : 
# 		f.write(object_name + "_read_pipe = open('/tmp/unity/' + '" + 
# 		object_name + "_python_object_read_pipe','r')" )
# 	exec(object_name + "_read_pipe = open('/tmp/unity/' + '" + 
# 		object_name + "_python_object_read_pipe','r')")
# 	with open('/tmp/log.txt','w') as f : 
# 		f.write('hallaleuja')
# 	exec(object_name + "_read_pipe.read()")
# 	exec(object_name + "_write_pipe = open('/tmp/unity/' + '" + 
# 		object_name + "_python_object_write_pipe','w')")
# 	exec('objects.append([' + object_name + '_read_pipe,' + object_name + '_write_pipe])')

# sys.stderr.write('hallaleuja')
# # with open('/tmp/log.txt') as f : 
# # 	f.write('hallaleuja')
# for object_ in objects : 
# 	object_[1].flush()
# 	print(object_[0].read())
# 	object_[1].write('hello there]\n')
# 	object_[1].close()

log_file = '/tmp/log.txt'
def log(string) : 
    data_already_present = ''
    if string[-1] != '\n' : 
        string += '\n'
    with open(log_file,'r') as f : 
        data_already_present = f.read()
    time.sleep(0.05)
    with open(log_file,'w') as f : 
        f.write(data_already_present + time.asctime(time.localtime(time.time())) + ' : python : ' + string)
        f.flush()
        os.fsync(f.fileno())

log('writing data to daemon')	
w = open('/tmp/unity/PlayerController1_python_object_write_pipe','w')
w.write('hello there\n')
w.close()
# with open('/tmp/log.txt','w') as f : 
# 	f.write('done writing')
log('reading data from daemon')
r = open('/tmp/unity/PlayerController1_python_object_read_pipe','r')
r.read()