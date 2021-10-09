import os
import commands
import time
from tkMessageBox import showinfo
import easygui as gui
import re

ETHPORT = 'ens33'
HOSTPORT = 'www.baidu.com'
buildoption_type='AMD Ryzen 5 4600U with Radeon Graphics'

testitem=['ETH_BBU','SFP_BBU','USB_BBU','SATA_BBU','M.2_BBU',
          'VGA_BBU','CPU_BBU','MEMORY_BBU','CONSOLE_BBU','PCIE_BBU']
for item in testitem:
    if (item == 'ETH_BBU'):
        ETH_result='Fail'
        fail_cnt=0
        cnt=0
        # os.system("ifconfig '%s' 192.168.217.131/24 up"%(ETHPORT))
        ethinfo=commands.getoutput("ethtool '%s'"%(ETHPORT))
        pinginfo=commands.getoutput("ping -c 15 -I '%s' '%s'"%(ETHPORT,HOSTPORT))
        # print(pinginfo)
        while (cnt<6):
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
        else:
            print('ETH Test fail, error code 05001')

    if (item == 'SFP_BBU'):
        print('SFP test Skip')

    if (item == 'USB_BBU'):
        USB_result='FAIL'
        usb_num=commands.getoutput("lsusb -v | grep Mouse | wc -l")
        if (usb_num == 0):
            print('USB Test failed, error code is 04001')
        else:
            print('USB Test Pass')
            USB_result='PASS'

    if (item == 'SATA_BBU'):
        sata_result= 'FAIL'
        sata_info=commands.getoutput("fdisk -l")
        sata_num=commands.getoutput("fdisk -l | grep /dev/sd | grep 125829120 | wc -l")
        if (sata_num < 1):
            print('Test failed, error code is 03002')
        else:
            sata_result= 'PASS'
            print('SATA Test Pass')

    if (item == 'M.2_BBU'):
        print('M.2 Test Skip')

    if (item == 'VGA_BBU'):
        VGA_result=gui.ccbox(msg='please check the vga screen display is light', title='VGA_check', choices=('light','no light'))
        if (VGA_result):
            VGA_result= 'PASS'
            print('VGA Test Pass')
        else:
            print('VGA Test failed, error code is 08001')

    if (item == 'CPU_BBU'):
        CPU_result='FAIL'
        cpu_info=commands.getoutput("cat /proc/cpuinfo | grep 'model name'")
        cpu_type = cpu_info.split(':')[-1]
        cpu_num=commands.getoutput("cat /proc/cpuinfo | grep process | wc -l")
        print("The CPU core on board is '%s'"%(cpu_num))
        if (buildoption_type in cpu_type):
            CPU_result='PASS'
            print('CPU Test Pass')
        else:
            print('CPU Test Failed, error code is 01001')

    if (item == 'MEMORY_BBU'):
        MEMORY_result='FAIL'
        MEM_total_info=commands.getoutput("cat /proc/meminfo | grep MemTotal")
        MEM_free_info=commands.getoutput("cat /proc/meminfo | grep MemFree")
        MEM_total = re.findall('\d+', MEM_total_info)
        MEM_total = int(MEM_total[0])
        if ('MemTotal:' in MEM_total_info):
            if (MEM_total <2500000):
                print('Memtotal Test Fail, error code is 02001')
            elif ('MemFree:' not in MEM_free_info):
                print('Memfree Test Fail, error code is 02003')
            else:
                MEMORY_result='PASS'
                print('Memory Test Pass')
        else:
            print('Memory info check failed, error code is 02002')

    if (item == 'CONSOLE_BBU'):
        CONSOLE_result='FAIL'
        commands.getoutput("rm -f ./BiTLog*.log")
        commands.getoutput("/mnt/Hoping/burnintest/64bit/bit_cmd_line_x64")
        start_time=time.time()
        while (time.time()-start_time < 60):
            bitlog=commands.getoutput("ls | grep BiTLog")
            if ('BiTLog' in bitlog):
                log = commands.getoutput("cat '%s'"%(bitlog))
                if ('TEST RUN PASSED' in log):
                    CONSOLE_result='PASS'
                    print('CONSOLE Test Pass')
                else:
                    print('CONSOLE Test Fail, error code 19001')
                commands.getoutput("mv '%s' ./ftlog/.tempLog"%(bitlog))
        time.sleep(5)

    if (item == 'PCIE_BBU'):
        PCIE_result='FAIL'
        tempnum=0
        pcie_info=commands.getoutput("/sbin/lspci | grep -i Ethernet")
        pcie_num=commands.getoutput("/sbin/lspci | grep -i Ethernet | wc -l")
        pcieX1Seep=commands.getoutput("/sbin/lspci -s 03:00.0 -vvv")
        pcieX1SeepValue=commands.getoutput("/sbin/lspci -s 03:00.0 -vvv | grep width")
        pcieX4Seep=commands.getoutput("/sbin/lspci -s 01:00.0 -vvv")
        pcieX4SeepValue = commands.getoutput("/sbin/lspci -s 01:00.0 -vvv | grep width")
        if (pcie_num<2 or '2.5GT' not in pcieX1Seep or '5GT' not in pcieX4SeepValue):
            print('Pcie Test failed, error coed is 13001')
        else:
            PCIE_result='PASS'
            print('Pcie Test Pass')