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

    def solve_random(self) -> list:
        solution_path = []
        dummy = Puzzle(Board(deepcopy(self.board)), self.size)
        for i in range(MAXMOVES):
            solution_path.append(dummy.__str__())
            if dummy.is_sorted:
                break
            dummy.move_rnd()
        return solution_path

    def solve_anchura(self) -> list:
        curr_puzzles = [deepcopy(self),]
        solved = None

        state_space_tree = TreeNode()   # Crear arbol
        state_space_tree.value = curr_puzzles[0]    # Setear la raiz del arbol
        curr_nodes = [state_space_tree]

        
        for i in range(MAXMOVES):
            if solved is not None:
                break

            next_nodes = []
            next_puzzles = []

            for j in range(len(curr_puzzles)):
                puzzle = curr_puzzles[j]
                moves = puzzle.__getmoves__()
                
                curr_node = curr_nodes[j]
                children_nodes = []

                for move in moves:
                    # Preparar el puzzle sobre el que se mueve
                    next_puzzle = deepcopy(puzzle)
                    
                    # Realiza el movimiento
                    next_puzzle.move(move[0], move[1])

                    # Podar elementos que vuelva a la posicion anterior
                    if next_puzzle.__getcurrent__() == puzzle.prev_pos:
                        continue

                    # Tareas relacionadas a la construccion del arbol
                    child_node = TreeNode(next_puzzle)
                    children_nodes.append(child_node)
                    next_nodes.append(child_node)



                    next_puzzles.append(next_puzzle)

                    if next_puzzle.is_sorted:
                        solved = child_node
                        break
                
                curr_node.append_children(children_nodes)
            curr_puzzles = next_puzzles
            curr_nodes = next_nodes

        solution_path = []
        solved.goto_root(solution_path)

        return solution_path

    def solve_bidireccional(self):
        curr_puzzles_obj: list[Puzzle] = [Puzzle(),]
        curr_puzzles_scr: list[Puzzle] = [deepcopy(self),]

        root_objective = TreeNode()
        root_screambled = TreeNode()

        root_objective.value = curr_puzzles_obj[0]
        root_screambled.value = curr_puzzles_scr[0]

        curr_nodes_obj: list[TreeNode] = [root_objective,]
        curr_nodes_scr: list[TreeNode] = [root_screambled,]

        coincidence = None

        for i in range(MAXMOVES):
            if coincidence:
                break

            next_nodes_obj = []
            next_nodes_scr = []

            next_puzzles_obj = []
            next_puzzles_scr = []

            # Generar arbol desde el objetivo
            for j in range(len(curr_puzzles_obj)):

                # print(f"REPORTE OBJ:\n{len(curr_puzzles_obj)=}\n{j=}\n{len(curr_nodes_obj)=}")

                puzzle = curr_puzzles_obj[j]
                moves = puzzle.__getmoves__()

                curr_node_obj = curr_nodes_obj[j]
                children_nodes = []

                # Generar los hijos para el tablero actual
                for move in moves:

                    next_puzzle = deepcopy(puzzle)

                    next_puzzle.move(move[0], move[1])

                    if next_puzzle.__getcurrent__() == puzzle.prev_pos:
                        continue

                    child_node = TreeNode(next_puzzle)
                    children_nodes.append(child_node)
                    next_nodes_obj.append(child_node)


                    next_puzzles_obj.append(next_puzzle)

                curr_node_obj.append_children(children_nodes)
            
            curr_puzzles_obj = next_puzzles_obj
            curr_nodes_obj = next_nodes_obj
            
            # Generar arbol desde el mezclado
            for h in range(len(curr_puzzles_scr)):

                puzzle = curr_puzzles_scr[h]
                moves = puzzle.__getmoves__()

                curr_node_scr = curr_nodes_scr[h]
                children_nodes = []

                # Generar los hijos para el tablero actual
                for move in moves:
                    next_puzzle = Puzzle(deepcopy(puzzle.board), puzzle.size)

                    next_puzzle.move(move[0], move[1])

                    if next_puzzle.__getcurrent__() == puzzle.prev_pos:
                        continue

                    child_node = TreeNode(next_puzzle)
                    children_nodes.append(child_node)
                    next_nodes_scr.append(child_node)


                    next_puzzles_scr.append(next_puzzle)

                curr_node_scr.append_children(children_nodes)
            curr_puzzles_scr = next_puzzles_scr
            curr_nodes_scr = next_nodes_scr

            # Probar si no se resolvio en el camino
            if Puzzle().board in [p.value.board for p in curr_nodes_scr]:
                path = []
                print("MAL")
                return path

            # Intentar mejorar este algo. de busqueda
            for node_obj in curr_nodes_obj:
                for node_scr in curr_nodes_scr:
                    if node_obj.value.board == node_scr.value.board:
                        path_obj = []
                        path_scr = []

                        node_obj.goto_root(path_obj)
                        node_scr.goto_root(path_scr)

                        return  path_obj[::-1] + path_scr

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
