#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

''' 
--------------------- specifications -----------------------------
 - start daemon process when called with the argument "start"
 - stop daemon process when called with the argument "stop"
 - read values from the text buffer when called with the argument "read"
------------------------------------------------------------------
'''

import sys,os
import signal
import daemon

def main() : 
    import time
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    while True : 
        sys.stdout.write('Daemon Alive\n')
        time.sleep(1) 

if __name__ == '__main__' : 
    # is the top level module being called

    PIDFILE = '/tmp/python_read_daemon.pid'
    LOGFILE = '/tmp/python_read_daemon.log'

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
        pass

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