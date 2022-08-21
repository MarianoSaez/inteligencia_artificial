from secrets import choice
from Board import Board
from copy import deepcopy

from Tree import TreeNode, print_tree

"""
MOVES:
1 := Arriba
2 := Derecha
3 := Abajo
4 := Izquierda
"""
MAXMOVES = 100_000_000

class Puzzle():
    def __init__(self, board: Board = None, size: int = 3) -> None:
        self.board = board
        self.size = size
        self.prev_pos = None

    def __getcurrent__(self) -> list[int, int]:
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] == "O":
                    return [row, column]

    def __getmoves__(self) -> list[list[int]]:
        curr = self.__getcurrent__()
        move_list = []
        if curr[0] > 0:
            # Arriba
            move_list.append([curr[0] - 1, curr[1]])
        if curr[0] < self.size - 1:
            # Abajo
            move_list.append([curr[0] + 1, curr[1]])
        if curr[1] > 0:
            # Izquierda
            move_list.append([curr[0], curr[1] - 1])
        if curr[1] < self.size - 1:
            # Derecha
            move_list.append([curr[0], curr[1] + 1])
        return move_list

    def move_rnd(self):
        """
        Mueve la ficha O de forma aleatoria.
        """
        moves = self.__getmoves__()
        curr = self.__getcurrent__()
        self.prev_pos = curr
        next = choice(moves)
        
        self.board[curr[0]][curr[1]] = self.board[next[0]][next[1]]
        self.board[next[0]][next[1]] = "O"

    def move(self, next_x, next_y) -> None:
        curr_x, curr_y = self.__getcurrent__()
        self.prev_pos = [curr_x, curr_y]
        self.board[curr_x][curr_y] = self.board[next_x][next_y]
        self.board[next_x][next_y] = "O"

    def mezclar(self, t: int) -> None:
        for i in range(t):
            self.move_rnd()

    @property
    def is_sorted(self):
        return Board([[1, 2, 3], [4, 5, 6], [7, 8, "O"]]) == self.board

    @property
    def board(self):
        return self.__board
    
    @board.setter
    def board(self, val):
        if val is None:
            self.__board = Board([[1, 2, 3], [4, 5, 6], [7, 8, "O"]])
        else:
            self.__board = val

    def __str__(self) -> str:
        return self.board.__str__()
        


if __name__ == "__main__":
    p = Puzzle()
    p.mezclar(1000)
    print(p.board)
    sol = p.solve_bidireccional()
    [print(s) for s in sol]
