from __future__ import division, print_function

import numpy as np
from astropy import wcs
from astropy.io import fits
import sys
import Image
import math

fname1="M95-1"
fname2="M95-2"

hdulist1 = fits.open(fname1+".fit")
hdulist2 = fits.open(fname2+".fit")

exp1=hdulist1[0].header['EXPTIME']/100
exp2=hdulist2[0].header['EXPTIME']/100

print (exp1)
print (exp2)

w1 = wcs.WCS(hdulist1[0].header)
w2 = wcs.WCS(hdulist2[0].header)

scidata1 = hdulist1[0].data
scidata2 = hdulist2[0].data

pix=800

#cx=149.000771848
#cy=69.6782129039

cx=160.989103461
cy=11.7012966458

scaley=0.25/2
scalex=scaley/math.cos(math.radians(cy))

wx=np.linspace(cx-scalex, cx+scalex, pix, 1)
wy=np.linspace(cy-scaley, cy+scaley, pix, 1)

px1, py1 = w1.wcs_world2pix(wx, wy, 1)
px2, py2 = w2.wcs_world2pix(wx, wy, 1)

#px1, py1 = w1.all_world2pix(wx, wy, 0, tolerance=5e-1)
#px2, py2 = w2.all_world2pix(wx, wy, 0, tolerance=5e-1)


a1 = np.zeros(shape=(pix,pix))
a2 = np.zeros(shape=(pix,pix))
b = np.zeros(shape=(pix,pix))

bg1 = np.median(scidata1)*0.95
bg2 = np.median(scidata2)*0.95

print (bg1)
print (bg2)

for (x,y), value in np.ndenumerate(b):

	try:
		a1[pix-y-1,pix-x-1] = ((scidata1[py1[y], px1[x]]-bg1)/exp1)/5
	except:
		a1[pix-y-1,pix-x-1]=0
		pass
	
	try:
		a2[pix-y-1,pix-x-1] = ((scidata2[py2[y], px2[x]]-bg2)/exp2)/5
	except:
		a2[pix-y-1,pix-x-1]=0
		pass	
	
	
	b[pix-y-1,pix-x-1]=((a2[pix-y-1,pix-x-1]-a1[pix-y-1,pix-x-1])/2)+50
		
#bg = np.median(b)		
		

#for (x,y), value in np.ndenumerate(b):
#
#	try:
#		aa = np.array([b[x-1,y],b[x+1,y],b[x,y+1],b[x,y-1],b[x-1,y-1],b[x+1,y+1],b[x-1,y+1],b[x+1,y-1]])
#
#		median=np.median(aa)
#	
#		if b[x,y]>(median*1.5):
#			b[x,y]=median
#			
#		if b[x,y]<(median/1.5):
#			b[x,y]=median
#		
#		if b[x,y]<(bg*0.9):
#			b[x,y]=bg
#
#	except:
#		pass
	

im = Image.fromarray(b)
im1 = Image.fromarray(a1)
im2 = Image.fromarray(a2)

im = im.convert('RGB')
im1 = im1.convert('RGB')
im2 = im2.convert('RGB')

im.save("/var/www/sn-dif.jpg")
im1.save("/var/www/sn1.jpg")
im2.save("/var/www/sn2.jpg")

		
