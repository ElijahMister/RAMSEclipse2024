# mainEF.py
# The main file for the Solar Eclipse 2024 Mission for Capitol Technology University
# Contributors: Elijah Mister, Owen Coffee, and Daniel Geer

#Import all needed libraries
import serial
import time
import csv
import os
import smbus
import RPi.GPIO as GPIO

#Import Payload .py Files
import payload
import filehandler
import sensor
import rockblock
import timer

#Functions      
def ledOff():
    #Turns all LEDs Off
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    
def ledScript():
    #Turns on Script LED (GREEN)
    GPIO.output(13, GPIO.HIGH)
    pass

def ledRB():
    #Turns on RockBlock LED (BLUE)
    GPIO.output(15, GPIO.HIGH)
    pass

def ledFile():
    #Turns on File Reading LED (RED)
    GPIO.output(11, GPIO.HIGH)
    pass
    

#Main Script
print("mainEF.py START")

#Creating Variables/Classes
p = payload.Payload() #Payload
rb = rockblock.Rockblock('/dev/ttyUSB0') # RockBlock
tps = sensor.BMP() #Temperature and Pressure Sensor
fh = filehandler.Filehandler("EclipseFlight_Data_") #Filehandler
t = timer.Timer(2) #Timer for 2 Seconds
rs = sensor.RADsens() #Radsens Sensor
therm = sensor.ADS1115() #Thermistors
GPIO.setmode(GPIO.BOARD) #LED SETUP
GPIO.setup(15,GPIO.OUT) #BLUE
GPIO.setup(13,GPIO.OUT) #GREEN
GPIO.setup(11,GPIO.OUT) #RED
stopAt = 1000 #Program Stops at this File Number
startTime = time.time() # Time at startup

# Calibrate Sensors
print("STARTING INSTRUMENT CALIBRATION")

#Setting Up LED
ledOff() #Reset LED Status

#File Set Up
print("File Calibration...")
if(fh.getLastFile() != 0):
    fh.setFileIndex(fh.getLastFile() + 1)

#Calibration Completed
print("Calibration Complete.")

#Ready to Start | Starting Loop
print("READY!\n------")

while True:
    #SET LED STATUS
    ledOff() #Reset Previous Status
    if(rb.isActive()):
        ledRB() #ROCKBLOCK ON
    else:
        ledScript() #ROCKBLOCK OFF
    
    #Capture Values
    if(tps.isActive()):
        try:
            #TPS WORKING
            #p.updateValue("temp1", tps.captureTemp())
            p.updateValue("pressure", tps.capturePres())
        except:
            #TPS FAILED
            #p.updateValue("temp1", -1)
            p.updateValue("pressure", -1)
    else:
        #TPS NOT ACTIVE
        #p.updateValue("temp1", -2)
        p.updateValue("pressure", -2)
        
    if(rs.isActive()):
        try:
            #RADSENS WORKING
            p.updateValue("radD", rs.getDynamicRad())
            p.updateValue("radS", rs.getStaticRad())
            p.updateValue("numPulses", rs.getNumPulses())
            p.updateValue("radSPerMin", rs.getStaticRadPerMin())
        except:
            #RADSENS FAILED
            p.updateValue("radD", -1)
            p.updateValue("radS", -1)
            p.updateValue("numPulses", -1)
            p.updateValue("radSPerMin", -1)
    else:
        #RADSENS NOT ACTIVE
        p.updateValue("radD", -1)
        p.updateValue("radS", -2)
        p.updateValue("numPulses", -2)
        p.updateValue("radSPerMin", -2)
    
    #THERMISTOR READING
    try:
        p.updateValue("temp1", therm.getTemp(0))
        p.updateValue("temp2", therm.getTemp(1))
        p.updateValue("temp3", therm.getTemp(2))
        p.updateValue("temp4", therm.getTemp(3))
    except:
        p.updateValue("temp1", -1)
        p.updateValue("temp2", -1)
        p.updateValue("temp3", -1)
        p.updateValue("temp4", -1)
    
    
    #Save Line of Data
    if(t.update() == True):
        try:
            #Attempting to Write to File
            t.resetTimer(2)
            fh.writeDataToFile(p,startTime)
            print("Line Inserted " + str(fh.getLineIndex()) + " | Timer: " + str(time.time() - startTime))
        except:
            #Failed to Write to File
            t.resetTimer(2)
            ledOff()
            ledFile()
            ledRB()
            ledScript()
            print("Failed to Insert Line " + str(fh.getLineIndex()) + " | Timer: " + str(time.time() - startTime))
    
    #Save Line Data to File
    if(fh.getLineIndex() >= 10):
        try:
            #Attempting to Save to File
            ledOff() #Reset LED Status
            ledFile() #Turn File LED On
            fh.closeAndStartNewFile()
            print("Saved File " + str(fh.getFileIndex() - 1) + " | Timer: " + str(time.time() - startTime))
        except:
            #Failed to Save to File
            ledOff()
            ledFile()
            ledRB()
            ledScript()
            print("Failed to Save File " + str(fh.getFileIndex() - 1) + " | Timer: " + str(time.time() - startTime))
            
    
    #Send RockBlock Message
    if(fh.getFileIndex() % 5 == 0 and fh.getLineIndex() == 1):
        if(rb.isActive()):
            calcTime = time.time() - startTime
            rb_msg = "{:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format(float(calcTime), float(p.grabValue("temp1")), float(p.grabValue("temp2")), float(p.grabValue("temp3")), float(p.grabValue("temp4")), float(p.grabValue("pressure")), float(p.grabValue("radSPerMin"))) #Constructs Message for RockBlock
            msgSent = rb.sendMessage(rb_msg) #Attempts to Send Message
            print("RockBlock Message Sent | " + rb_msg)
        else:
            print("RockBlock Message NOGO")
    
    #Checks to End Program DEBUG
    if(fh.getFileIndex() == stopAt):
        break
    
    #Wait
    rb.checkActive() #Finds the current status of the RockBlock
    time.sleep(1)
