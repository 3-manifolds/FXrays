#include "FXrays.h"

int testdata[] = {
  10, 
  27, 
 -1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,-1,1,0,-1,1,0,
 1,0,-1,0,-1,1,0,0,0,0,0,0,-1,1,0,0,-1,1,1,0,-1,0,0,0,0,-2,2,
 0,-1,1,-1,1,0,0,0,0,0,0,0,1,0,-1,1,0,-1,0,0,0,0,0,0,1,0,-1,
 0,-1,1,1,0,-1,0,-1,1,0,0,0,0,0,0,-1,1,0,-1,1,0,1,0,-1,0,0,0,
 1,0,-1,1,0,-1,0,0,0,0,-1,1,0,-1,1,0,0,0,0,0,0,0,-1,1,-1,1,0,
 -1,1,0,-1,1,0,0,0,0,-1,1,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,-1,1,2,0,-2,1,0,-1,0,0,0,0,-1,1,1,0,-1,0,-1,1,0,0,0,
 0,0,0,0,0,0,-1,1,0,0,-1,1,1,0,-1,0,0,0,0,-1,1,0,0,0,1,0,-1,
 0,0,0,0,0,0,0,-1,1,-1,1,0,0,0,0,1,0,-1,0,-1,1,1,0,-1,0,0,0,
 0,0,0,0,0,0,-1,1,0,1,0,-1,0,-1,1,-1,1,0,0,0,0,-1,1,0,0,0,0
};

main(){
  filter_list_t *testfilter;
  matrix_t *testmatrix = (matrix_t*)&testdata;
  int i;

  testfilter = embedded_filter(testmatrix->columns/3);
  find_vertices(testmatrix, testfilter, print_vertices);

}



