#coding=utf-8
import serial.tools.list_ports, os
from serial_module import my_ser, port_info, _serial
from meter_module import my_meter

def _shell():
    while True:
        global my_ser, my_meter
        in_str = raw_input('> ')

        if in_str == 'help':
            print '***************************************************************' + '\r\n' +\
                  '*                      模拟表shell命令码                        ' + '\r\n' +\
                  '*                                                              ' + '\r\n' +\
                  '* 1.valid port:    查看当前有效的端口号                          ' + '\r\n' +\
                  '* 2.port info:     查看端口参数信息,如串口号,波特率等              ' + '\r\n' +\
                  '* 3.set port:      设置端口号                                   ' + '\r\n' +\
                  '* 4.set parity:    设置奇偶校验位(E, O, N)                       ' + '\r\n' +\
                  '* 5.set baudrate:  设置波特率(300, 600 ,900, 1200 ,2400......)  ' + '\r\n' +\
                  '* 6.set bytesizes: 设置数据位(5, 6, 7)                          ' + '\r\n' +\
                  '* 7.set stopbits:  设置停止位(1, 1.5, 2)                        ' + '\r\n' +\
                  '* 8.open port:     打开端口                                     ' + '\r\n' +\
                  '* 9.close port:    关闭端口                                     ' + '\r\n' +\
                  '* 10.send data:    手动发送数据                                  ' + '\r\n' +\
                  '* 11.recv data:    手动接收数据                                  ' + '\r\n' +\
                  '* 11.recv data:    手动接收数据                                  ' + '\r\n' +\
                  '* 12.其他命令码:    调用当前运行操作系统平台的shell命令              ' + '\r\n' +\
                  '***************************************************************'

        elif in_str == 'valid port':
            port_list = list(serial.tools.list_ports.comports())
            num = 0
            if len(port_list) != 0:
                for name in port_list:
                    tmp_str = ''.join(name)
                    if tmp_str.find('usbserial') == -1:
                        continue
                    num += 1
                    print name
            else:
                print '提示: 没有可用的端口!'
            if num == 0:
                print '提示: 没有可用的端口!'

        elif in_str == 'port info':
            print 'port    : ' + port_info['port']
            print 'parity  : ' + port_info['parity']
            print 'timeout : ' + str(port_info['timeout'])
            print 'baudrate: ' + str(port_info['baudrate'])
            print 'bytesize: ' + str(port_info['bytesize'])
            print 'stopbits: ' + str(port_info['stopbits'])

        elif in_str == 'set port':
            tmp_str = raw_input('>port: ')
            if tmp_str.find('usbserial') != -1:
                port_info['port'] = tmp_str
            else:
                print 'Warning: set Port fail!'

        elif in_str == 'set parity':
            tmp_str = raw_input('>parity: ')
            if tmp_str == 'E' or tmp_str == 'O' or tmp_str == 'N':
                port_info['parity'] = tmp_str
            else:
                print 'Warning: set Parity fail!'

        elif in_str == 'set baudrate':
            tmp_str = raw_input('>baudrate: ')
            if int(tmp_str):
                port_info['baudrate'] = int(tmp_str)
            else:
                print 'Warning: set Baudrate fail!'

        elif in_str == 'set bytesize':
            tmp_str = raw_input('>bytesize: ')
            if int(tmp_str) <= 8 and int(tmp_str) >= 5:
                port_info['bytesize'] = int(tmp_str)
            else:
                print 'Warning: set Bytesize fail!'

        elif in_str == 'set stopbits':
            tmp_str = raw_input('>stopbits: ')
            if float(tmp_str) == 2 or float(tmp_str) == 1 or float(tmp_str) == 1.5:
                port_info['stopbits'] = float(tmp_str)
            else:
                print 'Warning: set Stopbits fail!'

        elif in_str == 'open port':
            my_ser = _serial(port_info['port'], port_info['baudrate'], port_info['bytesize'],\
                             port_info['parity'], port_info['stopbits'], port_info['timeout'])
            my_ser.open()
            my_ser.alive = True

        elif in_str == 'close port':
            my_ser.close()

        elif in_str == 'send data':
            tmp_str = raw_input('Please input send data: ')
            my_ser.send_data(tmp_str)

        elif in_str == 'recv data':
            print my_ser.recv_data(1024)

        else:
            os.system(in_str)
