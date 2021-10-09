import paramiko

class SSD_test:
    def __init__(self,logname,hostname,port,username,password):
        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        with open(logname, 'a+') as f:
            f.write("\r\rM.2 test start \r")
        SSD_result='Fail'

        stdin, stdout, stderr = ssh.exec_command("fdisk -l")
        disk_info = stdout.read()
        with open(logname, 'a+') as f:
            f.write("The disk info is:\r  '%s'\r" % (disk_info))
        stdin, stdout, stderr = ssh.exec_command("fdisk -l | grep '512.1 GB' | wc -l")
        disk_number = int(stdout.read())
        if (disk_number!=2):
            print("M.2 disk number detect failed, the number should be 2 while only '%d' detected"%(disk_number))
            with open(logname, 'a+') as f:
                f.write("M.2 disk number detect failed, the number should be 2 while only '%d' detected, error code 20001\r"%(disk_number))
        else:
            SSD_result='Pass'
            print('M.2 test Pass')
            with open(logname, 'a+') as f:
                f.write("M.2 test Pass\r")

        # close connect
        ssh.close()
        return SSD_result