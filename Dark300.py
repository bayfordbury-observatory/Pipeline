
#sgima.py
#This code performs hot and cold pixed removel using a 5 sigma clip
# Replacing the faulty pixels with the median pixel value
# it then reports stdev, median value, cold pixels removed, hot pixels removed and frame size in pixels.


import pyfits
import sys
import numpy

def coldpixel(data):
    m = numpy.median(data)
    p = data
    p = p.flatten()
    a = numpy.std(data,dtype=numpy.float64)
    K = m - (a*5)
    coldremove = 0
    while numpy.amin(data) < K:
        coldremove = coldremove + 1
        a =  numpy.amin(data)
        k =  numpy.where(data==a)
        x = k[0]
        x = x[0]
        y = k[1]
        y = y[0]
        data[x,y] = m
    return(data,coldremove)

def hotpixel(data):
    m = numpy.median(data)
    p = data
    p = p.flatten()
    a = numpy.std(data,dtype=numpy.float64)
    K = m + (a*5)   
    hotremove = 0
    while numpy.amax(data) > K:
        hotremove = hotremove + 1
        a =  numpy.amax(data)
        k =  numpy.where(data==a)
        x = k[0]
        x = x[0]
        y = k[1]
        y = y[0]
        data[x,y] = m
    return(data,hotremove)

        

def Do(FitsFileName):
    #FitsFileName = sys.argv[1] #Command line interface
    #FitsFileName = "Master_Dark 15_768x512_Bin4x4_Temp-20C_ExpTime1s.fits"
    hdulist = pyfits.open(FitsFileName)
    scidata = hdulist[0].data
    scidata,hotremove = hotpixel(scidata) #remove hot pixel with 5 sigma clip
    scidata,coldremove = coldpixel(scidata) #Remove cold pixel with 5 sigma clip
    
    hdulist[0].data = scidata
    SaveFitsMake = 'Clean_'+FitsFileName #Write saved file as Clean*
    #hdulist.writeto(SaveFitsMake)
    p = scidata
    p = p.flatten()
    a = numpy.std(p,dtype=numpy.float64) #Find stdev
    b = numpy.median(scidata)
    output = open('imagesigma.csv','a')
    O = FitsFileName+',' + str(a)+','+str(b)+','+str(coldremove)+','+str(hotremove)+',' 
    O = O + str(scidata.shape)
    print >> output,O
    output.close()
    return()

List = open('List.txt','Ur')
for i in List:
    i = i.strip('\n')
    Do(i)
            
