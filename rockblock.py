# rockblock.py
# Contains all the code required for the rockblock.
# Contributors: Elijah Mister, Owen Coffee, and Daniel Geer

import serial
import time
import csv
import os
import smbus


class Rockblock:
    #Rockblock Class
    #Communication with the RockBlock Device
    serial_port = '/dev/ttyUSB0' #DEFAULT
    ser = 0
    __active = False
    
    
    def __init__(self, serial_port):
        try:
            #Attempt to Open Serial Port
            self.serial_port = serial_port
            self.ser = serial.Serial(self.serial_port, 19200, timeout=1)
            self.ser.flushInput()
            self.ser.flushOutput()
            self.__active = True
        except:
            try:
                #If Serial Port Opened & Failed
                self.ser.close()
                self.__active = False
            except:
                #If Serial Port Failed
                self.__active = False
    
    def checkActive(self):
        try:
            #Attempt to Use Serial Port
            self.ser.flushInput()
            self.ser.flushOutput()
            self.__active = True
        except:
            try:
                #Attempt to Reconnect Serial Port
                self.ser = serial.Serial(self.serial_port, 19200, timeout=1)
                self.ser.flushInput()
                self.ser.flushOutput()
                self.__active = True
            except:
                try:
                    #If Serial Port Opened & Failed
                    self.ser.close()
                    self.__active = False
                except:
                    #If Serial Port Failed
                    self.__active = False
    
    def isActive(self):
        return self.__active
        
    def wait_until_response(self): #keeps reading the input buffer until it gets a signal 
        x = 1 #arbitrary loop flag
        while x == 1:
            y = ''#create empty placeholder
            y = self.ser.readline() #read from serial connection
            print(y) #print(str(y)) which specifies last status message of the RockBLOCK
            if y.startswith("+SBDIX:".encode()) == True:
                x = 0
                return str(y)
            if y.startswith("+SBDS:".encode()) == True:
                x = 0
                return str(y)
            if y == "OK\r".encode() or y == "ERROR\r".encode():
                x = 0
                return str(y)
            return(y)
            
    def test(self):
        self.ser.write("AT\r".encode())
        y = self.wait_until_response()
        if str(y):
            return True
        else: return False
    
    def clearBuffer(self):
        self.ser.write('AT+SBDD0\r'.encode())
        print(self.wait_until_response())
    
    def sendMessage(self, msg):
        message = 'AT+SBDWT=' + msg + '\r' #
        self.ser.write(message.encode()) #write AT command to load message to outbound buffer
        print(self.wait_until_response())
        send = 'AT+SBDIX\r' 
        self.ser.write(send.encode()) #write AT command to send message to Iridium service
        y = self.wait_until_response()
        
        
    def sendTextMessage(self, message, retry:int = 3): #attempt to send a message will try for retry times
        msg = 'AT+SBDWT=' + message + '\r'
        self.ser.write(msg.encode())
        response = self.wait_until_response()
        if response == "OK":
            for i in range(0, retry): #loop until retry value 
                print("retry: "+i) #print retry value in console
                self.ser.write('AT+SBDIX\r') #write AT command to send message
                response = self.wait_until_response() #call wait for response function
                if response.startswith("+SBDIX:"): 
                    response_array = self.parseSDIX(response) #read RockBLOCk response to obtain 
                    if response_array[0] == 0 or response_array[0] == 1 or response_array[0] == 2: 
                        return True
        return False
