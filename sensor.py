# sensor.py
# Contains all the code required for the eclipse sensors.
# Contributors: Elijah Mister, Owen Coffee, and Daniel Geer

import serial
import time
import csv
import os
import smbus
import math

class BMP:
    #BMP Sensor Class: Captures Temperature and Pressure
    #BMP Constants
    BMP085_I2C_ADDRESS = 0x77;
    BMP085_REG_CONTROL = 0xF4;
    BMP085_REG_TEMP = 0xF6;
    BMP085_REG_PRESSURE = 0xF6;
    BMP085_COMMAND_TEMPERATURE = 0x2E;
    BMP085_COMMAND_PRESSURE = 0x34;
    bus = 0
    __active = False
    
    __P0 = 101325; #Pressure at sea level in Pa
    __tempOffset = -16
    __pressureOffset = -67.1
    
    #MIGHT BE REMOVED
    temp_calibration_offset = 0;
    pressure_calibration_offset = 0;
    sea_level_pressure = 101.3; #Actual sea-level pressure
    
    
    def __init__(self):
        #Initalization
        try:
            self.bus = smbus.SMBus(1)
            self.__active = True
        except:
            self.__active = False
    
    def isActive(self):
        return self.__active
        
    def callibrate(self):
        #Performs calibration for temperature and pressure.
        print("NOT SETUP")
    
    #def captureTemp(self):
    #    #Returns temperature reading in F
    #    print("TEMP NOT SETUP")
    #
    #def capturePres(self):
    #    #Returns pressure reading in KPa
    #    print("PRESSURE NOT SETUP")
        
    def getAltitude(pressure:float, temp:float):
        if(pressure == 0):
            return 0
        r = pow((__P0/pressure),(1/5.257))-1
        x = (temp+273.15)
        h = (r*x)/0.0065
        return h #returns in meters
    
    def captureTemp(self):
        self.bus.write_byte_data(self.BMP085_I2C_ADDRESS, self.BMP085_REG_CONTROL, self.BMP085_COMMAND_TEMPERATURE)
        #time.sleep(0.005)  # Wait for temperature conversion
        raw_temp = self.bus.read_word_data(self.BMP085_I2C_ADDRESS, self.BMP085_REG_TEMP)
        raw_temp = ((raw_temp << 8) & 0xFF00) + (raw_temp >> 8)
        x = ((raw_temp - 0x0000) * 0.001)+self.__tempOffset
        print(x)
        return(x)
        #self.__temp_1 = ((raw_temp - 0x0000) * 0.001)  # Celsius
    
    def capturePres(self):
       self.bus.write_byte_data(self.BMP085_I2C_ADDRESS, self.BMP085_REG_CONTROL, self.BMP085_COMMAND_PRESSURE + (3 << 6))
       #time.sleep(0.014) # Wait for pressure conversion
       msb = self.bus.read_byte_data(self.BMP085_I2C_ADDRESS, self.BMP085_REG_PRESSURE)
       lsb = self.bus.read_byte_data(self.BMP085_I2C_ADDRESS, self.BMP085_REG_PRESSURE + 1)
       xlsb = self.bus.read_byte_data(self.BMP085_I2C_ADDRESS, self.BMP085_REG_PRESSURE + 2)
       pressure_raw = ((msb << 16) + (lsb << 8) + xlsb) >> (4)
       return (pressure_raw / 4096.0) # kPa
       #self.__pressure = (pressure_raw / 4096.0) # kPa

class RADsens:
    # giger counter
    # Define the I2C address of the sensor
    RAD_SENS_I2C_ADDR = 0x66
    bus = 0  # 1 indicates the I2C bus number
    __active = False
    
    # Function to read a 16-bit unsigned integer from the sensor
    def read_uint16(self, bus, register):
        data = self.bus.read_i2c_block_data(self.RAD_SENS_I2C_ADDR, register, 2)
        return (data[0] << 8) | data[1]

    # Function to write a 16-bit unsigned integer to the sensor
    def write_uint16(self, bus, register, value):
        self.bus.write_i2c_block_data(self.RAD_SENS_I2C_ADDR, register, [(value >> 8) & 0xFF, value & 0xFF])


    # Initialize the sensor
    def __init__(self):
    # Check sensor wiring and initialize
        try:
            self.bus = smbus.SMBus(1)
            self.__active = True
        except: 
            self.__active = False
        return
        
    def isActive(self):
        return self.__active

    # Setup sensor sensitivity
    def set_sensitivity(self, sensitivity):
        write_uint16(self.bus, 0x00, sensitivity)

    # Setup HV generator state
    def set_hv_generator_state(self, state):
        bus.write_byte(self.RAD_SENS_I2C_ADDR, 0x01 if state else 0x00)

    # Setup LED indication state
    def set_led_state(self, state):
        self.bus.write_byte(self.RAD_SENS_I2C_ADDR, 0x02 if state else 0x00)
    
    def getDynamicRad(self):
        return self.read_uint16(self.bus, 0x03)
    
    def getNumPulses(self):
        return self.read_uint16(self.bus, 0x05)
    
    def getStaticRadPerMin(self):
        #Returns the Static Radiation (60s)
        rad_intensity_static = self.read_uint16(self.bus, 0x04) #Static Radiation (500s)
        return ((rad_intensity_static/500)*60) #Returns Static Radiation (60s)
    
    def getStaticRad(self):
        #Returns the Static Radiation (500s)
        rad_intensity_static = self.read_uint16(self.bus, 0x04) #Static Radiation (500s)
        return rad_intensity_static #Returns Static Radiation (500s)


