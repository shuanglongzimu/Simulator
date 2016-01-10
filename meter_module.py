#coding=utf-8

import csv, sys, os, time, binascii, shell_module
from data_fmt import calc_checksum, str_to_hex

# type = sys.getfilesystemencoding()

# reader = csv.reader(open('/Users/lilonglong/Desktop/DLT645-2007.csv', 'rb'))
#
# list_data = []
#
# for line in reader:
#     print line[1].decode("utf8").encode(type)
#     # line[1] = unicode(line[1], 'utf8')
#     print line
#
# print reader

protocol_list = []

class meter:
    def __init__(self, bytes_waittime):
        self.bytes_waittime = 0.1
        self.buf_data = []

        path = os.getcwd() + '/meter_protocol'
        if not os.path.exists(path):
            print '提示: meter_protocol 目录不存在!'
        else:
            flag = False
            for i in os.listdir(path):
                file_path = path + '/' + i
                if not os.path.exists(file_path):
                    continue
                if i.find('.csv') == -1:
                    continue
                flag = True
                fp = open(file_path, 'rb')
                tmp_list = []
                tmp_list.append(i)
                tmp_list.extend(csv.reader(fp))
                protocol_list.append(tmp_list)
                fp.close()
            if not flag:
                print '提示: meter_protocol 目录下没有电表规约库.csv文件!'

    def recv_data(self, data):
        tmp_str = ''
        msg_valid = True
        for i in range(len(data)):
            tmp_str += data[2*i: 2*(i+1)] + ' '
        print time.strftime("%H:%M:%S", time.localtime()) + ' Recv: ' + tmp_str.upper()

        self.buf_data = str_to_hex(data, 2)
        for i in range(len(self.buf_data)):
            if self.buf_data[i] == 0x68:
                break
        del self.buf_data[:i]
        list_len = len(self.buf_data)
        if list_len == 14 or list_len == 16:
            checksum = calc_checksum(self.buf_data[:list_len - 2])
            if self.buf_data[7] != 0x68 or self.buf_data[8] & 0x40 or checksum != self.buf_data[list_len - 2] or self.buf_data[list_len - 1] != 0x16:
                print '提示: 解析数据报文失败!'
                msg_valid = False
        else:
            print '提示: 解析数据报文失败!'
            msg_valid = False

        list_log = []
        list_log.extend([time.strftime("%H:%M:%S", time.localtime())]) #发生时间
        list_log.extend(['接收']) #传输方向
        if msg_valid:
            DI = ''
            if list_len == 14:
                for i in range(2):
                    DI += '%02X' % ((self.buf_data[11 - i] - 0x33) & 0xff)
            else:
                for i in range(4):
                    DI += '%02X' % ((self.buf_data[13 - i] - 0x33) & 0xff)
            list_log.extend(['\'' + DI + '\'']) #数据标识
        else:
            list_log.extend([''])
        list_log.extend([tmp_str.upper()]) #数据报文
        addr = ''
        for i in range(6):
            addr += "%02X" % self.buf_data[6-i]

        self.save_log(addr, list_log)
        return msg_valid

    def send_data(self):
        send_data = []
        send_data.extend(self.buf_data[:8]) #拷贝电表地址

        DI = 0
        list_DI = []
        data_len = self.buf_data[9]
        for i in range(data_len):
            list_DI.extend([self.buf_data[10 + i]])
            self.buf_data[10 + i] = (self.buf_data[10 + i] - 0x33) & 0xff
            DI += self.buf_data[10 + i] << (i*8)

        tmp_list = []
        for i in range(len(protocol_list)):
            if data_len == 2 and protocol_list[i][0] != 'DLT645-1997.csv':
                continue
            if data_len == 4 and protocol_list[i][0] != 'DLT645-2007.csv':
                continue

            for j in range(2, len(protocol_list[i])):
                if DI != int('0x' + protocol_list[i][j][0], 16):
                    continue
                tmp_list = protocol_list[i][j]
                break
            break

        if len(tmp_list) == 0:
            if data_len == 2:
                send_data.extend([0xC1]) #97表异常回复控制字
                print 'Error: DLT645-1997.csv规约库没有数据标识 %04X.' % DI
            elif data_len == 4:
                send_data.extend([0xD1]) #07表异常回复控制字
                print 'Error: DLT645-2007.csv规约库没有数据标识 %08X.' % DI
            send_data.extend([0x01]) #Len
            send_data.extend([0x01]) #ERR
        else:
            fmt = tmp_list[1]
            size = int(tmp_list[2], 10)
            unit = tmp_list[3]
            name = tmp_list[5]
            data = tmp_list[6]

            if data_len == 2:
                send_data.extend([0x81])
            else:
                send_data.extend([0x91])
            send_data.extend([size + data_len])
            send_data.extend(list_DI)

            tmp_len = 0
            start_pos = 0
            while tmp_len < size:
                end_pos = data.find(';', start_pos)
                if end_pos == -1:
                    break
                tmp_str = data[start_pos:end_pos]
                tmp = str_to_hex(tmp_str, 2)
                tmp.reverse()
                send_data.extend(tmp)
                start_pos = end_pos + 1
                tmp_len += len(tmp)

            for i in range(size):
                send_data[10+data_len+i] = (send_data[10+data_len+i] + 0x33) & 0xff

        send_data.extend([calc_checksum(send_data)])
        send_data.extend([0x16])

        ret = ''
        for i in range(len(send_data)):
            ret += '%02X' % send_data[i] + ' '

        print time.strftime("%H:%M:%S", time.localtime()) + ' Send: ' + ret

        list_log = []
        list_log.extend([time.strftime("%H:%M:%S", time.localtime())])
        list_log.extend(['发送'])
        if len(tmp_list) == 0:
            list_log.extend([''])
        else:
            if data_len == 2:
                list_log.extend(['\'' + str('%04X' % DI) + '\'']) #数据标识
            else:
                list_log.extend(['\'' + str('%08X' % DI) + '\'']) #数据标识
        list_log.extend([ret])
        if len(tmp_list) == 0:
            list_log.extend(['异常应答'])
        else:
            list_log.extend([tmp_list[5] + '(' + tmp_list[1] + '): ' + tmp_list[6]])
        addr = ''
        for i in range(6):
            addr += "%02X" % send_data[6-i]
        self.save_log(addr, list_log)

        ret = ret.replace(' ', '')
        ret = ret.decode('hex')
        return ret

    def set_bytes_waittime(self, sec_tm):
        self.bytes_waittime = sec_tm

    def save_log(self, str_addr, list_data):
        log_dir = os.getcwd() + '/log/' + time.strftime("%Y%m%d", time.localtime())
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_path = log_dir + '/' + str_addr + '.csv'
        writer = csv.writer(file(log_path, 'a+'), dialect='excel')
        if os.path.getsize(log_path) == 0:
            writer.writerow(['发生时间', '传输方向', '数据标识', '报文内容', '解析报文'])
        writer.writerow(list_data)

my_meter = meter(0.1)

def process_simulator():
    '''
        处理模拟表报文的收发
    '''
    while True:
        if not shell_module.my_ser.alive:
            continue

        recv_data = shell_module.my_ser.recv_data(my_meter.bytes_waittime, 0xffffffff)
        if len(recv_data) == 0:
            continue
        recv_data = binascii.b2a_hex(recv_data)
        if my_meter.recv_data(recv_data):
            send_data = my_meter.send_data()
            if send_data != None:
                shell_module.my_ser.send_data(send_data)