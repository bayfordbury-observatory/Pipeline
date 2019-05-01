import astropy
import numpy as np
import sys
#from pylab import *
from astropy.io import fits
from datetime import datetime
startTime = datetime.now()

fitsfile = fits.open(sys.argv[1]+".fit")

print sys.argv[1]+".fit"

header = fitsfile[0].header
data = fitsfile[0].data
 
width=header['NAXIS1']
height=header['NAXIS2']

hdulist1 = fits.open(sys.argv[1]+".all.fit")
tbdata1 = hdulist1[1].data 
header1 = hdulist1[1].header

numstars = header1['NAXIS2']
print(numstars)

print(hdulist1[1].columns)

fluxes= tbdata1['FLUX']
bgs= tbdata1['BACKGROUND']
Xs= tbdata1['X']
Ys= tbdata1['Y']

def residuals(p, y, x):
	A,mu,sigma = p
	
	err = y-A*np.exp(-(x - mu)*(x - mu) / (2 *sigma*sigma) )
	
	return err

 
def GaussFit(x,y): #this could be optimised quite a lot
	best=999999

	
	sig=2.1	
	total1=0
 
	for n in range(0,9):
		 
		y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
		total1+=np.abs((y[n]-y2)*(y[n]-y2))
		
	sig=2.09
	total2=0
 
	for n in range(0,9):
		 
		y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
		total2+=np.abs((y[n]-y2)*(y[n]-y2))
	
	#print total1
	#print total2
	
	if total2 < total1: #go left
	
		for i in range(200,10, -1):
			sig=(float(i)/100)+0.1
	 
			total=0
	 
			for n in range(0,9):
				 
				y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
				total+=np.abs((y[n]-y2)*(y[n]-y2))

			if total<best:
				best=total
			else:
				sig=sig+0.01
				#print sig
				break
	
	else: # go right
	
		for i in range(200,600):
			sig=(float(i)/100)+0.1
	 
			total=0
	 
			for n in range(0,9):
				 
				y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
				total+=np.abs((y[n]-y2)*(y[n]-y2))

			if total<best:
				best=total
			else:
				sig=sig-0.01
				#print sig
				break
 
	return sig
 
 
print str(width)+"x"+str(height)
 
 
 
outname="fwhm.csv"
 
with open(outname, 'w') as file:
    file.write("x,y,flux,fwhm\r\n")
 
rejects="rejects.csv"
 
with open(rejects, 'w') as file:
    file.write("#x,y\r\n")
 
fwhmx=np.zeros(numstars)
fwhmy=np.zeros(numstars)


for i in range(0,numstars):
	x=Xs[i]
	y=Ys[i]
	flux=fluxes[i]
	bg=bgs[i]
	
	
	if flux<50000 and flux>10 and x>5 and x<(width-5) and y>5 and y<(height-5):

		#print str(x)+" "+str(y)
		x0=int(round(x))-1
		y0=int(round(y))-1

		ax = [data[y0,x0-4]-bg,data[y0,x0-3]-bg,data[y0,x0-2]-bg,data[y0,x0-1]-bg,data[y0,x0]-bg,data[y0,x0+1]-bg,data[y0,x0+2]-bg,data[y0,x0+3]-bg,data[y0,x0+4]-bg]
		
		fluxx = [data[y0,x0-4],data[y0,x0-3],data[y0,x0-2],data[y0,x0-1],data[y0,x0],data[y0,x0+1],data[y0,x0+2],data[y0,x0+3],data[y0,x0+4]]


		ay = [data[y0-4,x0]-bg,data[y0-3,x0]-bg,data[y0-2,x0]-bg,data[y0-1,x0]-bg,data[y0,x0]-bg,data[y0+1,x0]-bg,data[y0+2,x0]-bg,data[y0+3,x0]-bg,data[y0+4,x0]-bg]


		axv=[0,1,2,3,4,5,6,7,8]
		ayv=[0,1,2,3,4,5,6,7,8]

		for n in range(0,9):
			axv[n]=round(x-(x0-4+n)-1,3) 
			ayv[n]=round(y-(y0-4+n)-1,3)          

		maxvalx=max(ax)
		maxvaly=max(ay)

		for n in range(0,9):
			ax[n]=round(ax[n]/maxvalx,3)
			ay[n]=round(ay[n]/maxvaly,3)

		#print "BG: "+str(bg)+" Maxval: "+str(maxvalx)+" "+str(maxvaly)
		#print "ax "+str(ax)
		#print "ay "+str(ay)

		#print axv
		#print ayv

		sigx=GaussFit(axv,ax)
		sigy=GaussFit(ayv,ay)
		
		fwhmx[i]=sigx*2.35482
		fwhmy[i]=sigy*2.35482
		
		#print "Sigma="+str(sigx)+","+str(sigy)
		#print "FWHM="+str(round(fwhmx,3))+","+str(round(fwhmy,3))
		#print str(round(fwhmx,3))+","+str(round(fwhmy,3))
		

		
		#print "Ratio: "+str(round(sigx/sigy,3))
			
		#print str(x)+","+str(y)+","+str(fwhmx[i])+","+str(fwhmy[i])

		#string=str(x)+","+str(y)+","+str(flux)+","+str(round(fwhmx[i],3))+"\r\n"
		
		#with open(outname, 'a') as file:
		#	file.write(string)
		#if fwhmx[i]>5:
			#print str(x)+" "+str(y)+" "+str(x0)+" "+str(y0)+" "+str(fwhmx[i])+","+str(fwhmy[i])
			#print ax
			#print axv
			#print fluxx
		#	string=str(x)+","+str(y)+"\r\n"
		#	with open(rejects, 'a') as file:
		#		file.write(string)
		
		#print str(i)+" "+str(x)+" "+str(y)+" "+str(flux)+" "+str(fwhmx[i])+" "+str(fwhmy[i])
		
	#else:
		#print str(i)+" "+str(x)+" "+str(y)+" "+str(flux)


medianx=np.median(fwhmx)            
mediany=np.median(fwhmy)

print medianx
print mediany

th=1.5

lx=medianx/th
ux=medianx*th
ly=medianx/th
uy=medianx*th

for i in range(0,numstars):
	#fwhmx[i]
	#fwhmy[i]

	if fwhmx[i] > fwhmy[i]:
		ratio = fwhmx[i]/fwhmy[i]
	else:
		ratio = fwhmy[i]/fwhmx[i]	
		
	if fwhmx[i]<lx or fwhmy[i]<ly or fwhmx[i]>ux or fwhmy[i]>uy or ratio > 1.5:
		print str(Xs[i])+" "+str(Ys[i])+" "+str(fluxes[i])+" "+str(fwhmx[i])+" "+str(fwhmy[i])
		
		
 
print(datetime.now()-startTime)
#plt.xticks([-4,-3,-2,-1,0,1,2,3,4])
#plt.grid(True)
#plt.show()
