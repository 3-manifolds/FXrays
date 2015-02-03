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

    matrix_t *new_matrix(int rows, int columns)
    void destroy_matrix(matrix_t *matrix)
    filter_list_t *embedded_filter(int tets)
    void destroy_filter_list(filter_list_t *filterlist)

    
    void* find_vertices(matrix_t *matrix, filter_list_t *filter_list, int print_progress, 
                    void *(*output_func)(vertex_stack_t *stack, int dimension))
    
    void *find_vertices_mod_p(matrix_t *matrix, filter_list_t *filter_list, int print_progress, 
                          void *(*output_func)(vertex_stack_t *stack, int dimension))

cdef void* build_vertex_list(vertex_stack_t *stack, int dimension):
    cdef long coeff
    cdef vertex_t *V = *stack
     
    result = []
    while V != NULL:
        vector = []
        for i in range(dimension):
            coeff = V.vector[i]
            vector.append(coeff)
        result.append(tuple(vector))
        V = V.next
    return <void*> result


def find_Xrays(int rows, int columns, matrix, modp=False,
               filtering=True, print_progress=True):
    cdef filter_list_t *filter = NULL
    cdef matrix_t *c_matrix = new_matrix(rows, columns)

    if rows < 0 or columns < 0 or len(matrix) != rows*columns:
        raise ValueError('rows*columns != length of matrix list.')

    if filtering:
        filter = embedded_filter(columns/3)
        
    for i, c in enumerate(matrix):
        c_matrix.matrix[i] = c

    if modp:
        result = <object> find_vertices_mod_p(c_matrix, filter,
                                              print_progress, build_vertex_list)
    else:
        result = <object> find_vertices(c_matrix, filter,
                                        print_progress, build_vertex_list)

    if filtering:
        destroy_filter_list(filter)
    destroy_matrix(c_matrix)
    
        
    
    
    
                         
    


