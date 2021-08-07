#include <cblas.h>
#define ARRAY_SIZE 1024

static float x[] = {[0 ... ARRAY_SIZE] = 1.0};
static float y[] = {[0 ... ARRAY_SIZE] = 2.0};
static float a = 3.0;

int main() {
	cblas_saxpy(ARRAY_SIZE, a, x, 1, y, 1);
}
