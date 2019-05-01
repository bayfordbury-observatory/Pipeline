from __future__ import division, print_function

import numpy as np
#from numpy import int16
#from numpy import uint16
#import ctypes
#from numpy.ctypeslib import ndpointer
from astropy.io import fits
import sys
#import Image
#import math


name="M82"

hdulist1 = fits.open(name+"-1.fit")

headercopy=fits.getheader(name+"-1.fit")

try:
	print ("bzero: "+str(hdulist1[0].header['BZERO']))
except:
	print ("bzero: gone")
	pass
	
header1=hdulist1[0].header
#headercopy=header1.copy()
data = hdulist1[0].data

try:
	print ("bzero: "+str(headercopy['BZERO']))
except:
	print ("bzero: gone")
	pass





xaxis1=header1['NAXIS1']
yaxis1=header1['NAXIS2']



a1 = data.copy()

max = -10000000
min = 1000000


for x in range(0, xaxis1):
	for y in range(0, yaxis1):

		#a1[y,x]=data[y,x]+100
		
		
		if data[y,x]<min:
			min = data[y,x]
		if data[y,x]>max:
			max = data[y,x]

		

print("min: "+str(min))
print("max: "+str(max))



out = fits.PrimaryHDU(a1, headercopy)
out.header['BZERO']=32768
out.header['BSCALE']=1
#out.header['BITPIX']=16

try:
	print ("bzero: "+str(out.header['BZERO']))
except:
	print ("bzero: gone")
	pass


out.writeto('new.fit', clobber=True)

try:
	print ("bzero: "+str(out.header['BZERO']))
except:
	print ("bzero: gone")
	pass
	
hdulist1 = fits.open('new.fit')
header1=hdulist1[0].header

try:
	print ("bzero: "+str(header1['BZERO']))
except:
	print ("bzero: gone")
	pass