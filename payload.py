# payload.py
# Contains all the code related to the payload. 
# Contributors: Elijah Mister, Owen Coffee, and Daniel Geer

import serial
import time
import csv
import os
import smbus

class Payload:
    #Payload Class
    #Captures Data on Payload
    
    #Data Variables
    __temp_1 = 0; #Temperature Reading from THERM1
    __temp_2 = 0; #Temperature Reading from THERM2
    __temp_3 = 0; #Temperature Reading from THERM3
    __temp_4 = 0; #Temperature Reading from THERM4
    __pressure = 0; #Pressure Reading from BMP
    __radIntD = 0; #Radiation Intensity Dynamic from Geiger Counter
    __radIntS = 0; #Radiation Intensity Static from Geiger Counter (500s)
    __radIntSPerMin = 0; #Radiation Intensity Static from Geiger Counter (60s)
    __numPulses = 0; #Number of Pulses from Geiger Counter
    
    
    def __init__(self):
        #Initalization
        pass
    
    def updateValue(self, variable, newValue):
        #Updates the variable in the parameter
        if(variable == "temp1"):
            self.__temp_1 = newValue
        elif(variable == "temp2"):
            self.__temp_2 = newValue
        elif(variable == "temp3"):
            self.__temp_3 = newValue
        elif(variable == "temp4"):
            self.__temp_4 = newValue
        elif(variable == "pressure"):
            self.__pressure = newValue
        elif(variable == "radD"):
            self.__radIntD = newValue
        elif(variable == "radS"):
            self.__radIntS = newValue
        elif(variable == "numPulses"):
            self.__numPulses = newValue
        elif(variable == "radSPerMin"):
            self.__radIntSPerMin = newValue
        else:
            print("Not a valid variable.")
            return -1
    
    def grabValue(self, variable):
        #Returns the variable in the parameter.
        if(variable == "temp1"):
            return self.__temp_1
        elif(variable == "temp2"):
            return self.__temp_2
        elif(variable == "temp3"):
            return self.__temp_3
        elif(variable == "temp4"):
            return self.__temp_4
        elif(variable == "pressure"):
            return self.__pressure
        elif(variable == "radD"):
            return self.__radIntD
        elif(variable == "radS"):
            return self.__radIntS
        elif(variable == "radSPerMin"):
            return self.__radIntSPerMin
        elif(variable == "numPulses"):
            return self.__numPulses
        else:
            print("Not a valid variable.")
            return -1
