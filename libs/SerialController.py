import datetime
from threading import Thread
from time import sleep

from serial import Serial
import serial.tools.list_ports


class SerialController:
    def __init__(self, socket):
        self.socket      = socket
        self._port       = "/dev/ttyUSB0"
        self.__baud      = 115200
        self.__timeout   = 1
        self.__rtscts    = True
        # self.__conn      = Serial(self._port, self.__baud, timeout=self.__timeout, rtscts=self.__rtscts)
        self.__connection = False
        self.connect()
        Thread(target=self.readSerial).start()
    
    def connect(self):
        if(not self.__connection):
            self.__connection = True
            self.__conn = Serial(self._port, self.__baud, timeout=self.__timeout, rtscts=self.__rtscts)
    
    def disconnect(self):
        if(self.__connection):
            self.__conn.close()
            self.__connection = False

    def readSerial(self):
        while(self.__connection):
            if(self.__conn.in_waiting > 0):
                data = self.__conn.readline()
                print(data.decode("utf-8"))
                self.socket.sendMsg("message", data.decode("utf-8").strip())

    def reset(self):
        if (self.__connection):
            self.__conn.setDTR(0)
            sleep(1)
            self.__conn.setDTR(1)
            sleep(3)

    def writeToSerial(self, line):
        try:
            line = line+"\n"
            line = line.encode('utf-8')
            self.__conn.write(line)
            return "success"
        except Exception as e:
            print(str(e))
            return "Error"


# class SerialData:
#     def __init__(self):
#         self.data = 

if __name__ == '__main__':
    a = SerialConnection()
    a.connection()