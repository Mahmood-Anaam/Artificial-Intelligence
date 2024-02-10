import copy
from timeit import default_timer as timer

 # ..........................................................

class SudokuCSP:

    def __init__(self, board):
        self.board = board
        self.domains = {}
        self.neighbors = {}
        self.assignment = {}
        # our variables will be named as "CELL NUMBER"
        for v in range(81):
            self.neighbors.update({'CELL' + str(v): {}})
        for i in range(9):
            for j in range(9):
                name = (i * 9 + j)
                var = "CELL"+str(name)
                self.add_neighbor(var, self.get_row(i) | self.get_column(j) | self.get_square(i, j))
                # if the board has a value in cell[i][j] the domain of this variable will be that number
                if self.board[i][j] != 'X':
                    self.domains.update({var: str(self.board[i][j])})
                    self.assignment[var] = str(self.board[i][j])
                else:
                    self.domains.update({var: '123456789'})

        
        self.variables = list(self.domains.keys())
        self.constraints = different_values_constraint
        self.curr_domains = None
        self.nassigns = 0
        self.n_bt = 0

    # ..........................................................

    # returns the right square box given row and column index
    def get_square(self, i, j):
        if i < 3:
            if j < 3:
                return self.get_square_box(0)
            elif j < 6:
                return self.get_square_box(3)
            else:
                return self.get_square_box(6)
        elif i < 6:
            if j < 3:
                return self.get_square_box(27)
            elif j < 6:
                return self.get_square_box(30)
            else:
                return self.get_square_box(33)
        else:
            if j < 3:
                return self.get_square_box(54)
            elif j < 6:
                return self.get_square_box(57)
            else:
                return self.get_square_box(60)
    # ..........................................................

    # returns the square of the index's variabile, it must be 0, 3, 6, 27, 30, 33, 54, 57 or 60
    def get_square_box(self, index):
        tmp = set()
        tmp.add("CELL"+str(index))
        tmp.add("CELL"+str(index+1))
        tmp.add("CELL"+str(index+2))
        tmp.add("CELL"+str(index+9))
        tmp.add("CELL"+str(index+10))
        tmp.add("CELL"+str(index+11))
        tmp.add("CELL"+str(index+18))
        tmp.add("CELL"+str(index+19))
        tmp.add("CELL"+str(index+20))
        return tmp
    
     # ..........................................................

    def get_column(self, index):
        return {'CELL'+str(j) for j in range(index, index+81, 9)}
    # ..........................................................
    def get_row(self, index):
            return {('CELL' + str(x + index * 9)) for x in range(9)}
    # ..........................................................

    def add_neighbor(self, var, elements):
        # we dont want to add variable as its self neighbor
        self.neighbors.update({var: {x for x in elements if x != var}})
     # ..........................................................

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1
    # ..........................................................

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
     # ..........................................................

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        count = 0
        for var2 in self.neighbors.get(var):
            val2 = None
            if assignment.__contains__(var2):
                val2 = assignment[var2]
            if val2 is not None and self.constraints(var, val, var2, val2) is False:
                count += 1
        return count
     # ..........................................................

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))
     # ..........................................................

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
     # ..........................................................

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals
     # ..........................................................

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))
     # ..........................................................

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]
     # ..........................................................

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)
    # ..........................................................


# ................ End Class ................



# CSP Backtracking Search

def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    for var in csp.variables:
        if var not in assignment:
            return var

 # ..........................................................

def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    vars_to_check = []
    size = []
    for v in csp.variables:
        if v not in assignment.keys():
            vars_to_check.append(v)
            size.append(num_legal_values(csp, v, assignment))
    return vars_to_check[size.index(min(size))]

 # ..........................................................

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        count = 0
        for val in csp.domains[var]:
            if csp.nconflicts(var, val, assignment) == 0:
                count += 1
        return count
    
 # ..........................................................

def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)

 # ..........................................................


# Inference

def no_inference(csp, var, value, assignment, removals):
    return True

 # ..........................................................

def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


 # ..........................................................

def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b

 # ..........................................................

num_nodes = 0

def backtracking_search(csp,type):
    global num_nodes
    num_nodes = 0
    if type == 'CSP_BackTracking':
        select_unassigned_variable = first_unassigned_variable
        inference = no_inference  

    else :
        select_unassigned_variable = mrv
        inference = forward_checking

    def backtrack(assignment):
        global num_nodes  
        if len(assignment) == len(csp.variables):
            return assignment
        
        num_nodes = num_nodes + 1
        var = select_unassigned_variable(assignment, csp)
        
        for value in unordered_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    else:
                        csp.n_bt += 1
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    solved_board = copy.deepcopy(csp.board)

    start = timer()
    result = backtrack(copy.deepcopy(csp.assignment))

    if result is not None:
        for i in range(9):
            for j in range(9):
                index = i * 9 + j
                solved_board[i][j] = result.get("CELL" + str(index))

    else:
        print(f'\n ERROR: This is NOT a solved Sudoku puzzle.\n')
        
    end = timer()
    exec_time = round(end-start, 5)
    
    return solved_board,num_nodes,exec_time

 # ..........................................................


def backtrack_Brute_Force_Search(csp):
    global num_nodes
    num_nodes = 0



    def is_complete(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 'X':
                    return False
        return True
    
    # .............................

    def find_empty_cell(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 'X':
                    return row, col
        return None, None
    
    # .............................

    def is_valid_assignment(board, row, col, num):
        for i in range(9):
            if board[row][i] == num:
                return False
            
        for i in range(9):
            if board[i][col] == num:
                return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True
    
    # .............................

    def backtrack(board):
        global num_nodes
      

        if is_complete(board):
            return board
        num_nodes = num_nodes + 1
        row, col = find_empty_cell(board)

        for num in range(1,10):
            num = str(num)
            if is_valid_assignment(board, row, col, num):
                board[row][col] = num
                
                if backtrack(board):
                    return board
                
                board[row][col] = 'X'
        return None


    solved_board = copy.deepcopy(csp.board)
    start = timer()
    result = backtrack(copy.deepcopy(csp.board))

    if result is not None:
        solved_board = result

    else:
        print(f'\n ERROR: This is NOT a solved Sudoku puzzle.\n')
        
    end = timer()
    exec_time = round(end-start, 5)
    
    return solved_board,num_nodes,exec_time


 # ..........................................................






