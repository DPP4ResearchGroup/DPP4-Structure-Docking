#include <omp.h>
#include <cstdio>
int main() {
  printf("%d\n", omp_get_max_threads());
  return 0;
}  
