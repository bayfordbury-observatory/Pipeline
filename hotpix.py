from __future__ import division, print_function

import numpy as np
from numpy import int16
from numpy import uint16
import ctypes
from numpy.ctypeslib import ndpointer
from astropy.io import fits
import sys
import Image
import math
from datetime import datetime

lib = ctypes.cdll.LoadLibrary("hotpix2.so")
fun = lib.cfun
fun.restype = None
fun.argtypes =[ctypes.c_int,ctypes.c_int,ctypes.c_int,ndpointer(ctypes.c_int),ndpointer(ctypes.c_int)]

name=sys.argv[1]

hdulist1 = fits.open(name+".fit")

#FITS header
header1=hdulist1[0].header

#Image data
scidata1 = hdulist1[0].data.astype(np.int32)

#Pixel length of x-axis
xaxis1=header1['NAXIS1']

#Pixel length of y-axis
yaxis1=header1['NAXIS2']

print (xaxis1)#0
print (yaxis1)#1

print (header1['TSCOPEID'])#2
print (header1['EXPTIME'])#3
print (header1['FILTER'])#4
print (header1['XBINNING'])#5
print (header1['EGAIN'])#6
print (header1['XPIXSZ'])#7
print (header1['FOCALLEN'])#8

crval1=header1.get('CRVAL1', 720)#9
print (crval1)
if crval1<720:
	print (header1['CRVAL2'])#10
	print (header1['FWHM'])#11


#Initial array
a1 = scidata1.copy()

#Cold pixel must be below this sigma value, and hot pixel must be above 2x this value
strength=5

startTime = datetime.now()
fun(strength, xaxis1,  yaxis1, scidata1, a1)
print(datetime.now()-startTime)

out = fits.PrimaryHDU(int16(a1), header1)

out.scale('int16', bzero=32768)

	
out.writeto(sys.argv[1]+".hpf.fit", clobber=True)

