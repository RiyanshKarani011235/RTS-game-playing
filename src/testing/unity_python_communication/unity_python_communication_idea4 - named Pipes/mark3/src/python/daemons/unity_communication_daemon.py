#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

''' 
 - start daemon process when called with the argument "start"
 - stop daemon process when called with the argument "stop"
 - read values from the text buffer when called with the argument "read"
'''

import sys,os
import signal
import daemon
from utils.getcwd import getcwd
from utils import read_object_from_file
working_directory = getcwd()

objects_list = []
refresh_rate = 100

def main() :
    import time
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    global objects_list
    global refresh_rate
    update_time = 1.0/refresh_rate
    while True : 
        objects_list = []
        for root,dirs,files in os.walk(working_directory + 'text_buffer/python_read_text_buffer') : 
            for file in files : 
                objects_list.append(read_object_from_file.read(root + '/' + file))
        time.sleep(update_time)

if __name__ == '__main__' : 
    # is the top level module being called

    if len(sys.argv) < 3 :
        error_text = 'Usage: {} [command] [object name] [args]'.format(sys.argv[0])
        print(error_text)
        sys.stderr.write(error_text)
        raise SystemExit(1)

    PIDFILE = '/tmp/unity/' + sys.argv[2] + '.pid'
    LOGFILE = '/tmp/unity/' + sys.argv[2] + '.log'

    def start() : 
        try : 
            daemon.daemonize(PIDFILE,stdout=LOGFILE,stderr=LOGFILE)
        except RuntimeError as e : 
            # daemon already runnning, as defined in the 
            # daemon.daemonize method
            print(e)
            sys.stderr.write(e)
            raise SystemExit(1)
        else : 
            # daemon started
            main()

    def stop() : 
        # check if daemon is already running
        if os.path.exists(PIDFILE) :
            # daemon is running
            with open(PIDFILE) as f : 
                os.kill(int(f.read()),signal.SIGTERM)
        else : 
            # daemon is not running
            error_text = 'Daemon is not running'
            print(error_text)
            sys.stderr.write(error_text)
            raise SystemExit(1)
            
    def read() : 
        if os.path.exists(PIDFILE) : 
            global objects_list
            return objects_list
        else : 
            # daemon is not running
            error_text = 'Daemon is not running'
            print(error_text)
            sys.stderr.write(error_text)
            raise SystemExit(1)
            

    command_method_dictionary = {
        'start' : start,
        'stop' : stop,
        'read' : read,
    }

    if len(sys.argv) == 1 :
        error_string = 'No arguments provided. Usage: {} [start|stop]'.format(sys.argv[0])
        print(error_string)
        sys.stderr.write(error_string)
        raise SystemExit(1)

    else : 
        try : 
            command_method_dictionary[sys.argv[1]]()
        except KeyError : 
            error_string = 'Incorrect argument provided\n acceptable arguments are :\n' 
            for command in command_method_dictionary.keys() : 
                error_string += command + '\n'
                
            print(error_string,file=sys.stderr)
#             sys.stderr.write(error_string)
            raise SystemExit(1)