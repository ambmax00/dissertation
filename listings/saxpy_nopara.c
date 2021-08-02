#define ARRAY_SIZE 1024

static float x[ARRAY_SIZE] = {1.0};
static float y[ARRAY_SIZE] = {2.0};
static float a = 3.0;

int main() {

  for (int i = 0; i < ARRAY_SIZE; ++i) {
    y[i] += a * x[i];
  }

}
