/******************************************************************
$Id$
   FXrays -- computes extremal rays with filtering.
   Copyright (C) 2002 Marc Culler, Nathan Dunfield and others

   This program is distributed under the terms of the 
   GNU General Public License, version 2 or later, as published by
   the Free Software Foundation.  See the file GPL.txt for details.
*******************************************************************/
#include "Python.h"
#include "FXrays.h"

static PyObject *ErrorObject;

static void *build_vertex_list(vertex_stack_t *stack, int dimension){
  PyObject *result, *coeff;
  vertex_t *V = *stack;
  int i;

  result = PyList_New(0);
  if (result != NULL){
    for (; V != NULL; V = V->next ) {
      coeff = PyTuple_New(dimension);
      for (i=0; i<dimension ; i++)
	PyTuple_SetItem(coeff, i, PyInt_FromLong((long)V->vector[i]));
      PyList_Append(result, coeff);
      Py_DECREF(coeff);
    }
  }
  return result;
}

static PyObject *Py_find_Xrays(PyObject *self, PyObject *args, PyObject *keywds){
  PyObject *result;
  PyObject *pymatrix;
  int rows, columns, length;
  int modp = 0;
  int filtering = 1;
  int print_progress = 1;

  static char *kwlist[] = {"rows", "columns", "matrix", "modp", "filtering", "print_progress", NULL};

  if ( !PyArg_ParseTupleAndKeywords(args, keywds, "iiO|iii:find_vertices", kwlist,
		   &rows, &columns, &pymatrix, &modp, &filtering, &print_progress) )
    return NULL;

  if ( !PySequence_Check(pymatrix) ){
    PyErr_SetString( ErrorObject, 
     "Argument 3 to find_Xrays must support the sequence protocol.");
    return NULL;
  }

  length = PySequence_Length(pymatrix);

  if ( rows < 0 || columns < 0 || length != rows*columns ){
    PyErr_SetString( ErrorObject,
		     "Bad arguments to find_Xrays: rows*columns != size of matrix.");
    return NULL;
  }

  {
    int i;
    PyObject *Item;
    matrix_t *matrix = new_matrix(rows, columns);
    filter_list_t *filter = NULL;
    if (filtering)
      filter = embedded_filter(columns/3);
    for (i=0; i< length; i++) {
      Item = PySequence_GetItem(pymatrix, i);
      matrix->matrix[i] = PyInt_AsLong(Item);
      Py_DECREF(Item);
      }

    if (modp)
	result = (PyObject*)find_vertices_mod_p(matrix, filter, print_progress, build_vertex_list);
    else
	result = (PyObject*)find_vertices(matrix, filter, print_progress, build_vertex_list);
    if (filter)
      destroy_filter_list(filter);
    destroy_matrix(matrix);
  }
  return result;
}

/* Documentation */
static char find_Xrays_doc[]=
"Find the extremal rays of the cone defined by the intersection of the\n"
"solution set of the given linear equations and the positive orthant.\n"
"Arguments are (in order):\n"
"\n"
"rows: Number of rows of the matrix of linear equations.\n"
"\n"
"columns: Number of columns of the matrix of linear equations.\n"
"\n"
"matrix: The matrix of linear equations, given as a flat list of length\n"
"   rows*columns.\n"
"\n"
"modp (optional, default False): Whether to do the computation\n"
"   over p = 2^31 - 1 rather than Z.\n"
"\n"
"filter (optional, default True): Return only those extremal rays\n"
"   corresponding to embedded surfaces in quad coordinates.  That is, if V\n"
"   is the vector corresponding to the ray, then for each triple\n"
"    V[3*i:3*(i+1)] at most one entry is non-zero.\n"
"\n"
"print_progress (optional, default True): Whether to print out\n"
"   statistics on the progress of the computation.\n"
"\n";

/* List of functions defined in the module */

static PyMethodDef FXrays_methods[] = {
  {"find_Xrays", (PyCFunction)Py_find_Xrays, METH_VARARGS|METH_KEYWORDS,
   find_Xrays_doc},
  {NULL,		NULL}		/* sentinel */
};


/* Initialization function for the module */

DL_EXPORT(void)
initFXrays(void)
{
	PyObject *m, *d;

	/* Create the module and add the functions */
	m = Py_InitModule("FXrays", FXrays_methods);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);
	ErrorObject = PyErr_NewException("RXrays.error", NULL, NULL);
	PyDict_SetItemString(d, "error", ErrorObject);
}
