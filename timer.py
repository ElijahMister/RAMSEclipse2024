# timer.py
# Contains all the code required for the timer.
# Contributors: Elijah Mister, Owen Coffee, and Daniel Geer

import time

class Timer:
    #Timer Class
    #Tracks Time for Payload
    
    #Define Variables
    __target_time = 0;
    __start_time = 0;
    __target = 0;
    __id = 0;
    
    def __init__(self, target=600.0):
        self.__target = target
        self.__start_time = time.time()
        self.__target_time = self.__start_time+target
        self.__id = id(self)
    
    def update(self):
        if(time.time() >= self.__target_time):
            return True
        else:
            return False
        
    def countDown(self):
        print(str(self.__target_time - time.time()))
        
    def getTargetAsString(self):
        return str(self.__target);
        
    def resetTimer(self, target = -1):
        if(target > 0):
            self.__target = target
        self.__start_time = time.time()
        self.__target_time = self.__start_time+self.__target
