import threading
import ctypes
import inspect
import time


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
    # print('please make effect')

class Thread(threading.Thread):
    def run(self):
        while 1:
            time.sleep(1)
            print('I hate you')


t=Thread()
t.start()
time.sleep(3)
stop_thread(t)