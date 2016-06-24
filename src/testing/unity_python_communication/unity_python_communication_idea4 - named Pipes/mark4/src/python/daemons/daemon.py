
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
        pass
        # os.remove(pidfile)
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

    import time
    log_file = '/tmp/log.txt'
    # try : 
    #     os.system('rm ' + log_file)
    # except : 
    #     pass
    # os.system('touch ' + log_file)

    def log(string) : 
        data_already_present = ''
        if string[-1] != '\n' : 
            string += '\n'
        with open(log_file,'a+') as f :
            object_name = pidfile.split('.')[-2].split('/')[-1] 
            f.write(data_already_present + time.asctime(time.localtime(time.time())) + ' : python : ' + object_name + ' : ' + string)
            f.flush()
            os.fsync(f.fileno())
    
    def sigterm_handler(signo,frame) : 
        log('exiting daemon')
        raise SystemExit(1)
        
    signal.signal(signal.SIGTERM,sigterm_handler)
    log('daemon initialized')
    if initialize_pipes :

            # sys.stdout.write(string)
        # unity pipes initialization
        unity_read_pipe_filename = ''
        unity_write_pipe_filename = ''

        for element in pidfile.split('.')[:-1] : 
            unity_read_pipe_filename += element + '.'
        unity_write_pipe_filename = unity_read_pipe_filename

        unity_write_pipe_filename = unity_write_pipe_filename[:-1] + '_unity_object_read_pipe'
        unity_read_pipe_filename = unity_read_pipe_filename[:-1] + '_unity_object_write_pipe'

        unity_read_pipe = open(unity_read_pipe_filename,'r')
        unity_write_pipe = open(unity_write_pipe_filename,'w')

        # unity handshake
        # r,w = os.pipe()
        # pid = os.fork()
        # if pid == 0 : 
        #     # read process
        #     os.close(r)
        #     time.sleep(1)
        #     with os.fdopen(w,'w') as w : 
        #         w.write('do it now')
        #     unity_read_pipe.read()
        #     log('received acknowledgement from unity')
        #     sys.exit(0)
        # else : 
        #     # write process
        #     os.close(w)
        #     with os.fdopen(r,'r') as r : 
        #         log(r.read())
        #     log('sending handshake to unity')    
        #     unity_write_pipe.write('I am iron man\n')
        #     log('handshake sent')
        #     unity_write_pipe.close()
        #     os.waitpid(pid,0)
        #     unity_write_pipe = open(unity_write_pipe_filename,'w')
        #     unity_write_pipe.write('connected\n')
        #     unity_write_pipe.close()
            
        log('sending handshake to unity')    
        unity_write_pipe.write('I am iron man\n')
        log('handshake sent')
        unity_write_pipe.close()
        unity_read_pipe.read()
        log('received acknowledgement from unity')  
        unity_write_pipe = open(unity_write_pipe_filename,'w')
        unity_write_pipe.write('connected\n')
        unity_write_pipe.close()

        time.sleep(1)
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
        python_read_pipe = open(python_read_pipe_filename,'r')
        log('waiting at read()')
        python_read_pipe.read()
        # with open('/tmp/log.txt','w') as f : 
        #     f.write('hhhhhh')
        time.sleep(1)
        python_write_pipe = open(python_write_pipe_filename,'w')
        python_write_pipe.write('hello there\n')
        log('handshake sent')
        time.sleep(1)
        python_write_pipe.close()
        log('received acknowledgement from python')
        log('daemon - python communication established')
  