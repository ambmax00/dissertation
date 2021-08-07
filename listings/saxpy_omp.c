#include <omp.h>
#define ARRAY_SIZE 1024

static float x[] = {[0 ... ARRAY_SIZE] = 1.0};
static float y[] = {[0 ... ARRAY_SIZE] = 2.0};
static float a = 3.0;

int main() {

  // launch threads
  #pragma omp parallel 
  {
    // The code in this region is executed by ALL threads
    int threadnum = omp_get_thread_num(); 
    int numthreads = omp_get_num_threads();

    // lower and upper bound for this thread are determined using the thread number and number of threads
    int lb = ARRAY_SIZE*threadnum/numthreads;
    int ub = ARRAY_SIZE*(threadnum+1)/numthreads;

    for (int i = lb; i < ub; ++i) {
      y[i] += a * x[i];
    }

  } // end parallel region, synchronize

  // tasks share memory, and the result is visible here

}
