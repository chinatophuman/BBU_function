import paramiko


host='10.168.1.198'
user='root'
passwd='111111'

import paramiko
import re

# remote operation command
def rcmd(command=None, host=None, passwd=None, user=None, port=22, save_path="rcmd_error.txt"):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=passwd, port=port)
        try:
            _stdin, _stdout, _stderr = ssh.exec_command(command)
            bash_out = _stdout.readlines()
            bash_err = _stderr.read()
            if bash_err:
                save_err = '[%s] bash input: %s, ERROR:\n%s' % (host, command, bash_err) + "\n"
                with open(save_path, "a+") as f:
                    f.write(save_err)
                return False
            if bash_out:
                return bash_out
        except Exception as ssh_err:
            save_err = '[%s] bash ERROR:\n%s' % (host, ssh_err) + "\n"
            with open(save_path, "a+") as f:
                f.write(save_err)
            return False
        finally:
            ssh.close()
    except Exception as ssh_err:
        save_err = '[%s] bash ERROR:\n%s' % (host, ssh_err) + "\n"
        with open(save_path, "a+") as f:
            f.write(save_err)
        return False

# get used memory
def get_used_mem(host=None, passwd=None, user='root', port=22):
    used_mem = -1
    cmd_result = rcmd(command='free', host=host, passwd=passwd, user=user, port=port)
    if cmd_result:
        mem_out = cmd_result[1]
        used_mem = int(mem_out.split()[2])
        used_mem = round(used_mem / 1024 / 1024, 1)
        return used_mem
    else:
        return used_mem

# get disk free
def get_total_disk(host=None, passwd=None, user='root', port=22):
    total_disk = -1
    cmd_result = rcmd(command='df', host=host, passwd=passwd, user=user, port=port)
    if cmd_result:
        disk_out = cmd_result[1:]
        total_disk = 0
        for d in disk_out:
            total_disk += int(d.split()[1])
        total_disk = round(total_disk / 1024 / 1024 / 1024, 1)
        return total_disk
    else:
        return total_disk

# get total memory
def get_total_mem(host=host, passwd=passwd, user='root', port=22):
    total_mem = -1
    cmd_result = rcmd(command='free', host=host, passwd=passwd, user=user, port=port)
    print(cmd_result)
    if cmd_result:
        mem_out = cmd_result[1]
        total_mem = int(mem_out.split()[1])
        total_mem = round(total_mem / 1024 / 1024)
        return total_mem
    else:
        return total_mem

total_memory = get_total_mem()
print(total_memory)