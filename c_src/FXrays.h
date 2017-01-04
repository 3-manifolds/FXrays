/******************************************************************
$Id$
   FXrays -- computes extremal rays with filtering.
   Copyright (C) 2002 Marc Culler, Nathan Dunfield and others

   This program is distributed under the terms of the 
   GNU General Public License, version 2 or later, as published by
   the Free Software Foundation.  See the file GPL.txt for details.
*******************************************************************/
#ifndef VERTEX_H
#define VERTEX_H

#define PRIME ((unsigned int)0x7fffffff)
#define BLOCKSIZE 1000

typedef struct support_s {
  unsigned int supp[4];
} support_t;

// This is a column bitmask for up to 128 columns.
// To optimize extraction, the column indices are
// represented as follows (low order bits to the right):
//    supp[1]                      supp[0]
//  [126, 124, ...  , 64]   [62, 60, ... , 2, 0]
//
//    supp[3]                      supp[2]
//  [127, 125,      , 65]   [63, 61, ... , 3, 1] 


typedef struct vertex_s {
  support_t support;
  struct vertex_s *next;
  int value;
  int vector[1];
} vertex_t;

typedef vertex_t* vertex_stack_t;

typedef struct block_s {
  struct block_s *next;
  vertex_t vertices[1];
} block_t;

typedef struct reservoir_s {
  int dimension;
  block_t *blocklist;
  vertex_t *first_vertex;
} reservoir_t;

typedef struct filter_list_s {
  int size;
  support_t filter[1];
} filter_list_t;

typedef struct matrix_s {
  int rows;
  int columns;
  int matrix[1];   // allow room for rows*columns+1 int32's !!!!
} matrix_t;



//matrices
matrix_t    *FXrays_new_matrix(int rows, int columns);
void         FXrays_destroy_matrix(matrix_t *matrix);

//filterlists
filter_list_t *FXrays_embedded_filter(int tets);
void           FXrays_destroy_filter_list(filter_list_t *filterlist);


//main functions
void *FXrays_find_vertices(matrix_t *matrix, filter_list_t *filter_list, int print_progress, 
		    void *(*output_func)(vertex_stack_t *stack, int dimension));
void *FXrays_find_vertices_mod_p(matrix_t *matrix, filter_list_t *filter_list, int print_progress, 
			  void *(*output_func)(vertex_stack_t *stack, int dimension));

//testing
void *FXrays_print_vertices(vertex_stack_t *stack, int dimension);




#endif
