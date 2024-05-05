import RPi.GPIO as GPIO
import time

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
    #GPIO.output(11, GPIO.HIGH)
    GPIO.output(15, GPIO.HIGH)
    pass

def ledFile():
    #Turns on File Reading LED (RED)
    #GPIO.output(15, GPIO.HIGH)
    GPIO.output(11, GPIO.HIGH)
    pass

GPIO.setmode(GPIO.BOARD) #LED SETUP
#GPIO.setup(11,GPIO.OUT) #BLUE
#GPIO.setup(13,GPIO.OUT) #GREEN
#GPIO.setup(15,GPIO.OUT) #RED

GPIO.setup(15,GPIO.OUT) #BLUE
GPIO.setup(13,GPIO.OUT) #GREEN
GPIO.setup(11,GPIO.OUT) #RED

try:
    while True:
       ledOff()
       ledScript()
       print("GREEN")
       time.sleep(3)
       ledOff()
       ledRB()
       print("BLUE")
       time.sleep(3)
       ledOff()
       ledFile() 
       print("RED")
       time.sleep(3)
except:
    ledOff()
