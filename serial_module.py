import serial, time

port_info = {
    'port'     : '/dev/tty.usbserial-A70277IW',
    'bytesize' : 8,
    'parity'   : 'E',
    'stopbits' : 1,
    'baudrate' : 2400,
    'timeout'  : 0,
}

class _serial:
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.l_serial = serial.Serial()
        self.l_serial.port = port
        self.l_serial.baudrate = baudrate
        self.l_serial.bytesize = bytesize
        self.l_serial.parity = parity
        self.l_serial.stopbits = stopbits
        self.l_serial.timeout = timeout
        self.alive = False

    def open(self):
        try:
            self.l_serial.open()
            if self.l_serial.isOpen():
                self.alive = True
                print 'Port is opened success!'
            else:
                self.alive = False
                print 'Port is opened fail!'
        except:
            print 'Port is opened fail!'

    def close(self):
        try:
            self.l_serial.close()
            if self.l_serial.isOpen():
                self.alive = True
                print 'Port is closed fail!'
            else:
                self.alive = False
                print 'Port is closed success!'
        except:
            print 'Port is closed fail!'

    def send_data(self, data):
        data_len = 0
        if self.alive:
            data_len = self.l_serial.write(data)
            return data_len
        else:
            print "Send data fail!"
        return data_len

    def recv_data(self, bytes_time, wait_time):
        buf = ''
        if self.alive:
            tmp_time = 0.0
            valid_flag = False
            start_tm = time.time()
            while True:
                tmp = self.l_serial.inWaiting()
                if tmp > 0:
                    valid_flag = True
                    buf += self.l_serial.read(1)
                    tmp_time = time.time()
                elif valid_flag:
                    if time.time() - tmp_time > bytes_time:
                        break

                if int(time.time() - start_tm) > wait_time:
                    break
        else:
            print "Port is closed!"
        return buf

    def inWaiting(self):
        return self.l_serial.inWaiting()

    def set_port(self, port):
        self.l_serial.setPort(port)

    def set_baudrate(self, baudrate):
        self.l_serial.setBaudrate(baudrate)

    def set_bytesize(self, bytesize):
        self.l_serial.setByteSize(bytesize)

    def get_serial_info(self):
        print self.l_serial

    def get_serial_st(self):
        return self.alive

my_ser = _serial(port_info['port'], port_info['baudrate'], port_info['bytesize'],\
                 port_info['parity'], port_info['stopbits'], port_info['timeout'])






