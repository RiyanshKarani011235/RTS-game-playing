#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import os,sys
import atexit
import signal

def daemonize(pidfile,stdin='/dev/null',stdout='/dev/null',stderr='/dev/null') : 
    if os.path.exists(pidfile) : 
        raise RuntimeError('Already running')
    
    # first fork (detach the child process from the parent 
    # process, and then terminate the parent)
    try : 
        if os.fork() > 0 : 
            raise SystemExit(0)  # parent exit
    except OSError as e : 
        raise RuntimeError('fork number 1 failed')
    else : 
        pass  # fork 1 success
    
    # it is a good practice to change the directory so that
    # the daemon is no longer working in the directory it was
    # launched from
    os.chdir('/')
    os.umask(0)
    
    os.setsid()  # the child process is now the session leader
    
    # second fork (relinquish session leadership)
    try : 
        if os.fork() > 0 : 
            raise SystemExit(0)
    except OSError as e : 
        raise RuntimeError('fork number 2 failed')
    else : 
        pass  # fork 2 success
        
    # replace the file descriptors for stdin, stdout and stderr
    with open(stdin,'rb',0) as f : 
        # dup2 duplicates the file descriptor, closing the latter
        # first if necessary
        os.dup2(f.fileno(),sys.stdin.fileno())
    with open (stdout,'ab',0) as f : 
        os.dup2(f.fileno(),sys.stdout.fileno())
    with open(stderr,'ab',0) as f : 
        os.dup2(f.fileno(),sys.stderr.fileno())
        
    # write the PID file
    with open(pidfile,'w') as f : 
        # write the PID of this daemon in the pid file (which in
        # this case is /tmp/daemon.pid)
        f.write(str(os.getpid()))
        
    # remove the PID file at exit
    atexit.register(lambda: os.remove(pidfile))
    
    # signal handler for termination
    def sigterm_handler(signo,frame) : 
        raise SystemExit(1)
    # this method is called when any signal is
    # passed to this process
        
    # signal.signal(signalnum, handler)
    # Set the handler for signal signalnum to the function handler. 
    # Handler can be a callable Python object
    signal.signal(signal.SIGTERM,sigterm_handler)
    
def main() : 
    import time
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    while True : 
        sys.stdout.write('Daemon Alive\n')
        time.sleep(1)
    
if __name__ == '__main__' :  # this is the file which is run
    PIDFILE = '/tmp/daemon.pid'
    
    if len(sys.argv) != 2 : 
        error_text = 'Usage: {} [start|stop]'.format(sys.argv[0])
        print(error_text)
        # with open(sys.stderr,'wt') as f : 
        #     f.write(error_text)
        sys.stderr.write(error_text)
        raise SystemExit(1)
    
    if sys.argv[1] == 'start' :
        try : 
            daemonize(PIDFILE, stdout='/tmp/daemon.log', stderr='/tmp/daemon.log')
        except RuntimeError as e : 
            error_text = e
            print(e)
            sys.stderr.write(error_text)
            raise SystemExit(1)
        else : 
            pass # daemon started
        
        main()
        
    elif sys.argv[1] == 'stop' : 
        if os.path.exists(PIDFILE) :  # check if daemon is already running
            with open(PIDFILE) as f : 
                # os.kill(pid, sig) Send signal sig to the process pid. 
                # Constants for the specific signals available on the host 
                # platform are defined in the signal module.
                os.kill(int(f.read()),signal.SIGTERM)
                # in this case the file f (/tmp/daemon.pid) which stores the 
                # PID of the daemon process is read (returning the PID of the
                # daemon process). This PID is the first argument to the 
                # os.kill method, which means that this signal will be sent
                # to the daemonized process
                # -----------------------------------------------------------
                # we send the signal "signal.SIGTERM" to the daemon process.
                # since the "signal.signal(signal.SIGTERM,sigterm_handler)"
                # handler is defined for the signal "signal.SIGTERM", the 
                # sigterm_handler method is called, which is defined in
                # daemonize.py
        
        else : 
            error_text = 'daemon not running'
            print(error_text)
            sys.stderr.write(error_text)
            raise(SystemExit(1))
            
    else : 
        error_text = 'unknown command {}'.format(sys.argv[1])
        print(error_text)
        sys.stderr.write(error_text)
        raise SystemExit(1) 