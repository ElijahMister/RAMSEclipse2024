# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:34:09 2024

@author: neumo
"""



def getAltitude(pressure:float, temp:float):
    P0 = 101325; #Pa
    if pressure == 0:
        return 0
    r = pow((P0/pressure),(1/5.257))-1
    x = (temp+273.15)
    h = (r*x)/0.0065
    return h


print (getAltitude(101000, 15))