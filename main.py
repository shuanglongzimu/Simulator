#coding=utf-8
import threading
from shell_module import _shell, my_ser
from meter_module import process_simulator

Threads = []
th1 = threading.Thread(target = process_simulator, args = '')
Threads.append(th1)

th2 = threading.Thread(target = _shell, args = '')
Threads.append(th2)

if __name__ == '__main__':
    print '              欢迎使用模拟表工具            '
    for t in Threads:
        t.setDaemon(True)
        t.start()
    t.join()

