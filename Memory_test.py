import paramiko
import re



class Memory_test:
    def __init__(self,logname):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname='10.168.1.213', port=22, username='root', password='1')

        with open(logname, 'a+') as f:
            f.write("\r\rMEMORY test start \r")
        MEMORY_result='FAIL'
        stdin, stdout, stderr = ssh.exec_command("cat /proc/meminfo | grep MemTotal")
        MEM_total_info=stdout.read()
        MEM_total_info_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("cat /proc/meminfo | grep MemFree")
        MEM_free_info=stdout.read()
        # print('MEM_free is:',MEM_free_info)
        MEM_free_info_error=stderr.read()
        MEM_total = re.findall('\d+', MEM_total_info)
        MEM_total = int(MEM_total[0])
        with open(logname, 'a+') as f:
            f.write("MEM total info is:\r  '%s'\rMEM free info is:\r  '%s'\r"%(MEM_total_info,MEM_free_info))
        # print('MEM_total is:',MEM_total)
        if ('MemTotal:' in MEM_total_info):
            if (MEM_total < 60000000):
                print('Memtotal Test Fail, error code is 02001')
                with open(logname, 'a+') as f:
                    f.write("Memtotal Test Fail, error code is 02001\r")
            elif ('MemFree:' not in MEM_free_info):
                print('Memfree Test Fail, error code is 02003')
                with open(logname, 'a+') as f:
                    f.write("Memfree Test Fail, error code is 02003\r")
            else:
                MEMORY_result='PASS'
                print('Memory Test Pass')
                with open(logname, 'a+') as f:
                    f.write("Memory Test Pass\r")
        else:
            print('Memory info check failed, error code is 02002')
            with open(logname, 'a+') as f:
                f.write("Memory info check failed, error code is 02002\r")

        # close connect
        ssh.close()