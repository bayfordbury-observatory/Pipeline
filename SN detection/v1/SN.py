from __future__ import division, print_function

import numpy as np
#from astropy import wcs
from astropy.io import fits
import sys
from PIL import Image
import math

#prefix of the input images
name="M95"

#width of the output image
width=800

#binning ratios
bin=np.zeros(shape=(5))

bin[1]=0.36
bin[2]=0.36
bin[3]=1.8
bin[4]=3

#open two fits to compare
hdulist1 = fits.open(name+"-1.fit")
hdulist2 = fits.open(name+"-2.fit")

header1=hdulist1[0].header
header2=hdulist2[0].header

exp1=header1['EXPTIME']/100
exp2=header2['EXPTIME']/100


pxsize1=(header1['XPIXSZ']/header1['XBINNING'])*bin[header1['XBINNING']]
pxsize2=(header2['XPIXSZ']/header2['XBINNING'])*bin[header2['XBINNING']]

scidata1 = hdulist1[0].data
scidata2 = hdulist2[0].data

#centre coordinates
cra1=header1['CRVAL1']
cdec1=header1['CRVAL2']

cra2=header2['CRVAL1']
cdec2=header2['CRVAL2']

#average centre coordinate
cx=(cra1+cra2)/2
cy=(cdec1+cdec2)/2

#pixel width of images

xaxis1=header1['NAXIS1']
yaxis1=header1['NAXIS2']

xaxis2=header2['NAXIS1']
yaxis2=header2['NAXIS2']

#plate scale of images

fdec=math.cos(math.radians(cy))

xscale1=header1['CDELT1']/fdec
yscale1=header1['CDELT2']

xscale2=header2['CDELT1']/fdec
yscale2=header2['CDELT2']

#rotation of images

rot1=0-(header1['CROTA1']+header1['CROTA2'])/2
rot2=0-(header2['CROTA1']+header2['CROTA2'])/2

print(rot1)
print(rot2)

#print(scale1)
#print(scale2)

#scale of first image

scaley=yscale1*yaxis1*0.5
scalex=scaley/math.cos(math.radians(cy))

#sine and cosine of position angles

sinr1=math.sin(math.radians(rot1))
cosr1=math.cos(math.radians(rot1))

sinr2=math.sin(math.radians(rot2))
cosr2=math.cos(math.radians(rot2))

#offset of images

cxd1=cx-cra1
cyd1=cy-cdec1

cxd2=cx-cra2
cyd2=cy-cdec2

print(cxd1)
print(cxd2)
print(cyd1)
print(cyd2)


#scaley=0.25/2

#scalex=scaley

#scale of second image

scaley2=scaley/width
scalex2=scalex/width

#create blank images

a1 = np.zeros(shape=(width,width))
a2 = np.zeros(shape=(width,width))

b = np.zeros(shape=(width,width))
c = np.zeros(shape=(width,width))

#approximate background value

bg1 = np.median(scidata1)*0.98
bg2 = np.median(scidata2)*0.98

print (bg1)
print (bg2)

#loop through the pixels (this is probably inefficient)

for (x,y), value in np.ndenumerate(b):
	
	xc=(x-(width/2))*scalex2
	yx=(y-(width/2))*scaley2

	x1=xc+cxd1		
	y1=yx+cyd1
	
	x2=(xaxis1/2)+(x1/xscale1)*cosr1-(y1/yscale1)*sinr1
	y2=(yaxis1/2)+(x1/xscale1)*sinr1+(y1/yscale1)*cosr1	
	
	if x2>0 and x2<=xaxis1 and y2>0 and y2<=yaxis1:
	
		a1[y,x]=((scidata1[int(y2), int(x2)]-bg1)/(pxsize1*exp1))
		
		x1=xc+cxd2		
		y1=yx+cyd2
		
		x2=(xaxis2/2)+(x1/xscale2)*cosr2-(y1/yscale2)*sinr2
		y2=(yaxis2/2)+(x1/xscale2)*sinr2+(y1/yscale2)*cosr2	
		
		
		a2[y,x]=((scidata2[int(y2), int(x2)]-bg2)/(pxsize2*exp2))
		
		if x2>0 and x2<=xaxis2 and y2>0 and y2<=yaxis2 and a1[y,x]<100:
			
			b[y,x]=(a2[y,x]-a1[y,x])/2
			
		else:
			b[y,x]=0
		
		
	else:

		b[y,x]=0
		
for (x,y), value in np.ndenumerate(b):

	try:
		aa = np.array([b[x,y],b[x-1,y],b[x+1,y],b[x,y+1],b[x,y-1],b[x-1,y-1],b[x+1,y+1],b[x-1,y+1],b[x+1,y-1]])
		
		av=np.median(aa)

		if b[x,y]>(av*1.5):
			c[x,y]=av+20
		else:
			c[x,y]=b[x,y]+20
			


	except:
		c[x,y]=b[x,y]+20
		pass		
		

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

		
