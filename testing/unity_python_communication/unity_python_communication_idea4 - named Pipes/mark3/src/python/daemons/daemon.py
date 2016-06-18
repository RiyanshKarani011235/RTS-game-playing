
import os,sys
import atexit
import signal
import time,datetime

def daemonize(pidfile,stdin='/dev/null',stdout='/dev/null',stderr='/dev/null', initialize_pipes = True) : 
    print(pidfile)
    print(stdin)
    print(stdout)
    print(stderr)
    if os.path.exists(pidfile) : 
        raise RuntimeError('Already running')

    try : 
        if os.fork() > 0 : 
            raise SystemExit(0)  # parent exit
    except OSError as e : 
        raise RuntimeError('fork number 1 failed')
    else : 
        pass  # fork 1 success

    os.chdir('/')
    os.umask(0)
    
    os.setsid()  # the child process is now the session leader
    
    try : 
        if os.fork() > 0 : 
            raise SystemExit(0)
    except OSError as e : 
        raise RuntimeError('fork number 2 failed')
    else : 
        pass  # fork 2 success

    with open(stdin,'rb',0) as f : 
        os.dup2(f.fileno(),sys.stdin.fileno())
    with open (stdout,'ab',0) as f : 
        os.dup2(f.fileno(),sys.stdout.fileno())
    with open(stderr,'ab',0) as f : 
        os.dup2(f.fileno(),sys.stderr.fileno())
        
    with open(pidfile,'w') as f : 
        f.write(str(os.getpid()))
    
    # cleaning up before exiting
    def at_exit() : 
        os.remove(pidfile)
        # try : 
        #    os.remove(stdin)
        # except PermissionError :
        #     pass
        # try : 
        #     os.remove(stdout)
        # except PermissionError :
        #     pass
        # try :
        #     os.remove(stderr)
        # except PermissionError : 
        #     pass
    atexit.register(at_exit)
    
    def sigterm_handler(signo,frame) : 
        raise SystemExit(1)
        
    signal.signal(signal.SIGTERM,sigterm_handler)

    if initialize_pipes :

        import time
        log_file = '/tmp/log.txt'
        try : 
            os.system('rm ' + log_file)
        except : 
            pass
        os.system('touch ' + log_file)

        def log(string) : 
            data_already_present = ''
            if string[-1] != '\n' : 
                string += '\n'
            with open(log_file,'r') as f : 
                data_already_present = f.read()
            with open(log_file,'w') as f : 
                f.write(data_already_present + time.asctime(time.localtime(time.time())) + ' : python : ' + string)

        # unity pipes initialization
        unity_read_pipe_filename = ''
        unity_write_pipe_filename = ''

        for element in pidfile.split('.')[:-1] : 
            unity_read_pipe_filename += element + '.'
        unity_write_pipe_filename = unity_read_pipe_filename

        unity_write_pipe_filename = unity_write_pipe_filename[:-1] + '_unity_object_read_pipe'
        unity_read_pipe_filename = unity_read_pipe_filename[:-1] + '_unity_object_write_pipe'

        log('sending handshake to unity')
        unity_write_pipe = open(unity_write_pipe_filename,'w')
        unity_write_pipe.write('hello there\n')
        log('handshake sent')
        unity_write_pipe.close()
        unity_read_pipe = open(unity_read_pipe_filename,'r')
        unity_read_pipe.read()
        log('received acknowledgement from unity')
        log('daemon - unity communication established')

        # python pipes initialization
        python_read_pipe_filename = ''
        python_write_pipe_filename = ''

        for element in pidfile.split('.')[:-1] : 
            python_read_pipe_filename += element + '.'
        python_write_pipe_filename = python_read_pipe_filename

        python_write_pipe_filename = python_write_pipe_filename[:-1] + '_python_object_read_pipe'
        python_read_pipe_filename = python_read_pipe_filename[:-1] + '_python_object_write_pipe'
        
        log('sending handshake to python')
        python_write_pipe = open(python_write_pipe_filename,'w')
        python_write_pipe.write('hello there\n')
        log('handshake sent')
        python_write_pipe.close()
        python_read_pipe = open(python_read_pipe_filename,'r')
        python_read_pipe.read()
        log('received acknowledgement from python')
        log('daemon - python communication established')
  