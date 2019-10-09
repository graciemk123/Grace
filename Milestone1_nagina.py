#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 08:34:08 2019

@author: baw50

Coders: baw50, agw5173,gzk3, dpr5315

Summary: Create cross section maps of potential temperature, horitzontal temperature gradient, 
vertical derivative of potential temperature, and horizontal laplacian
    
Extended Summary:Create N-S, vertical cross sections of variables mentioned above
after computing them using functions found in our myLib library. Cross section can be easily changed
by changing the 'myLon' variable to whatever desired longitude location 
    
    
"""

#Module Imports
import numpy as np 
import myLib_copy as me
from netCDF4 import Dataset
import matplotlib.pyplot as plt

#Configure Program 
#Look at variables in GFS file
filePathAndName = '/ulteosrv2/s0/meteo473Fa19/'+'gfsanl_4_20180630_0000_000.nc'
myVarName = 'TMP'
myVarName2 = 'HGT'
myVarName3 = 'ABSV'
levelList = range(200,1050,50)
tempLevel = range(200,350,5)
levelListDDz = range(250,1000,50)
myLon = 0




#Read a data array
ncfile=Dataset(filePathAndName,'r')
lat=ncfile['latitude'][:]
long=ncfile['longitude'][:]

#Create 3-D array of Absolute Vorticity
ABSV=me.arrayRead(ncfile,myVarName3,levelList)


#Create 3-D array with desired temperature maps 
temp = me.arrayRead(ncfile,myVarName,levelList)


#Create 3-D array with desired heights
hgt = me.arrayRead(ncfile,myVarName2,levelList)


#Compute Potential Temperature 
potentialTemp = me.tmp2theta(temp,levelList)




#Compute d(theta)/d(z)
DDz = me.DDz(potentialTemp,hgt)



# Computing Temperature Gradient
DtempMag =me.horizgradient(temp,long,lat)

#Compute Laplacian
laplacian = me.laplacian(temp,lat,long)


#Make Cross Section Maps
me.crossSection(potentialTemp,lat,long,myLon,levelList,'Potential Temperature Cross Section')
me.crossSection(DtempMag,lat,long,myLon,levelList,'Temperature Gradient Cross Section')
me.crossSection(DDz,lat,long,myLon,levelListDDz,'Vertical Derivative of Theta Cross Section')
me.crossSection(laplacian,lat,long,myLon,levelList,'Laplacian Cross Section')

#Create map of Laplacian in the horizontal 
plt.figure()
#slicing laplacian at one pressure level
tLap = laplacian[15,:,:]
plt.contourf(tLap,200)
plt.title('Laplacian')