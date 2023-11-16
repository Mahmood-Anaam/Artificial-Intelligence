
class Game:

    def __init__(self):
        self.initialize()
    # ................................

    def initialize(self):
        self.current_state = [[' ', ' ', ' '],
                              [' ', ' ', ' '],
                              [' ', ' ', ' ']]
        self.min_player = 'X'
        self.max_player = 'O'
        self.num_exploer_nodes = 0
        self.total_exploer_nodes = 0
    


    # ................................

    def draw_board(self):
        str_line = '-------------'
        print('\n' + str_line)
        for i in range(0, 3):
            s = "|"
            for j in range(0, 3):
                print(f'{s} {self.current_state[i][j]} |', end='')
                s = ""
            print("\n" + str_line)

    # ................................

    def available_moves(self, inc=0):
        available_cells = []
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == ' ':
                    available_cells.append(i * 3 + j + inc)
        return available_cells

    # ................................

    def valid_move(self, postion):
        if postion < 0 or postion > 8:
            return False
        elif self.current_state[postion//3][postion % 3] != ' ':
            return False
        else:
            return True

    # ................................

    def is_end(self):

        state = self.current_state
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]

        if [self.max_player,
            self.max_player,
                self.max_player] in win_state:
            return self.max_player

        if [self.min_player,
                self.min_player,
                self.min_player
            ] in win_state :
            return self.min_player

        if len(self.available_moves()) > 0:
            return None

        else:
            return 'Tie'

    # ................................

    def max(self):

        maxv, px, py = -2, None, None
        result = self.is_end()

        if result == self.min_player:
            return (-1, 0, 0)
        elif result == self.max_player:
            return (1, 0, 0)
        elif result == 'Tie':
            return (0, 0, 0)

        self.num_exploer_nodes = self.num_exploer_nodes + 1
        
        for pos in self.available_moves():
            x, y = pos//3, pos % 3
            self.current_state[x][y] = self.max_player
            (m, _, _) = self.min()
            if m > maxv:
                maxv = m
                px = x
                py = y
            self.current_state[x][y] = ' '
        return (maxv, px, py)

    # ................................

    def min(self):

        minv, qx, qy = 2, None, None
        result = self.is_end()

        if result == self.min_player:
            return (-1, 0, 0)
        elif result == self.max_player:
            return (1, 0, 0)
        elif result == 'Tie':
            return (0, 0, 0)

        self.num_exploer_nodes = self.num_exploer_nodes + 1

        for pos in self.available_moves():
            x, y = pos//3, pos % 3
            self.current_state[x][y] = self.min_player
            (m, _, _) = self.max()
            if m < minv:
                minv = m
                qx = x
                qy = y
            self.current_state[x][y] = ' '

        return (minv, qx, qy)

    # ................................

    def max_alpha_beta(self, alpha=-2, beta=2):

        maxv, px, py = -2, None, None
        result = self.is_end()

        if result == self.min_player:
            return (-1, 0, 0)
        elif result == self.max_player:
            return (1, 0, 0)
        elif result == 'Tie':
            return (0, 0, 0)

        self.num_exploer_nodes = self.num_exploer_nodes + 1

        for pos in self.available_moves():
            x, y = pos//3, pos % 3
            self.current_state[x][y] = self.max_player
            (m, _, _) = self.min_alpha_beta(alpha, beta)
            if m > maxv:
                maxv = m
                px = x
                py = y
            self.current_state[x][y] = ' '
            if maxv >= beta:
                return (maxv, px, py)
            if maxv > alpha:
                alpha = maxv

        return (maxv, px, py)

    # ................................

    def min_alpha_beta(self, alpha=-2, beta=2):

        minv, qx, qy = 2, None, None
        result = self.is_end()

        if result == self.min_player:
            return (-1, 0, 0)
        elif result == self.max_player:
            return (1, 0, 0)
        elif result == 'Tie':
            return (0, 0, 0)

        self.num_exploer_nodes = self.num_exploer_nodes + 1

        for pos in self.available_moves():
            x, y = pos//3, pos % 3
            self.current_state[x][y] = self.min_player
            (m, _, _) = self.max_alpha_beta(alpha, beta)
            if m < minv:
                minv = m
                qx = x
                qy = y

            self.current_state[x][y] = ' '

            if minv <= alpha:
                return (minv, qx, qy)

            if minv < beta:
                beta = minv

        return (minv, qx, qy)

    # ................................

    def human_turn(self):

        msg = "\n{0}'s move. What is your move (possible moves at the moment are: {1}) | enter {2} to exit the game)?\n"
        msg = msg.format(self.player_turn, str(
            self.available_moves(inc=1))[1:-1], 0)

        while True:
            value = input(msg)
            if value.isdigit():
                value = int(value)
                if self.valid_move(value-1):
                    break
                elif value == 0:
                    exit()
        x, y = (value-1)//3, (value-1) % 3
        self.current_state[x][y] = self.player_turn

    # ................................

    def computer_turn(self, func):
        (_, x, y) = func()
        self.current_state[x][y] = self.player_turn

        msg = "\n{0}'s selected move: {1}. Number of search tree nodes generated:{2}"
        msg = msg.format(self.player_turn, x*3+y+1, self.num_exploer_nodes)
        print(msg)

        self.total_exploer_nodes = self.total_exploer_nodes + self.num_exploer_nodes
        self.num_exploer_nodes = 0

    # ................................

    def play(self, mode, player_turn, algo):
        self.initialize()
        self.mode = mode
        self.algo = algo
        self.player_turn = player_turn

        if self.algo == 1:
            maxfunc = self.max
            minfunc = self.min
        else:
            maxfunc = self.max_alpha_beta
            minfunc = self.min_alpha_beta

        if self.mode == 1:
            self.draw_board()

        while True:
            self.result = self.is_end()

            if self.result != None:
                if self.result == "Tie":
                    print("\n", "TIE", "\n")
                else:
                    print("\n {0} WON \n".format(self.result))
                return

            if self.mode == 1:

                if self.player_turn == self.min_player:
                    self.human_turn()
                    self.player_turn = self.max_player

                elif self.player_turn == self.max_player:
                    self.computer_turn(func=maxfunc)
                    self.player_turn = self.min_player

                self.draw_board()

            else:

                if self.player_turn == self.max_player:
                    self.computer_turn(func=maxfunc)
                    self.player_turn = self.min_player
                else:
                    self.computer_turn(func=minfunc)
                    self.player_turn = self.max_player

                self.draw_board()
                
        

    # ................................


# ................ End Class ................


if __name__ == "__main__":
    pass
