from django.shortcuts import render
from django.http import HttpResponse

from math import floor #Funcion suelo
from math import ceil #Funcion techo

def home(request):

    return render(request, 'layout_generator/home.html')

def generated_layout(request):

    #hash_table = {2:[33,22,42,43]}
    hash_table = {1:[3,0,8,1,6,4],2:[0,3,0,1]}
    '''a    
        0 = Not available
        1 = Out of service
        2 = Handicap seat
        5 = Assigned seat
    '''
    # Helper that calculates the new maximum capacity based on the social distancing parameters
    def new_max_capacity(normal_capacity,current_capacity)->int:
        return (normal_capacity / 100) * current_capacity

    # Helper function that prints the matrix in format
    def print_bus(matrix)->None:
        for each in matrix:
            print(each)

    # Helper function that replace numbers in the matrix in O(1) complexity | Space complexity O(1)
    def replace_numbers(matrix,arr,num)->None:
        while len(arr) > 0:
            num1 = arr.pop(0)
            num2 = arr.pop(0)
            matrix[num1][num2] = num

    # Helper function that create a matrix with the specified parameters
    def create_matrix(columns,rows,seat_size,social_distance):
        matrix = [[0 for col in range(columns)]for row in range(rows)]
        return matrix

    # Algorithm that determines the best distribution of spaces on a given matrix time complexity O(N) | Space complexity O(N)
    def assign_spaces(matrix,hash_table,block_distance)->None:
        # If there is any modification
        if len(hash_table.keys()) > 0:
            # If we have a seat that needs a handicap
            if 2 in hash_table.keys() and 1 not in hash_table.keys():
                current_index = []
                current_index.append(hash_table[2].pop(0))
                current_index.append(hash_table[2].pop(0))
                while current_index[1] >= block_distance:
                    current_index[1] = current_index[1] - block_distance
                while current_index[0] >= block_distance:
                    current_index[0] = current_index[0] - block_distance
                for layer in range(current_index[0],len(matrix),block_distance):
                    for index in range(current_index[1],len(matrix[0]),block_distance):
                        if matrix[layer][index] == 1:
                            continue
                        matrix[layer][index] = 5

            # If there is a handicap any not available seat
            if 2 in hash_table.keys() and 1 in hash_table.keys():
                places_not_available = hash_table[1]
                replace_numbers(matrix,places_not_available,1)
                max_matrix = []
                max_matrix_sum = 0
                while len(hash_table[2]) > 0:
                    cache_matrix = []
                    current_sum = 0
                    current_index = []
                    current_index.append(hash_table[2].pop(0)) 
                    current_index.append(hash_table[2].pop(0)) 
                    while current_index[0] >= block_distance:
                        current_index[0] = current_index[0] - block_distance
                    while current_index[1] >= block_distance:
                        current_index[1] = current_index[1] - block_distance
                    for layer in range(current_index[0],len(matrix),block_distance):
                        for index in range(current_index[1],len(matrix[0]),block_distance):
                            if matrix[layer][index] == 1:
                                continue
                            cache_matrix.append(layer)
                            cache_matrix.append(index)
                    if max_matrix_sum < len(cache_matrix):
                        max_matrix_sum = len(cache_matrix)
                        max_matrix = cache_matrix
                replace_numbers(matrix,max_matrix,5)

            # There is no handicaps but there is not available places
            if 2 not in hash_table.keys() and 1 in hash_table.keys():
                places_not_available = hash_table[1]
                replace_numbers(matrix,places_not_available,1)
                max_matrix = []
                max_matrix_sum = 0
                count = 0
                while count < block_distance:
                    current_sum = 0
                    cache_mat = []
                    current_index = [0,count]
                    for layer in range(current_index[0],len(matrix),block_distance):
                        for index in range(current_index[1],len(matrix[0]),block_distance):
                            if matrix[layer][index] == 1:
                                continue
                            cache_mat.append(layer)
                            cache_mat.append(index)
                    if len(cache_mat) > max_matrix_sum:
                        max_matrix_sum = len(cache_mat)
                        max_matrix = cache_mat
                    count += 1
                replace_numbers(matrix,max_matrix,5)

        # If we dont have any modification
        else:
            for layer in range(0,len(matrix),block_distance):
                for index in range(0,len(matrix[0]),block_distance):
                    matrix[layer][index] = 5
    
    def layout_generator():
        columns = 4
        columns += 1
        rows = 11
        distance_between_seats = 50
        distance = 100
        new_matrix = create_matrix(columns,rows,distance_between_seats,distance)
        assign_spaces(new_matrix,hash_table,ceil(distance/distance_between_seats))
        print_bus(new_matrix)

        return(new_matrix)

    matrix = layout_generator()

    rows_    = len(matrix)
    columns_ = len(matrix[0])

    total_len = rows_ * columns_

    z = 0
    dict_ = {}

    for x in range(rows_):
        for y in range(columns_):
            z += 1
            dict_[z] = (matrix[x][y])

    print(dict_)
    
    matrix_width  = 2
    matrix_width  = matrix_width + 1

    matrix_height = 6

    return render(request, 'layout_generator/calculated_layout.html', {
        #'matrix_height':range(matrix_height),
        #'matrix_width':range(matrix_width)
        'rows':range(rows_),
        'columns':columns_,
        'matrix_dict':dict_
    }
    )

def generate_initial_grid(request):

    return render(request, 'layout_generator/generate_layout.html')