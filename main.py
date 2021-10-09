import os
import commands
import time
from tkMessageBox import showinfo
import easygui as gui
import re
import paramiko

ETHPORT = 'p3p1'
HOSTPORT = 'www.baidu.com'
buildoption_type='Intel(R) Core(TM) i3-4150 CPU @ 3.50GHz'
logname = 'ft_test_log.txt'

# create SSH item
ssh = paramiko.SSHClient()
# permit connect to remote host
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# connect
ssh.connect(hostname='10.168.1.198', port=22, username='root', password='111111')

testitem=['ETH_BBU','SFP_BBU','USB_BBU','SATA_BBU','M.2_BBU',
          'VGA_BBU','CPU_BBU','MEMORY_BBU','CONSOLE_BBU','PCIE_BBU']

for item in testitem:
    if (item == 'ETH_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rETH test start \r")
        ETH_result='Fail'
        fail_cnt=0
        cnt=0
        # os.system("ifconfig '%s' 192.168.217.131/24 up"%(ETHPORT))
        stdin, stdout, stderr = ssh.exec_command("ethtool '%s'" % (ETHPORT))
        ethinfo = stdout.read()
        eth_error = stderr.read()
        with open(logname,'a+') as f:
            f.write("The board's ETH info is:\r  '%s'\r"%(ethinfo))

        while (cnt<6):
            # print('ethinfo is:', ethinfo)
            stdin, stdout, stderr = ssh.exec_command("ping -c 15 -I '%s' '%s'" % (ETHPORT, HOSTPORT))
            pinginfo = stdout.read()
            ping_err = stderr.read()
            # print('pinginfo is:', pinginfo)
            # print(pinginfo)
            with open(logname, 'a+') as f:
                f.write("The '%d' ping info is:\r  '%s'\r" % (cnt,pinginfo))
            if (not('Speed: 1000Mb/s' in ethinfo) or not('Link detected: yes' in ethinfo) or
                    not('0% packet loss' in pinginfo) or ('10% packet loss' in pinginfo) or ('100% packet loss' in pinginfo)):
                fail_cnt+=1
                cnt+=1
            else:
                # print('Test Pass')
                cnt+=1
        if (fail_cnt < 3):
            ETH_result='Pass'
            print('ETH Test Pass')
            with open(logname, 'a+') as f:
                f.write("ETH Test Pass\r")
        else:
            print('ETH Test fail, error code 05001')
            with open(logname, 'a+') as f:
                f.write("ETH Test fail, error code 05001\r")

    if (item == 'SFP_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rSFP test start \r")
        print('SFP test Skip')
        with open(logname,'a+') as f:
            f.write("SFP test Skip, No SFP hardware\r")

    if (item == 'USB_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rUSB test start \r")
        USB_result='FAIL'
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Mouse | wc -l")
        mouse_num=int(stdout.read())
        # print(mouse_num)
        mouse_num_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Mouse")
        mouse_info=stdout.read()
        # print(mouse_num)
        mouse_info_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Keyboard | wc -l")
        keybaord_num = int(stdout.read())
        keyboard_num_error = stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Keyboard")
        keybaord_info = stdout.read()
        keyboard_info_error = stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Bulk-Only | wc -l")
        usb_num = int(stdout.read())
        usb_num_error = stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Bulk-Only")
        usb_info = stdout.read()
        usb_info_error = stderr.read()
        with open(logname, 'a+') as f:
            f.write("Mouse info is:\r  '%s'\rKeyboard info is:\r  '%s'\rUSB info is:\r  '%s'\r"%(mouse_info,keybaord_info,usb_info))
        if (mouse_num != 1):
            print('Mouse Test failed, error code is 04003')
            with open(logname, 'a+') as f:
                f.write("Mouse Test failed, error code is 04003\r")
        elif(keybaord_num != 1):
            print('Keyboard Test failed, error code is 04002')
            with open(logname, 'a+') as f:
                f.write("Keyboard Test failed, error code is 04002\r")
        elif(usb_num != 1):
            print('USB Test failed, error code is 04001')
            with open(logname, 'a+') as f:
                f.write("USB Test failed, error code is 04001\r")
        else:
            print('USB Test Pass')
            USB_result='PASS'
            with open(logname, 'a+') as f:
                f.write("USB Test Pass\r")

    if (item == 'SATA_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rSATA test start \r")
        sata_result= 'FAIL'
        stdin, stdout, stderr = ssh.exec_command("fdisk -l")
        sata_info=stdout.read()
        info_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("fdisk -l | grep /dev/sd | grep bytes | wc -l")
        sata_num=int(stdout.read())
        num_error=stderr.read()
        with open(logname, 'a+') as f:
            f.write("SATA info is:\r  '%s'\rSATA number is:\r  '%d'\r"%(sata_info,sata_num))
        if (sata_num < 1):
            print('SATA number Test failed, error code is 03002')
            with open(logname, 'a+') as f:
                f.write("SATA number Test failed, detect '%d' SATA number, need at least 1 SATA ,error code is 03002\r"%(sata_num))
        else:
            sata_result= 'PASS'
            print('SATA Test Pass')
            with open(logname, 'a+') as f:
                f.write("SATA Test Pass\r")

    if (item == 'M.2_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rM.2 test start \r")
        print('M.2 Test Skip')
        with open(logname,'a+') as f:
            f.write("M.2 test Skip, No M.2 hardware\r")

    if (item == 'VGA_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rVGA test start \r")
        VGA_result=gui.ccbox(msg='please check the vga screen display is light', title='VGA_check', choices=('light','not light'))
        if (VGA_result):
            VGA_result= 'PASS'
            print('The user choose light, VGA Test Pass')
            with open(logname, 'a+') as f:
                f.write("The user choose light, VGA Test Pass\r")
        else:
            print('The user choose not light, VGA Test failed, error code is 08001')
            with open(logname, 'a+') as f:
                f.write("The user choose not light, VGA Test failed, error code is 08001\r")

    if (item == 'CPU_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rCPU test start \r")
        CPU_result='FAIL'
        stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep 'model name'")
        cpu_info=stdout.read()
        cpu_info_error=stderr.read()
        cpu_type = cpu_info.split(':')[-1]
        # print("The CPU type on board is:",cpu_type)
        stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep process | wc -l")
        cpu_num=int(stdout.read())
        cpu_num_error=stderr.read()
        # print("The CPU core on board is:",cpu_num)
        with open(logname, 'a+') as f:
            f.write("CPU info is:\r  '%s'\rCPU number is:\r  '%d'\r"%(cpu_info,cpu_num))
        if (buildoption_type in cpu_type):
            CPU_result='PASS'
            print('CPU Test Pass')
            with open(logname, 'a+') as f:
                f.write("CPU Test Pass\r")
        else:
            print('CPU Test Failed, error code is 01001')
            with open(logname, 'a+') as f:
                f.write("CPU Test Failed, error code is 01001\r")

    if (item == 'MEMORY_BBU'):
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
            if (MEM_total > 4000000):
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

    if (item == 'CONSOLE_BBU'):
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

    if (item == 'PCIE_BBU'):
        with open(logname, 'a+') as f:
            f.write("\r\rPCIE test start \r")
        PCIE_result='FAIL'
        tempnum=0
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci | grep -i Ethernet")
        pcie_info=stdout.read()
        pcie_info_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci | grep -i Ethernet | wc -l")
        pcie_num=stdout.read()
        pcie_num_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 03:00.0 -vvv")
        pcieX1Seep=stdout.read()
        pcieX1Seep_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 03:00.0 -vvv | grep width")
        pcieX1SeepValue=stdout.read()
        pcieX1SeepValue_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 01:00.0 -vvv")
        pcieX4Seep=stdout.read()
        pcieX4Seep_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 01:00.0 -vvv | grep width")
        pcieX4SeepValue=stdout.read()
        pcieX4SeepValue_error=stderr.read()
        # print('pcie_num is:',pcie_num)
        # print('pcieX1Seepvalue is:',pcieX1SeepValue)
        # print('pcieX4Seepvalue is:', pcieX4SeepValue)
        with open(logname, 'a+') as f:
            f.write("PCIE info is:\r  '%s'\rPCIE number is:\r  '%s'\rPCIEX1Seep is:\r  '%s'\rPCIEX1SeepValue is:\r  '%s'\rPCIEX4Seep is:\r"
                    "  '%s'\rPCIEX4SeepValue is:\r  '%s'\r"%(pcie_info,pcie_num,pcieX1Seep,pcieX1SeepValue,pcieX4Seep,pcieX4SeepValue))
        if (pcie_num<1 or '2.5GT' not in pcieX1Seep or '2.5GT' not in pcieX4Seep):
            print('Pcie Test failed, error coed is 13001')
            with open(logname, 'a+') as f:
                f.write("Pcie Test failed, error coed is 13001\r")
        else:
            PCIE_result='PASS'
            print('Pcie Test Pass')
            with open(logname, 'a+') as f:
                f.write("Pcie Test Pass\r")


# close connect
ssh.close()