#include <immintrin.h>
#define ARRAY_SIZE 1024

// attribute needed for alignment, misalignment leads to errors
static float x[] __attribute__ ((aligned(8*ARRAY_SIZE))) = {[0 ... ARRAY_SIZE] = 1.0};
static float y[] __attribute__ ((aligned(8*ARRAY_SIZE))) = {[0 ... ARRAY_SIZE] = 2.0};
static float a = 3.0;


int main() {

  __m256 a_vec, x_vec, y_vec, r_vec;

  // set each entry of a_vec to a 
  a_vec = _mm256_set1_ps(a);

  int stride = 8;
  for (int i = 0; i < ARRAY_SIZE; i += stride) {
    // load values into registers with appropriate offset i
    x_vec = _mm256_load_ps(&x[i]);
    y_vec = _mm256_load_ps(&y[i]);

    // perform saxpy: (1) multiply, (2) add
    r_vec = _mm256_add_ps(_mm256_mul_ps(a_vec, x_vec), y_vec);
    
    // copy results back to y
    _mm256_store_ps(&y[i], r_vec);
  }

}
