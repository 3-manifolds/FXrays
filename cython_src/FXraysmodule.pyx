#cython: language_level=3

cdef extern from "FXrays.h":
    cdef struct support_s:
        unsigned int supp[4]
    ctypedef support_s support_t

    cdef struct vertex_s:
        support_t support
        vertex_s *next
        int value
        int vector[0]
    ctypedef vertex_s vertex_t
        
    ctypedef vertex_t* vertex_stack_t

    cdef struct filter_list_s:
        int size
        support_t filter[0]
    ctypedef filter_list_s filter_list_t

    cdef struct matrix_s:
        int rows
        int columns
        int matrix[0]
    ctypedef matrix_s matrix_t

    matrix_t *FXrays_new_matrix(int rows, int columns)
    void FXrays_destroy_matrix(matrix_t *matrix)
    filter_list_t *FXrays_embedded_filter(int tets)
    void FXrays_destroy_filter_list(filter_list_t *filterlist)
    
    void* FXrays_find_vertices(matrix_t *matrix, filter_list_t *filter_list, int print_progress, 
                    void *(*output_func)(vertex_stack_t *stack, int dimension) except *)
    
    void *FXrays_find_vertices_mod_p(matrix_t *matrix, filter_list_t *filter_list, int print_progress, 
                          void *(*output_func)(vertex_stack_t *stack, int dimension) except *)


cdef extern from "Python.h":
    cdef void Py_INCREF(object o)

cdef void* build_vertex_list(vertex_stack_t *stack, int dimension):
    cdef long coeff
    cdef vertex_t *V = stack[0]
    result = []
    while V != NULL:
        vector = []
        for i in range(dimension):
            coeff = V.vector[i]
            vector.append(coeff)
        result.append(tuple(vector))
        V = V.next
    Py_INCREF(result)
    return <void*> result


def find_Xrays(int rows, int columns, matrix, modp=False,
               filtering=True, print_progress=True):
    """
    Find the extremal rays of the cone defined by the intersection of the
    solution set of the given linear equations and the positive
    orthant.

    Arguments are (in order):

    rows: Number of rows of the matrix of linear equations.

    columns: Number of columns of the matrix of linear equations.

    matrix: The matrix of linear equations, given as a flat list of length
    rows*columns.

    modp (optional, default False): Whether to do the computation
    over p = 2^31 - 1 rather than Z.

    filtering (optional, default True): Return only those extremal rays
    corresponding to embedded surfaces in quad coordinates.  That is,
    if V is the vector corresponding to the ray, then for each triple
    V[3*i:3*(i+1)] at most one entry is non-zero.

    print_progress (optional, default True): Whether to print out
    statistics on the progress of the computation.
    """
    cdef filter_list_t *filter = NULL
    cdef matrix_t *c_matrix = FXrays_new_matrix(rows, columns)

    if rows < 0 or columns < 0 or len(matrix) != rows*columns:
        raise ValueError('rows*columns != length of matrix list.')

    if filtering:
        filter = FXrays_embedded_filter(columns//3)

    for i, c in enumerate(matrix):
        c_matrix.matrix[i] = c

    if modp:
        result = <object> FXrays_find_vertices_mod_p(c_matrix, filter,
                                              print_progress, build_vertex_list)
    else:
        result = <object> FXrays_find_vertices(c_matrix, filter,
                                        print_progress, build_vertex_list)

    if filtering:
        FXrays_destroy_filter_list(filter)
    FXrays_destroy_matrix(c_matrix)
    return result
        
    
    
    
                         
    


