#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#define ARRAY_SIZE 1024

static float a = 3.0; 

int main(int argc, char** argv) {

  MPI_Init(&argc,&argv);
  MPI_Comm comm = MPI_COMM_WORLD;

  int rank, size;
  // get information form communicator
  MPI_Comm_rank(comm, &rank);
  MPI_Comm_size(comm, &size);

  // size needs to be a divisor of ARRAY_SIZE
  if (ARRAY_SIZE % size != 0) exit(-1);
  int num_local = ARRAY_SIZE / size;

  // allocate local arrays on each process
  float* x_loc = (float*)malloc(num_local*sizeof(float));
  float* y_loc = (float*)malloc(num_local*sizeof(float));

  // global arrays
  float *x, *y; 

  if (rank == 0) {
	// init data on rank 0
	x = (float*)malloc(ARRAY_SIZE*sizeof(float));
	y = (float*)malloc(ARRAY_SIZE*sizeof(float));
	for (int i = 0; i < ARRAY_SIZE; ++i) {
		x[i] = 1.0; y[i] = 2.0;
	}
  }

  // send to other processes
  MPI_Scatter(x,num_local,MPI_FLOAT,x_loc,num_local,MPI_FLOAT,0,comm);
  MPI_Scatter(y,num_local,MPI_FLOAT,y_loc,num_local,MPI_FLOAT,0,comm);
  
  // perform operation on local arrays
  for (int  i = 0; i < num_local; ++i) {
	  y_loc[i] += a * x_loc[i];
  }

  // gather data on rank 0
  MPI_Gather(y_loc,num_local,MPI_FLOAT,y,num_local,MPI_FLOAT,0,comm);
  // print it out, store it ...

  // clean up
  free(x_loc); free(y_loc);
  if (rank == 0) {
	  free(x); free(y);
  }
  
  MPI_Finalize();

}
