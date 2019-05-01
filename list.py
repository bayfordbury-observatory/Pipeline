import astropy
import sys
from astropy.io import fits
 
filename=sys.argv[1]+".all.fit"
outname=sys.argv[1]+".all.txt"
 
f = fits.open(filename)
 
#f.info()
with open(outname, 'w') as file:
    file.write("x,y,flux,background,ra,dec\r\n")
rows = f[1].header['naxis2']
#print nrows2
tbdata = f[1].data
cols=5

for x in range(0, rows):
    #print tbdata[x]
    string1=str(tbdata[x][0])+","
    for n in range(1,cols):
        string1 = string1+str(tbdata[x][n])+","
    string1=string1+str(tbdata[x][cols])+"\r\n"
    with open(outname, 'a') as file:
        file.write(string1)
f.close()
exit();
