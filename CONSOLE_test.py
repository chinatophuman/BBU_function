import paramiko
import time
import commands
import threading
import ctypes
import inspect


class CONSOLE_test:
    def __init__(self,logname,hostname,port,username,password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def test_content(self):

        # # create SSH item
        # ssh = paramiko.SSHClient()
        # # permit connect to remote host
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # # connect
        # ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rCONSOLE test start \r")
        CONSOLE_result='FAIL'
        commands.getoutput('rm -f console.txt')

        def _async_raise(tid, exctype):
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        def stop_thread(thread):
            _async_raise(thread.ident, SystemExit)
            # print('I hate you')

        class cat_console_value(threading.Thread):
            # def __init__(self, logname):
            #     self.logname = logname
            #     super(local_console_value, self).__init__()
            #     self._stop_event = threading.Event()

            def run(self):
                # with open(self.logname, 'a+') as f:
                #     f.write('start get console value \r')
                commands.getoutput('cat /dev/ttyUSB0 > console.txt')
                # while True:
                #     print('test')
                #     time.sleep(0.5)

            # def stop(self):
            #     self._stop_event.set()


        t = cat_console_value()
        t.start()
        time.sleep(1)
        commands.getoutput("echo 'console' > /dev/ttyUSB0")
        time.sleep(1)
        stop_thread(t)

        console_value = commands.getoutput('cat console.txt')

        with open(self.logname, 'a+') as f:
            f.write("local console get value is %s \r" % (console_value))
        if ('command not found' not in console_value):
            with open(self.logname, 'a+') as f:
                f.write('CONSOLE Test Failed, error code 19001 \r')
        else:
            CONSOLE_result='PASS'
            with open(self.logname, 'a+') as f:
                f.write('CONSOLE Test PASS \r')


        # ssh.close()
        return CONSOLE_result