class MPU6050:
    # MPU for gyroscope and acceleration
    
    I2C_ADDRESS = 0x68;
    bus = 0
    
    def __init__(self):
        try:
            self.bus = smbus.SMBus(1)
            self.__active = True
        except: 
            self.__active = False
        return
        
    def read_uint16(self, bus, register):
        data = self.bus.read_i2c_block_data(self.I2C_ADDRESS, register, 2)
        return (data[0] << 8) | data[1]
    
    def getAccelerationX(self):
        pass
    def getAccelerationY(self):
        pass
    def getAccelerationZ(self):
        pass
    def getGyroX(self):
        pass
    def getGyroY(self):
        pass
    def getGyroZ(self):
        pass
        
        
        
class ADS1115:
    # ADS1115 for the analog to digital
 
    # Define the I2C bus number (0 or 1)
    I2C_BUS = 1

    # Define the address of ADS1015 (default address)
    ADS1015_ADDRESS = 0x48

    # Define the registers
    ADS1015_REG_POINTER_CONVERT = 0x00
    ADS1015_REG_POINTER_CONFIG = 0x01

    # Configuration values for ADS1015
    ADS1015_CONFIG_OS_SINGLE = 0x8000
    ADS1015_CONFIG_MUX_SINGLE_0 = 0x4000  # Channel 0
    ADS1015_CONFIG_MUX_SINGLE_1 = 0x5000  # Channel 1
    ADS1015_CONFIG_MUX_SINGLE_2 = 0x6000  # Channel 2
    ADS1015_CONFIG_MUX_SINGLE_3 = 0x7000  # Channel 3
    ADS1015_CONFIG_PGA_6_144V = 0x0000  # +/-6.144V range
    ADS1015_CONFIG_MODE_SINGLE = 0x0100
    ADS1015_CONFIG_DR_128SPS = 0x0000  # 128 samples per second
    ADS1015_CONFIG_COMP_QUE_DISABLE = 0x0003
    
    # Bus
    bus = smbus.SMBus(I2C_BUS)
    
    
    def __init__(self):
        pass
        
    def read_adc(self, channel):
        # Configuration word
        config = (self.ADS1015_CONFIG_OS_SINGLE |
                  self.ADS1015_CONFIG_MUX_SINGLE_0 |  # Channel 0
                  self.ADS1015_CONFIG_PGA_6_144V |
                  self.ADS1015_CONFIG_MODE_SINGLE |
                  self.ADS1015_CONFIG_DR_128SPS |
                  self.ADS1015_CONFIG_COMP_QUE_DISABLE)

        # Set the channel
        if channel == 0:
            config |= self.ADS1015_CONFIG_MUX_SINGLE_0
        elif channel == 1:
            config |= self.ADS1015_CONFIG_MUX_SINGLE_1
        elif channel == 2:
            config |= self.ADS1015_CONFIG_MUX_SINGLE_2
        elif channel == 3:
            config |= self.ADS1015_CONFIG_MUX_SINGLE_3

        # Write configuration to the ADC
        self.bus.write_i2c_block_data(self.ADS1015_ADDRESS, self.ADS1015_REG_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])

        # Wait for conversion to complete
        time.sleep(0.1)

        # Read the conversion result
        data = self.bus.read_i2c_block_data(self.ADS1015_ADDRESS, self.ADS1015_REG_POINTER_CONVERT, 2)
        value = (data[0] << 8) | data[1]

        # Convert to signed value
        if value & 0x8000:
            value -= 1 << 16

        return value

    def voltage_to_temperature(self, voltage):
        # Calculate resistance of the thermistor
        # Thermistor parameters
        R0 = 10000.0  # Resistance at nominal temperature (in ohms)
        T0 = 25.0     # Nominal temperature (in Celsius)
        beta = 3950.0 # Beta value of the thermistor
        R = R0 / ((3.3 / voltage) - 1.0)
        # Calculate temperature using the Steinhart-Hart equation
        T = 1.0 / (1.0 / (T0 + 273.15) + (1.0 / beta) * math.log(R / R0)) - 273.15
        return T
        
    def adcToVoltage(self, adc_value, max_voltage = 3.3):
        return ((adc_value/17712)*max_voltage)
    
    def getTemp(self, channel):
        adcVal = self.read_adc(channel)
        volt = self.adcToVoltage(adcVal)
        temp = self.voltage_to_temperature(volt)
        return temp
