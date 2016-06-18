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
    # this step makes the daemon process give up the ability
    # to acquire a new controlling terminal (because only a 
    # session leader can do so) and provides even more isolation
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
        # first if necessary.
        # syntax : dup(fd,fd2) where : 
        #         fd  --> file descriptor to be duplicated
        #         fd2 --> the duplicate file descriptor 
        os.dup2(f.fileno(),sys.stdin.fileno())
        # what we are doing here is that we are replacing 
        # sys.stdin with the file object returned by 
        # open(stdin,rb,0)
    with open (stdout,'ab',0) as f : 
        os.dup2(f.fileno(),sys.stdout.fileno())
    with open(stderr,'ab',0) as f : 
        os.dup2(f.fileno(),sys.stderr.fileno())
        
    # write the PID of the daemon in the pid file (which in this
    # case is "/tmp/daemon.pid")
    with open(pidfile,'w') as f : 
        f.write(str(os.getpid()))
        
    # remove the PID file at exit
    atexit.register(lambda: os.remove(pidfile))
    # since we need to supply a function to the "atexit.register" 
    # method, we define an inline function using the "lambda" 
    # keyword
    
    # signal handler for termination
    def sigterm_handler(signo,frame) : 
        raise SystemExit(1)
    # this method is called when any signal is
    # passed to this process
        
    # signal.signal(signalnum, handler)
    # Set the handler for signal signalnum to the function handler. 
    # Handler can be a callable Python object
    signal.signal(signal.SIGTERM,sigterm_handler)
    