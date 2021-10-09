import os
import commands
import time
from tkMessageBox import showinfo
import easygui as gui
import re
import paramiko
from ETH_test import ETH_test
from VGA_test import VGA_test
from USB_test import USB_test
from SATA_test import SATA_test
from CPU_test import CPU_test
from Memory_test import Memory_test
from CONSOLE_test import CONSOLE_test
from PCIE_test import PCIE_test
from SSD_test import SSD_test
from SFP_test import SFP_test

ETHPORT = 'enp2s0'
HOSTPORT = '10.168.1.124'
buildoption_type='Intel(R) Xeon(R) D-2177NT CPU @ 1.90GHz'
logname = 'ft_test_log.txt'
hostname = '10.168.1.213'
port = 22
username = 'root'
password = '1'
SFPPORT1 = 'enp184s0f0'
SFPPORT2 = 'enp184s0f1'
SFPPORT3 = 'enp184s0f2'
SFPPORT4 = 'enp184s0f3'

# # create SSH item
# ssh = paramiko.SSHClient()
# # permit connect to remote host
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # connect
# ssh.connect(hostname='10.168.1.198', port=22, username='root', password='111111')

commands.getoutput("rm -f '%s'"%(logname))

testitem=['SFP_BBU']

# testitem=['VGA_BBU','ETH_BBU','USB_BBU','SATA_BBU','M.2_BBU',
#           'SFP_BBU','CPU_BBU','MEMORY_BBU','CONSOLE_BBU','PCIE_BBU']
for item in testitem:
    if (item=='VGA_BBU'):
        VGA_result=VGA_test(logname)
    if (item=='ETH_BBU'):
        ETH_result=ETH_test(logname,ETHPORT,HOSTPORT,hostname,port,username,password)
    if (item=='USB_BBU'):
        USB_result=USB_test(logname,hostname,port,username,password)
    if (item=='SATA_BBU'):
        SATA_result=SATA_test(logname,hostname,port,username,password)
    if (item=='CPU_BBU'):
        CPU_result=CPU_test(logname,buildoption_type)
    if (item=='MEMORY_BBU'):
        Memory_result=Memory_test(logname)
    if (item=='CONSOLE_BBU'):
        CONSOLE_result=CONSOLE_test(logname)
    if (item=='PCIE_BBU'):
        PCIE_result=PCIE_test(logname,hostname,port,username,password)
    if (item=='M.2_BBU'):
        SSD_result=SSD_test(logname,hostname,port,username,password)
        print(SSD_result)
    if (item=='SFP_test'):
        SFP_result=SFP_test(logname,hostname,port,username,password,SFPPORT1,SFPPORT2,SFPPORT3,SFPPORT4)
        print(SFP_result)