from __future__ import division, print_function

import numpy as np
import ctypes
from numpy.ctypeslib import ndpointer
from astropy.io import fits
import sys
from PIL import Image
import math

lib = ctypes.cdll.LoadLibrary("/mnt/c/Users/David/OneDrive - University of Hertfordshire/GitHub/pipeline/SN detection/v2/py.so")
fun = lib.cfun
fun.restype = None
fun.argtypes =[ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ndpointer(ctypes.c_float),ndpointer(ctypes.c_float),ndpointer(ctypes.c_float),ndpointer(ctypes.c_float),ndpointer(ctypes.c_float)]
fun.restype = ctypes.c_int


name="M95"

#m82
#cx=149.0
#cy=69.7

#nv
#cx=305.9
#cy=20.8

#m95
#cx=161
#cy=11.7

bin=np.zeros(shape=(5))

bin[1]=0.36
bin[2]=0.36
bin[3]=1.8
bin[4]=3

hdulist1 = fits.open(name+"-1.fit")
hdulist2 = fits.open(name+"-2.fit")

#FITS header
header1=hdulist1[0].header
header2=hdulist2[0].header

#exposure time (100s)
exp1=header1['EXPTIME']/100
exp2=header2['EXPTIME']/100

#Effective pixel scalar size
pxsize1=(header1['XPIXSZ']/header1['XBINNING'])*bin[header1['XBINNING']]
pxsize2=(header2['XPIXSZ']/header2['XBINNING'])*bin[header2['XBINNING']]

#Image data
scidata1 = hdulist1[0].data.astype(np.float32)
scidata2 = hdulist2[0].data.astype(np.float32)

#Centre of image in RA
cra1=header1['CRVAL1']
cra2=header2['CRVAL1']

#Centre of image in Dec
cdec1=header1['CRVAL2']
cdec2=header2['CRVAL2']

#average centre in RA and Dec
cx=(cra1+cra2)/2
cy=(cdec1+cdec2)/2

#Pixel length of x-axis
xaxis1=header1['NAXIS1']
xaxis2=header2['NAXIS1']

#Pixel length of y-axis
yaxis1=header1['NAXIS2']
yaxis2=header2['NAXIS2']

#scaling in angular size on sky due to declination
fdec=math.cos(math.radians(cy))

#pixel scale in deg/pixel
xscale1=header1['CDELT1']/fdec
yscale1=header1['CDELT2']

xscale2=header2['CDELT1']/fdec
yscale2=header2['CDELT2']

#rotation of image
rot1=0-(header1['CROTA1']+header1['CROTA2'])/2
rot2=0-(header2['CROTA1']+header2['CROTA2'])/2

#output image dimensions
pix=1000

#output scale
scaley2=0.00027777777 #(1"/pix)

#pix=int((10/60)/scaley2)

scalex2=scaley2/math.cos(math.radians(cy))

#sin and cos of image rotation angle
sinr1=math.sin(math.radians(rot1))
cosr1=math.cos(math.radians(rot1))

sinr2=math.sin(math.radians(rot2))
cosr2=math.cos(math.radians(rot2))

#difference from input image centre to output image centre
cxd1=cx-cra1
cxd2=cx-cra2

cyd1=cy-cdec1
cyd2=cy-cdec2

#Initial array
a1 = np.zeros((pix,pix),dtype="float32")
a2 = np.zeros((pix,pix),dtype="float32")

b = np.zeros((pix,pix),dtype="float32")
c = np.zeros((pix,pix),dtype="float32")

#background value of input images
bg1 = np.median(scidata1)*0.95
bg2 = np.median(scidata2)*0.95

print("rot1 "+str(rot1))
print("rot2 "+str(rot2))

print("cxd1 "+str(cxd1))
print("cxd2 "+str(cxd2))
print("cyd1 "+str(cyd1))
print("cyd2 "+str(cyd2))

print ("bg2 "+str(bg1))
print ("bg2 "+str(bg2))

print ("xaxis1 "+str(xaxis1))
print ("xaxis2 "+str(xaxis2))
print ("yaxis1 "+str(yaxis1))
print ("yaxis2 "+str(yaxis2))

print ("scalex2 "+str(scalex2))
print ("scaley2 "+str(scaley2))

#background subtract input images and scale according to exposure time and pixel size
scidata1=(np.array(scidata1)-bg1)/(pxsize1*exp1)
scidata2=(np.array(scidata2)-bg2)/(pxsize2*exp2)

print ("running")

sncount=fun(pix, xaxis1, xaxis2, yaxis1, yaxis2, scalex2, scaley2, xscale1, xscale2, yscale1, yscale2, cxd1, cyd1, cxd2, cyd2, sinr1, sinr2, cosr1, cosr2, scidata1, scidata2, a1, a2, b)

print ("sn pix count: "+str(sncount))

#print (scidata1)
#print (a1)
#print (a2)

a1=np.fliplr(a1)
a1=np.flipud(a1)

a2=np.fliplr(a2)
a2=np.flipud(a2)
	
b=np.fliplr(b)
b=np.flipud(b)

c=np.array(b)+20

print ("outputting images")

im = Image.fromarray(c)
im1 = Image.fromarray(a1)
im2 = Image.fromarray(a2)

im = im.convert('RGB')
im1 = im1.convert('RGB')
im2 = im2.convert('RGB')

im.save(name+"-dif.png")
im1.save(name+"-1.jpg")
im2.save(name+"-2.jpg")

		
