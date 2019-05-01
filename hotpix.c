#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//gcc -fPIC -shared -o hotxaxis.so hotxaxis.c
//export LD_LIBRARY_PATH=/usr/local/lib/python2.7/:$LD_LIBRARY_PATH

int compare (const void * a, const void * b)
{
  return ( *(int*)a - *(int*)b );
}


int median(int array[]){

    qsort(array, 9, sizeof(int), compare);

    return array[4];
}

void cfun(int strength, int xaxis, int yaxis, const int *data1, int *outa1) {

    const int * scidata = (int *) data1;	
	
    int * a1 = (int *) outa1;

	int medarr[] = {0,0,0,0,0,0,0,0,0};
	
	int x, y, k, upper, lower, sigma, av;


	for(x=1; x<(xaxis-1); x++){
		for(y=1; y<(yaxis-1); y++){
		
			k=(y*xaxis)+x;
				
			medarr[0]=scidata[k+1];
			medarr[1]=scidata[k-1];
			medarr[2]=scidata[k+xaxis-1];
			medarr[3]=scidata[k+xaxis];
			medarr[4]=scidata[k+xaxis+1];
			medarr[5]=scidata[k-xaxis-1];
			medarr[6]=scidata[k-xaxis];
			medarr[7]=scidata[k-xaxis+1];			
			medarr[8]=scidata[k];

			av=median(medarr);
			
			sigma=sqrt(av);

			lower=av-(sigma*strength);
			upper=av+(sigma*strength);

			if(scidata[k]>upper || scidata[k]<lower){
				a1[k]=av;
			}else{
				a1[k]=scidata[k];
				
			}

		}
	}

}
