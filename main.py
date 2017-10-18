import sys
from Queue import PriorityQueue
from copy import deepcopy
from math import sqrt

input_file = open('solver.inp', 'r') # read input from file

case_number = int(input_file.readline())

puzzle_area = []
final_states = []
paths = []

def get_min_path(array):
    min_index = 0
    min_len = len(array[0])
    i = 0
    len_arr = len(array)
    while i < len_arr:
        if (array[i] != None):
            l = len(array[i])
            if  l < min_len :
                min_len = l
                min_index = i
            if (i != len_arr - 1):
                i += 1
            else:
                break
        else:
            i += 1
    return i

def get_rectangular_block_numbers(puzzle):
    row_num = len(puzzle)
    col_num = len(puzzle[0])
    rectangular_block_numbers = []
    for i in range(row_num):
        for j in range(col_num):
            curr_num = puzzle[i][j]
            if curr_num != 0 and curr_num not in rectangular_block_numbers:
                rectangular_block_numbers.append(curr_num)
    return rectangular_block_numbers

def move_up(puzzle, rectangular_block_number):
    row_num = len(puzzle)
    col_num = len(puzzle[0])
    cp_puzzle = deepcopy(puzzle)
    for i in range(row_num):
        for j in range(col_num):
            if (cp_puzzle[i][j] == rectangular_block_number):
                if(i != 0):
                    if (cp_puzzle[i-1][j] == 0):
                        cp_puzzle[i-1][j] = rectangular_block_number
                        cp_puzzle[i][j] = 0
                    else:
                        return -1
                else:
                    return -1
    return cp_puzzle

def move_down(puzzle, rectangular_block_number):
    row_num = len(puzzle)
    col_num = len(puzzle[0])
    cp_puzzle = deepcopy(puzzle)
    for i in range(row_num-1, -1, -1):
        for j in range(col_num-1, -1, -1):
            if (cp_puzzle[i][j] == rectangular_block_number):
                if(i != row_num - 1):
                    if (cp_puzzle[i+1][j] == 0):
                        cp_puzzle[i+1][j] = rectangular_block_number
                        cp_puzzle[i][j] = 0
                    else:
                        return -1
                else:
                    return -1
    return cp_puzzle

def move_left(puzzle, rectangular_block_number):
    row_num = len(puzzle)
    col_num = len(puzzle[0])
    cp_puzzle = deepcopy(puzzle)
    for i in range(row_num):
        for j in range(col_num):
            if (cp_puzzle[i][j] == rectangular_block_number):
                if(j != 0):
                    if (cp_puzzle[i][j-1] == 0):
                        cp_puzzle[i][j-1] = rectangular_block_number
                        cp_puzzle[i][j] = 0
                    else:
                        return -1
                else:
                    return -1
    return cp_puzzle

def move_right(puzzle, rectangular_block_number):
    row_num = len(puzzle)
    col_num = len(puzzle[0])
    cp_puzzle = deepcopy(puzzle)
    for i in range(row_num):
        for j in range(col_num-1,-1,-1):
            if (cp_puzzle[i][j] == rectangular_block_number):
                if(j != col_num - 1):
                    if (cp_puzzle[i][j+1] == 0):
                        cp_puzzle[i][j+1] = rectangular_block_number
                        cp_puzzle[i][j] = 0
                    else:
                        return -1
                else:
                    return -1
    return cp_puzzle

def heuristic_diagonal(curr, final):
    row_num = len(curr.puzzle)
    col_num = len(curr.puzzle[0])
    if (curr.puzzle == final):
        return 0
    result = 0
    block_numbers = curr.rectangular_block_numbers

    for num in block_numbers:
        fin_i = 0
        fin_j = 0
        flag = 0
        i = 0
        j = 0
        while flag == 0 and i < row_num:
            if j == col_num:
                j = 0
            while flag == 0 and j < col_num:
                if curr.puzzle[i][j] == num:
                    while flag == 0 and fin_i < row_num:
                        if fin_j == col_num:
                            fin_j = 0
                        while flag == 0 and fin_j < col_num:
                            if final[fin_i][fin_j] == num:
                                flag = 1
                                result += sqrt(abs(i-fin_i)**2 + abs(j-fin_j)**2)
                            fin_j += 1
                        fin_i += 1
                j += 1
            i += 1
    return int(result)

