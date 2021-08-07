#define ARRAY_SIZE 1024

static float x[] = {[0 ... ARRAY_SIZE] = 1.0};
static float y[] = {[0 ... ARRAY_SIZE] = 2.0};
static float a = 3.0;

int main() {

  #pragma omp parallel for
  for (int i = 0; i < ARRAY_SIZE; ++i) {
    y[i] += a * x[i];
  }

}
