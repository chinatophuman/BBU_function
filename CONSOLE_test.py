import paramiko
import time

class CONSOLE_test:
    def __init__(self,logname):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname='10.168.1.213', port=22, username='root', password='1')

        with open(logname, 'a+') as f:
            f.write("\r\rCONSOLE test start \r")
        CONSOLE_result='FAIL'
        try:
            stdin, stdout, stderr=ssh.exec_command("rm -f ./BiTLog*.log")
            # print(stdout.read())
        except:
            print('delete BitLog failed')
        try:
            stdin, stdout, stderr=ssh.exec_command("/mnt/Hoping/burnintest/64bit/bit_cmd_line_x64")
            # print(stdout.read())
        except:
            print('run bit_cmd_line_x64 failed')
        start_time=time.time()
        while (time.time()-start_time < 60):
            stdin, stdout, stderr=ssh.exec_command("ls | grep BiTLog")
            bitlog=stdout.read()
            # print('bitlog is:',bitlog)
            if ('BiTLog' in bitlog):
                stdin, stdout, stderr = ssh.exec_command("cat '%s'"%(bitlog))
                log = stdout.read()
                if ('TEST RUN PASSED' in log):
                    CONSOLE_result='PASS'
                    print('CONSOLE Test Pass')
                    with open(logname, 'a+') as f:
                        f.write("CONSOLE Test Pass\r")
                else:
                    print('CONSOLE Test Fail, error code 19001')
                    with open(logname, 'a+') as f:
                        f.write("CONSOLE Test Fail, error code 19001\r")
                ssh.exec_command("mv '%s' ./ftlog/.tempLog"%(bitlog))
            time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command("ls | grep BiTLog")
        bitlog = stdout.read()
        if ('BiTLog' not in bitlog):
            print('CONSOLE Test timeout, error code 19002')
            with open(logname, 'a+') as f:
                f.write("CONSOLE Test timeout, error code 19002\r")

        # close connect
        ssh.close()