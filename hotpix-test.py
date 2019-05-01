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


print("Running hot pixel filter")


name=sys.argv[1]

hdulist1 = fits.open(name+".fit")

#FITS header
header1=hdulist1[0].header

newheader=header1.copy()

bzero=header1['BZERO']



#exposure time (100s)
exp1=header1['EXPTIME']/200 #200 for M82


#Image data
scidata1 = hdulist1[0].data.astype(np.int32)

#Pixel length of x-axis
xaxis1=header1['NAXIS1']

#Pixel length of y-axis
yaxis1=header1['NAXIS2']

dbid=header1['DBID']

print (dbid)

def printr(x,y):

	aa = np.array([scidata1[y,x],scidata1[y-1,x],scidata1[y+1,x],scidata1[y,x+1],scidata1[y,x-1],scidata1[y-1,x-1],scidata1[y+1,x+1],scidata1[y-1,x+1],scidata1[y+1,x-1],scidata1[y-2,x],scidata1[y+2,x],scidata1[y,x+2],scidata1[y,x-2]])
	aa=np.sort(aa)

	print(str(scidata1[y,x])+" "+str(aa[0])+" "+str(aa[1])+" "+str(aa[2])+" "+str(aa[3])+" "+str(aa[4])+" "+str(aa[5])+" "+str(aa[6])+" "+str(aa[7])+" "+str(aa[8])+" "+str(aa[9])+" "+str(aa[10])+" "+str(aa[11])+" "+str(aa[12]))


print ("cp")
import csv
with open('cp.csv', 'rb') as csvfile:
	file = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in file:
		printr(int(row[0]),int(row[1]))
print ("hp")
import csv
with open('hp.csv', 'rb') as csvfile:
	file = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in file:
		printr(int(row[0]),int(row[1]))
print ("cr")
import csv
with open('cr.csv', 'rb') as csvfile:
	file = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in file:
		printr(int(row[0]),int(row[1]))
print ("star")
import csv
with open('star.csv', 'rb') as csvfile:
	file = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in file:
		printr(int(row[0]),int(row[1]))
print("normal")
import csv
with open('norm.csv', 'rb') as csvfile:
	file = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in file:
		printr(int(row[0]),int(row[1]))





