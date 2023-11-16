import platform
from os import system
import sys
from game import Game


"""
Accept three (3) command line arguments, so your code could be executed with
     python filename.py ALGO FIRST MODE
where:

filename.py : is your python code file name,
ALGO        : specifies which algorithm the computer player will use:
    1 - MiniMax,
    2 - MiniMax with alpha-beta pruning,

FIRST       : specifies who begins the game (X/O)

MODE is mode in which your program should operate:
    1 - human (X) versus computer (O),
    2 - computer (X) versus computer (O),

Example: python main.py 2 X 1


If the number of arguments provided is NOT three (none, one, two or more than three) 
or arguments are invalid (incorrect ALGO, FIRST or MODE) your program should display 
the following error message:

ERROR: Not enough/too many/illegal input arguments.and exit.

"""


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


# ................................

ALGO, FIRST, MODE = None, None, None


def acceptArguments():
    global ALGO, FIRST, MODE

    try:

        n = len(sys.argv)
        if n != 4:
            raise Exception("Not enough/too many/illegal input arguments.")

        ALGO = int(sys.argv[1])
        FIRST = sys.argv[2].upper()
        MODE = int(sys.argv[3])

        if ALGO not in [1, 2] or FIRST not in ["X", "O"] or MODE not in [1, 2]:
            raise Exception("Not enough/too many/illegal input arguments.")

    except Exception as error:
        print("ERROR:", str(error))
        exit()


# ................................

def displayInfo():
    IT_number = 'AXXXXXXXX'
    firstName = 'Mahmood'
    lastName = 'Anaam'
    algo = 'MiniMax' if ALGO == 1 else 'MiniMax with alpha-beta pruning'
    mode = 'human versus computer' if MODE == 1 else 'computer versus computer'
    first = FIRST.upper()
    print("."*50)
    print('{0}, {1}, {2} solution:'.format(lastName, firstName, IT_number))
    print('Algorithm: {0}'.format(algo))
    print('First: {0}'.format(first))
    print('Mode: {0}'.format(mode))
    print("."*50)


# ................................

def main():
    clean()
    acceptArguments()
    displayInfo()

    gameObj = Game()

    gameObj.play(
        mode=MODE,
        player_turn=FIRST,
        algo=ALGO
    )


# ................................

if __name__ == '__main__':
    main()

 
