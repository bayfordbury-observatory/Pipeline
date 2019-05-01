import astropy
import sys
import math
from astropy.io import fits
import numpy


fitsfile = fits.open(sys.argv[1]+".fit")

header = fitsfile[0].header
data = fitsfile[0].data
 
width=header['NAXIS1']
height=header['NAXIS2']

hdulist1 = fits.open(sys.argv[1]+".all.fit")
tbdata1 = hdulist1[1].data 
header1 = hdulist1[1].header

hdulist2 = fits.open("nomad.all.fit")
tbdata2 = hdulist2[1].data 
header2 = hdulist2[1].header

print(hdulist2[1].columns)

rows1 = header1['NAXIS2']
print(rows1)

rows2 = header2['NAXIS2']
print(rows2)


fluxes= tbdata1['FLUX']
Xs= tbdata1['X']
Ys= tbdata1['Y']
nomadX= tbdata2['X']
nomadY= tbdata2['Y']

names= tbdata2['NOMAD1']
vmag= tbdata2['Vmag']
rmag= tbdata2['Rmag']

#print(Xs)
#print(nomadX)


for i in range(0,rows1):
	x=Xs[i]
	y=Ys[i]
	match=0
	for j in range(0,rows2):
		xn=nomadX[j]
		yn=nomadY[j]
		dx=xn-x
		dy=yn-y
		dist=math.sqrt(dx*dx+dy*dy)
		if dist<2:
			#print (str(x)+" "+str(y)+" "+str(xn)+" "+str(yn)+" "+names[j]+" "+str(vmag[j])+" "+str(fluxes[i]))
			print (str(rmag[j])+" "+str(fluxes[i]))
			match=1
			break

	if match==0:
		print("0 "+str(fluxes[i]))


