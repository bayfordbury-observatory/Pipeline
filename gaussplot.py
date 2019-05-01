import astropy
import numpy
from pylab import *
from astropy.io import fits


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
 
 


def plotGauss(sig,plt, col):
     
    x=np.arange(-5,5,0.1)
    y=np.arange(-5,5,0.1)
    for i in range(0,100):
        x[i]=round(x[i],1)
        y[i]=np.exp(-(x[i]*x[i]) / (2 * sig*sig))  
    #print x
    plt.plot(x,y, color=col)
    return 0
 
 
def GaussFit(x,y): #this could be optimised quite a lot
	best=999999
	sig=2.1	
	total1=0
 
	for n in range(0,11):
		 
		y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
		total1+=np.abs((y[n]-y2)*(y[n]-y2))
		
	sig=2.09
	total2=0
 
	for n in range(0,11):
		 
		y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
		total2+=np.abs((y[n]-y2)*(y[n]-y2))
	
	#print total1
	#print total2
	
	if total2 < total1: #go left
	
		for i in range(200,10, -1):
			sig=(float(i)/100)+0.1
	 
			total=0
	 
			for n in range(0,11):
				 
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
	 
			for n in range(0,11):
				 
				y2=np.exp(-(x[n]*x[n]) / (2 * sig*sig))
				total+=np.abs((y[n]-y2)*(y[n]-y2))

			if total<best:
				best=total
			else:
				sig=sig-0.01
				#print sig
				break
 	#print "Best: " +str(best)
	return sig
 
print "Dimensions: "+str(width)+"x"+str(height)
 

n=0

fwhmx=np.zeros(numstars)
fwhmy=np.zeros(numstars)

for i in range(0,numstars):
	x=Xs[i]
	y=Ys[i]
	flux=fluxes[i]
	bg=bgs[i]
	
	
	if flux<55000 and flux>10 and x>5 and x<(width-5) and y>5 and y<(height-5):
	
	
		from datetime import datetime
		startTime = datetime.now()
             
		#print "Coord: "+str(x)+" "+str(y)
		x0=int(round(x))-1
		y0=int(round(y))-1


		ax = [data[y0,x0-5]-bg,data[y0,x0-4]-bg,data[y0,x0-3]-bg,data[y0,x0-2]-bg,data[y0,x0-1]-bg,data[y0,x0]-bg,data[y0,x0+1]-bg,data[y0,x0+2]-bg,data[y0,x0+3]-bg,data[y0,x0+4]-bg,data[y0,x0+5]-bg]
		
		ay = [data[y0-5,x0]-bg,data[y0-4,x0]-bg,data[y0-3,x0]-bg,data[y0-2,x0]-bg,data[y0-1,x0]-bg,data[y0,x0]-bg,data[y0+1,x0]-bg,data[y0+2,x0]-bg,data[y0+3,x0]-bg,data[y0+4,x0]-bg,data[y0+5,x0]-bg]


		axv=[0,1,2,3,4,5,6,7,8,9,10]
		ayv=[0,1,2,3,4,5,6,7,8,9,10]

		for n in range(0,11):
			axv[n]=round(x-(x0-5+n)-1,3)
			ayv[n]=round(y-(y0-5+n)-1,3)         

		maxvalx=max(ax)
		maxvaly=max(ay)

		for n in range(0,11):
			ax[n]=round(ax[n]/maxvalx,3)
			ay[n]=round(ay[n]/maxvaly,3)

		
		#print "BG: "+str(bg)+" Maxval: "+str(maxvalx)+" "+str(maxvaly)
		#print "ax "+str(ax)
		#print " ay "+str(ay)

		#print axv
		#print ayv

		sigx=GaussFit(axv,ax)
		sigy=GaussFit(ayv,ay)
		
		fwhmx[i]=sigx*2.35482
		fwhmy[i]=sigy*2.35482
		
		
		#print "Sigma="+str(sigx)+","+str(sigy)
		#print "FWHM="+str(round(fwhmx,3))+","+str(round(fwhmy,3))
		print str(round(fwhmx[i],3))+","+str(round(fwhmy[i],3))
		#print "Ratio: "+str(round(sigx/sigy,3))
		
		#print(datetime.now()-startTime)


		#if fwhmx[i]>13:
		if x>1110 and x<1140 and y>430 and y<440:

			plt.plot(axv,ax, marker='o', color='r')
			plt.plot(ayv,ay, marker='o', color='b')
			#plt.plot(axv,ax, color='r')
			#plt.plot(ayv,ay, marker='o', color='b')

			print str(x0)+","+str(y0)+","+str(fwhmx[i])+","+str(fwhmy[i])+ " "+str(flux)

			plotGauss(sigx,plt, 'm')
			plotGauss(sigy,plt, 'c')
			break
             
	n+=1   
 


plt.yticks([0,0.25,0.5,0.75,1,1.25])
plt.xticks([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6])
plt.grid(True)
plt.show()


