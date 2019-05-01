import astropy
import numpy as np
import sys
#from pylab import *
from astropy.io import fits
from datetime import datetime
startTime = datetime.now()
from scipy.optimize import leastsq

fitsfile = fits.open(sys.argv[1]+".fit")

#print sys.argv[1]+".fit"

header = fitsfile[0].header
data = fitsfile[0].data
 
width=header['NAXIS1']
height=header['NAXIS2']

hdulist1 = fits.open(sys.argv[1]+".all.fit")
tbdata1 = hdulist1[1].data 
header1 = hdulist1[1].header

numstars = header1['NAXIS2']
#print(numstars)

#print(hdulist1[1].columns)

fluxes= tbdata1['FLUX']
bgs= tbdata1['BACKGROUND']
Xs= tbdata1['X']
Ys= tbdata1['Y']

def residualsfixed(p, y, x, max):
	mu,sigma = p
	
	err = y-max*np.exp(-(x - mu)*(x - mu) / (2 *sigma*sigma) )
	
	return err

	
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
 
ax=np.zeros(36)
axv=np.zeros(36)


fwhm=np.zeros(numstars)


for i in range(0,numstars):
	x=Xs[i]
	y=Ys[i]
	flux=fluxes[i]
	bg=bgs[i]
	
	total=flux+bg
	
	
	if total<65000 and flux>10 and x>5 and x<(width-5) and y>5 and y<(height-5):

		#print str(x)+" "+str(y)
		x0=int(round(x))-1
		y0=int(round(y))-1

		k=0
		m=0
		for n in range (-4, 5):
			#k=(n+4)*9+m+4
			#print str(n)+" "+str(m)+" "+str(k)
			
			ax[k]=data[y0+m,x0+n]-bg
			if n<0:
				axv[k]=0-np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			else:
				axv[k]=np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			k=k+1

		
		n=0
		for m in range (-4, 5):
			#k=(n+4)*9+m+4
			#print str(n)+" "+str(m)+" "+str(k)
			
			ax[k]=data[y0+m,x0+n]-bg
			if m<0:
				axv[k]=0-np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			else:
				axv[k]=np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			k=k+1
				
		for m in range (-4, 5):
			n=m
			#k=(n+4)*9+m+4
			#print str(n)+" "+str(m)+" "+str(k)
			
			ax[k]=data[y0+m,x0+n]-bg
			if m<0:
				axv[k]=0-np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			else:
				axv[k]=np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			k=k+1	

		for m in range (4, -5,-1):
			n=m
			#k=(n+4)*9+m+4
			#print str(n)+" "+str(m)+" "+str(k)
			
			ax[k]=data[y0+m,x0+n]-bg
			if m<0:
				axv[k]=0-np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			else:
				axv[k]=np.sqrt((y0+m-y+1)*(y0+m-y+1)+(x0+n-x+1)*(x0+n-x+1))
			k=k+1

		#print "BG: "+str(bg)+" Maxval: "+str(maxval)+" "+str(maxvaly)
		#print "ax "+str(ax)
		#print "ay "+str(ay)

		#print axv
		#print ayv
		
		maxval=max(ax)

		
		p0 = [maxval, 0, 1]
		plsq = leastsq(residuals, p0, args=(ax, axv))

		p0 = [0, 1]
		plsqfix = leastsq(residualsfixed, p0, args=(ax, axv, maxval))

		fwhmfix=plsqfix[0][1]*2.35482
		
		fwhm[i]=plsq[0][2]*2.35482
		
		
		flux2=plsq[0][0]
		
		ratio=maxval/flux2
		
		if ratio < 0.8 or ratio >1.6:
			fwhm[i]=0
		
		#print "Sigma="+str(sigx)+","+str(sigy)
		#print "FWHM="+str(round(fwhm,3))+","+str(round(fwhm,3))
		#print str(round(fwhm,3))+","+str(round(fwhm,3))
		

		
		#print "Ratio: "+str(round(sigx/sigy,3))
			
		#print str(x)+","+str(y)+","+str(fwhm[i])+","+str(fwhm[i])

		#string=str(x)+","+str(y)+","+str(flux)+","+str(round(fwhm[i],3))+"\r\n"
		
		#with open(outname, 'a') as file:
		#	file.write(string)
		#if fwhm[i]>5:
			#print str(x)+" "+str(y)+" "+str(x0)+" "+str(y0)+" "+str(fwhm[i])+","+str(fwhm[i])
			#print ax
			#print axv
			#print fluxx
		#	string=str(x)+","+str(y)+"\r\n"
		#	with open(rejects, 'a') as file:
		#		file.write(string)
		
		#print str(i)+" "+str(x)+" "+str(y)+" "+str(flux)+" "+str(fwhm[i])+" "+str(fwhm[i])
		
	#else:
		#print str(i)+" "+str(x)+" "+str(y)+" "+str(flux)


median=np.median(fwhm) 

print median

th=1.6

lx=median/th
ux=median*th

print ("lower limit: " +str(lx))
print ("upper limit: " +str(ux))

for i in range(0,numstars):
	#fwhm[i]
	#fwhm[i]

		
	if fwhm[i]<lx or fwhm[i]>ux :
		#print "rejected: "+str(Xs[i])+" "+str(Ys[i])+" "+str(fluxes[i])+" "+str(fwhm[i])+" "+str(fwhm[i])
		string=str(Xs[i])+","+str(Ys[i])+"\r\n"
		with open(rejects, 'a') as file:
			file.write(string)
		
		
 
#print(datetime.now()-startTime)
#plt.xticks([-4,-3,-2,-1,0,1,2,3,4])
#plt.grid(True)
#plt.show()
