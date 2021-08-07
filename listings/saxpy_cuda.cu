#define ARRAY_SIZE 1024 
#define BLOCK_SIZE 256

static float x[ARRAY_SIZE];
static float y[ARRAY_SIZE];
static float a = 3.0;

// the identifier __global__ indicates that it should be launched on the GPU
__global__ 
void saxpy(int N, float d_a, float* d_x, float* d_y) {
	int i = blockIdx.x*blockDim.x+threadIdx.x;
	if (i < N) d_y[i] = d_a*d_x[i] + d_y[i];
}	

int main() {

	// initialize memory on CPU
	for (int i = 0; i < ARRAY_SIZE; ++i) {
        	x[i] = 1.0; y[i] = 2.0;
        }

	// allocate memory on GPU
	float *d_x, *d_y;
	cudaMalloc(&d_x, ARRAY_SIZE*sizeof(float));
	cudaMalloc(&d_y, ARRAY_SIZE*sizeof(float));

	// copy data to GPU
	cudaMemcpy(d_x, x, ARRAY_SIZE*sizeof(float), cudaMemcpyHostToDevice);
	cudaMemcpy(d_y, y, ARRAY_SIZE*sizeof(float), cudaMemcpyHostToDevice);
	
	// launch kernel
	int nblocks = (ARRAY_SIZE + BLOCK_SIZE) / BLOCK_SIZE;
	saxpy<<<nblocks,BLOCK_SIZE>>>(ARRAY_SIZE, a, d_x, d_y);

	// copy back
	cudaMemcpy(y, d_y, ARRAY_SIZE*sizeof(float), cudaMemcpyDeviceToHost);

	// free up memory on GPU
	cudaFree(d_x);
	cudaFree(d_y);

}


