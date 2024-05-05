# filehandler.py
# Contains all the code required for the file handler.
# Contributors: Elijah Mister, Owen Coffee, and Daniel Geer

import serial
import time
import csv
import os
import smbus

class Filehandler:
    #File Handler Class
    #Creation of Files for Payload
    
    #Variables
    __file_index = 0;
    __file_name = "";
    __csv_file = None;
    __csv_writer = None;
    __line_index = 0;
    __filetype = ".csv";
    __dir = "/home/solar/Desktop/EclipseFiles/Data/";
    #__dir = "/media/solar/JAHDRIVE/EclipseFlightData"
    
    def __init__(self, name, directory = None):
        self.__file_name = name
        if directory != None:
            self.__dir = directory
        
        self.__csv_file = open(self.__dir+self.__file_name+str(self.__file_index)+self.__filetype, 'w', newline='')
    
    def writeDataToFile(self, payload, startTime):
        self.__csv_writer = csv.writer(self.__csv_file)
        calcTime = int((time.time()-startTime) * 1000) #Saves 3 Decimal Places
        calcTime = calcTime / 1000 #Converts Back to Decimal
        self.__csv_writer.writerow([calcTime, payload.grabValue("temp1"), payload.grabValue("temp2"), payload.grabValue("temp3"), payload.grabValue("temp4"), payload.grabValue("pressure"), payload.grabValue("radD"), payload.grabValue("radS"), payload.grabValue("numPulses"),payload.grabValue("radSPerMin")])
        self.__line_index += 1
    
    def closeFile(self):
        self.__csv_file.close()
    
    def closeAndStartNewFile(self):
        self.__csv_file.close()
        self.__line_index = 0
        self.__file_index = self.__file_index+1 
        self.__csv_file = open(self.__dir+self.__file_name+str(self.__file_index)+self.__filetype, 'w', newline='')
    
    def getLineIndex(self):
        return self.__line_index
    
    def getFileIndex(self):
        return self.__file_index
    
    def getLastFile(self):
        #Finds the last saved file.
        #folder_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the Python script
        
        # List all files in the directory
        files = os.listdir(self.__dir)
        
        # Filter files based on the naming pattern
        relevant_files = [file for file in files if file.startswith(self.__file_name)]
        
        if not relevant_files:
            print("No relevant files found.")
            return 0
        
        # Extract sequence numbers and find the maximum
        sequence_numbers = [int(file.split("_")[-1].split(".")[0]) for file in relevant_files]
        max_sequence_number = max(sequence_numbers)
        
        return max_sequence_number
    
    def setFileIndex(self, newIndex):
        #Sets a new file index. Opens a folder that starts at that index.
        self.__file_index = newIndex
        self.__csv_file = open(self.__dir+self.__file_name+str(self.__file_index)+self.__filetype, 'w', newline='')
    
