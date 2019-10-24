#include <stdio.h>
#include <stdlib.h>

//To compile:
//gcc -fPIC -shared -o py.so py.c


int compare(const void *a, const void *b){
    float fa = *(float *) a;
    float fb = *(float *) b;
    return (fa > fb) - (fa < fb);
}


float median(float array[]){

    qsort(array, 9, sizeof(float), compare);

    return array[4];
}

int cfun(int pix, int xaxis1, int xaxis2, int yaxis1, int yaxis2, float scalex2, float scaley2, float xscale1, float xscale2, float yscale1, float yscale2, float cxd1, float cyd1, float cxd2, float cyd2, float sinr1, float sinr2, float cosr1, float cosr2, const float *data1, const float *data2, float *outa1, float *outa2, float *outb) {

	size_t size = pix*pix;

	int sncount = 0;

    const float * scidata1 = (float *) data1;
	const float * scidata2 = (float *) data2;	
	
    float * a1 = (float *) outa1;
	float * a2 = (float *) outa2;
	float * b = (float *) outb;

	float xaxis1f = (float)xaxis1;
	float xaxis2f = (float)xaxis2;
	float yaxis1f = (float)yaxis1;
	float yaxis2f = (float)yaxis2;

	float medarr[] = {0,0,0,0,0,0,0,0,0};
	//float *medarr;

	int x, y, i, j, k1, k2;

	float xc, yc, x1, y1, x2, y2;

	float av;

	for(x=0; x<pix; x++){
		for(y=0; y<pix; y++){

			k1=(y*pix)+x;

			xc=(x-(pix/2))*scalex2;
			yc=(y-(pix/2))*scaley2;

			x1=xc-cxd2;		
			y1=yc-cyd2;
	
			x2=(xaxis1/2)+(x1/xscale1)*cosr1-(y1/yscale1)*sinr1;
			y2=(yaxis1/2)+(x1/xscale1)*sinr1+(y1/yscale1)*cosr1;				

			if(x2>0 && x2<=xaxis1 && y2>0 && y2<=yaxis1){
			
				k2=((int)y2*xaxis1)+(int)x2;
				
				a1[k1]=data1[k2];
			
				x1=xc+cxd2;
				y1=yc+cyd2;
		
				x2=(xaxis2/2)+(x1/xscale2)*cosr2-(y1/yscale2)*sinr2;
				y2=(yaxis2/2)+(x1/xscale2)*sinr2+(y1/yscale2)*cosr2;	
		
				
				if(x2>0 && x2<=xaxis2 && y2>0 && y2<=yaxis2){

					k2=((int)y2*xaxis2)+(int)x2;

					a2[k1]=data2[k2];
			
					if(a1[k1]<140){
						//b[k1]=(a2[k1]-a1[k1])/2;

						if ((a2[k1]-a1[k1]) > 100){
							b[k1]=255;
							//b[k1]=(a2[k1]-a1[k1])/2;
						}

					}

				}
			}			
	
		}

	}


	for(x=1; x<(pix-1); x++){
		for(y=1; y<(pix-1); y++){

			
			k1=(y*pix)+x-1;
			medarr[0]=b[k1];

			k1=(y*pix)+x+1;
			medarr[1]=b[k1];

			k1=((y-1)*pix)+x;
			medarr[2]=b[k1];

			k1=((y+1)*pix)+x;
			medarr[3]=b[k1];

			k1=((y-1)*pix)+x-1;
			medarr[4]=b[k1];

			k1=((y-1)*pix)+x+1;
			medarr[5]=b[k1];

			k1=((y+1)*pix)+x-1;
			medarr[6]=b[k1];

			k1=((y+1)*pix)+x+1;
			medarr[7]=b[k1];			

			k1=(y*pix)+x;
			medarr[8]=b[k1];

			av=median(medarr);

			if(b[k1]>(av*5)){
				b[k1]=av;
			}
			if(b[k1]>50){
				sncount++;
			}

		}
	}
	return sncount;
}
