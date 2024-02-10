
import sys
import os
import pandas as pd
import sudokucsp 

"""
Accept two (2) command line arguments, so your code could be executed with
     python filename.py MODE FILENAME
where:

filename.py : is your python code file name,

MODE is mode in which your program should operate:
    1 - brute force search,
    2 - Constraint Satisfaction Problem back-tracking search,
    3 - CSP with forward-checking and MRV heuristics,
    4 - test if the completed puzzle is correct.

FILENAME : is the input CSV file name (unsolved or solved sudoku puzzle),   



Example: python main.py  2 testcase4.csv


If the number of arguments provided is NOT two (none, one,or more than two) or arguments 
are invalid (incorrect FILENAME or MODE) program display  the following error message:

ERROR: Not enough/too many/illegal input arguments.and exit.

"""




MODE,FILENAME = None, None


def acceptArguments():
    global MODE,FILENAME
    
    try:

        n = len(sys.argv)
        
        if n != 3:
            raise Exception("Not enough/too many/illegal input arguments.")


        MODE = int(sys.argv[1])
        FILENAME = str(sys.argv[2])
    
        if MODE not in [1,2,3,4] or  not os.path.exists(FILENAME):
            raise Exception("Not enough/too many/illegal input arguments.")

    except Exception as error:
        print("ERROR:", str(error))
        exit()


# ................................

def displayInfo():
    IT_number = 'AXXXXXXXX'
    firstName = 'Mahmood'
    lastName = 'Anaam'
    if MODE == 1:
        algo = 'brute force search'
    elif MODE == 2:
        algo = 'CSP back-tracking search'
    elif MODE == 3:
        algo = 'CSP with forward-checking and MRV heuristics'
    else:
        algo = 'TEST'
 
    print('\n{0}, {1}, {2} solution:'.format(lastName, firstName, IT_number))
    print('Input file: {0}'.format(FILENAME))
    print('Algorithm: {0}'.format(algo))
    print("."*30)


# ................................

def displayBoard(board):
    for i in range(len(board)):
        s = ','
        for j in range(len(board[1])):
            if j==len(board[1])-1:
                s = ''
            print(f'{board[i][j]}{s}',end="")
        print()
    print()


# ................................

def readData():
    df = pd.read_csv(FILENAME,header=None)
    return df.to_numpy().tolist()


# ................................

def displayReportResults(solved_board,num_nodes=0,exec_time=0):
    print('Number of search tree nodes generated: {0}'.format(num_nodes))
    print('Search time: {0} seconds'.format(exec_time))
    print(f'\n Solved puzzle:\n')
    displayBoard(solved_board)
    
 

# ................................
def main():
    global MODE,FILENAME
    acceptArguments()
    input_board = readData()

    num_nodes = 0
    exec_time = 0

    csp = sudokucsp.SudokuCSP(input_board)
    displayInfo()


    if MODE == 4:
        
        print(f'\n Solved puzzle:\n')
        displayBoard(input_board)

        if csp.goal_test(csp.domains):
            print(f'\n This is a valid, solved, Sudoku puzzle.\n')
            
        else:
            print(f'\n ERROR: This is NOT a solved Sudoku puzzle.\n')
        
        print('Number of search tree nodes generated: {0}'.format(num_nodes))
        print('Search time: {0} seconds'.format(exec_time))
        print()    
        return
    
    print(f'\n Input puzzle:\n')
    displayBoard(input_board)
    
    if MODE == 1:
        solved_board,num_nodes,exec_time = sudokucsp.backtrack_Brute_Force_Search(csp)

    elif MODE == 2:
        solved_board,num_nodes,exec_time = sudokucsp.backtracking_search(csp,type='CSP_BackTracking')
    
    elif MODE == 3:
        solved_board,num_nodes,exec_time = sudokucsp.backtracking_search(csp,type='CSP_forward_Checking_MRV')
        
        
    displayReportResults(
        solved_board=solved_board,
        num_nodes= num_nodes,
        exec_time=exec_time
        )
    pd.DataFrame(solved_board).to_csv('{0}_solution.csv'.format(FILENAME.split('.')[0]),index=False,header=None)
        


# ................................

def calculateAverage(mode=2,fileName='testcase6.csv'):
    global MODE,FILENAME
    MODE,FILENAME  = mode,fileName
    input_board = readData()
    csp = sudokucsp.SudokuCSP(input_board)

    exec_time_sum = 0
    for i in range(10):
        if mode==1:
            _,num_nodes,exec_time = sudokucsp.backtrack_Brute_Force_Search(csp)
        elif mode==2:
            _,num_nodes,exec_time = sudokucsp.backtracking_search(csp,type='CSP_BackTracking')
        else :
            _,num_nodes,exec_time = sudokucsp.backtracking_search(csp,type='CSP_forward_Checking_MRV')

        exec_time_sum = exec_time_sum + exec_time
       

    return exec_time_sum/10,num_nodes


# ................................

if __name__ == '__main__':
     main()
     
    # print(calculateAverage(mode=1,fileName='testcase6.csv'))
    # print(calculateAverage(mode=2,fileName='testcase6.csv'))
    # print(calculateAverage(mode=3,fileName='testcase6.csv'))


 