def heuristic_manhattan(curr, final):
    row_num = len(curr.puzzle)
    col_num = len(curr.puzzle[0])
    if (curr.puzzle == final):
        return 0
    manhattan = 0
    block_numbers = curr.rectangular_block_numbers
    fin_i = 0
    fin_j = 0
    flag = 0
    for num in block_numbers:
        fin_i = 0
        fin_j = 0
        for i in range(row_num):
            for j in range(col_num):
                flag = 0
                if curr.puzzle[i][j] == num:
                    while flag == 0 and fin_i < row_num:
                        if fin_j == col_num:
                            fin_j = 0
                        while flag == 0 and fin_j < col_num:
                            if final[fin_i][fin_j] == num:
                                flag = 1
                                manhattan += abs(i - fin_i) + abs(j - fin_j)
                            fin_j += 1
                        if not flag:
                            fin_i += 1
    return manhattan

class node:
    def __init__(self, puzzle, parent, final, rectangular_block_numbers, is_diagonal):
        self.children = []
        self.final = final
        self.parent = parent
        self.puzzle = puzzle
        self.is_diagonal = is_diagonal
        self.rectangular_block_numbers = rectangular_block_numbers
        if parent:
            self.path = parent.path[:]
            self.path.append(puzzle)
            self.g = parent.g + 1
        else:
            self.path = [puzzle]
            self.g = 0
        if self.is_diagonal:
            self.f = self.g + heuristic_diagonal(self, self.final)
        else:
            self.f = self.g + heuristic_manhattan(self, self.final)

    def propagate_children(self):
        for num in self.rectangular_block_numbers:
            pzl = deepcopy(move_left(self.puzzle, num))
            if pzl != -1:
                if self.parent and pzl != self.parent.puzzle:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
                elif self.parent == None:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
            pzl = deepcopy(move_right(self.puzzle, num))
            if pzl != -1:
                if self.parent and pzl != self.parent.puzzle:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
                elif self.parent == None:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
            pzl = deepcopy(move_up(self.puzzle, num))
            if pzl != -1:
                if self.parent and pzl != self.parent.puzzle:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
                elif self.parent == None:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
            pzl = deepcopy(move_down(self.puzzle, num))
            if pzl != -1:
                if self.parent and pzl != self.parent.puzzle:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))
                elif self.parent == None:
                    self.children.append(node(pzl, self, self.final, self.rectangular_block_numbers, self.is_diagonal))


def a_star(start_node):
    open_list = PriorityQueue()
    closed_list = []
    open_list_2 = []
    a_flag = 0
    open_list.put((0, start_node))
    open_list_2.append(start_node)
    while not open_list.empty():
        q = open_list.get()
        open_list_2.remove(q[1])
        closed_list.append(q[1])
        q[1].propagate_children()
        for child in q[1].children:
            a_flag = 0
            if child.puzzle == child.final:
                return child.path
            if child not in closed_list:
                for state in open_list_2:
                    if state.puzzle == child.puzzle:
                        a_flag = 1
                        if state.f < child.f:
                            a_flag = 0
                            break
                if not a_flag:
                    open_list.put((child.f, child))
                    open_list_2.append(child)

    return None

def get_case(f):
    final_states = []
    puzzle_area = []
    is_diagonal = int(f.readline()) #heuristic determination
    puzzle_meta = map(int,f.readline().rstrip('\n').split(' '))
    f.readline() #Read 'S'
    row_number = puzzle_meta[0]
    column_number = puzzle_meta[1]
    piece_number = puzzle_meta[2]
    final_states_number = puzzle_meta[3]
    for i in range(row_number):
        puzzle_area.append(map(int,f.readline().rstrip('\n').split(' ')))
    f.readline() #Read 'F'
    rectangular_block_numbers = get_rectangular_block_numbers(puzzle_area)
    for i in range(final_states_number):
        final_states.append([])
        for j in range(row_number):
            final_states[i].append(map(int,f.readline().rstrip('\n').split(' ')))
        if (final_states_number - 1 is not i):
            f.readline()
    for final_state in final_states:
        paths.append(a_star(node(puzzle_area, None, final_state, rectangular_block_numbers, is_diagonal)))
    return paths[get_min_path(paths)]

for k in range(case_number):
    a = sys.stdin.read(1)
    if ord(a) is 10:
        pathed = get_case(input_file)
        row = len(pathed[0])
        col = len(pathed[0][0])
        for i in range(len(pathed)):
            for j in range(row):
                for k in range(col):
                    print pathed[i][j][k],
                print ""
