from copy import deepcopy
from Puzzle import Puzzle
from Tree import TreeNode


# CONSTANTS
MAX_MOVES = 10_000_000


class BaseSolver:
    def solve(self, puzzle: Puzzle) -> list[str]:
        raise NotImplementedError

class RandomSolver(BaseSolver):
    def solve(self, puzzle: Puzzle) -> list[str]:
        solution_path = []
        dummy = deepcopy(puzzle)
        for i in range(MAX_MOVES):
            solution_path.append(dummy.__str__())
            if dummy.is_sorted:
                break
            dummy.move_rnd()
        return solution_path

class BFSSolver(BaseSolver):
    def solve(self, puzzle: Puzzle) -> list[str]:
        curr_puzzles = [ deepcopy(puzzle) ]
        curr_nodes = [ TreeNode(curr_puzzles[0]) ]

        for i in range(MAX_MOVES):
            next_nodes = []
            next_puzzles = []

            for j in range(len(curr_puzzles)):
                curr = curr_puzzles[j]
                moves = curr.__getmoves__()
                
                curr_node = curr_nodes[j]

                for move in moves:
                    if move != curr.prev_pos:
                        # Preparar el puzzle sobre el que se mueve
                        next_puzzle = deepcopy(curr)
                        
                        # Realiza el movimiento
                        next_puzzle.move(move[0], move[1])

                        # Tareas relacionadas a la construccion del arbol
                        child_node = TreeNode(next_puzzle)
                        curr_node.append_child(child_node)
                        next_nodes.append(child_node)

                        next_puzzles.append(next_puzzle)

                        if next_puzzle.is_sorted:
                            solution_path = []
                            curr_node.goto_root(solution_path)
                            return [Puzzle(size=puzzle.size).board] + solution_path
                    
            curr_puzzles = next_puzzles
            curr_nodes = next_nodes

class BidirectionalBFSSolver(BaseSolver):
    def solve(self, puzzle: Puzzle) -> list[str]:
        curr_puzzles_obj: list[Puzzle] = [ Puzzle(size=puzzle.size) ]
        curr_puzzles_scr: list[Puzzle] = [ deepcopy(puzzle) ]

        curr_nodes_obj: list[TreeNode] = [ TreeNode(curr_puzzles_obj[0]) ]
        curr_nodes_scr: list[TreeNode] = [ TreeNode(curr_puzzles_scr[0]) ]

        for i in range(MAX_MOVES):

            next_nodes_obj = []
            next_nodes_scr = []

            next_puzzles_obj = []
            next_puzzles_scr = []

            # Generar arbol desde el objetivo
            for j in range(len(curr_puzzles_obj)):

                curr = curr_puzzles_obj[j]
                moves = curr.__getmoves__()

                curr_node_obj = curr_nodes_obj[j]

                # Generar los hijos para el tablero actual
                for move in moves:
                    if move != curr.prev_pos:
                        # Crear un clon del puzzle y realizar el movimiento en el
                        next_puzzle = deepcopy(curr)
                        next_puzzle.move(move[0], move[1])

                        # Agregar el clon al arbol de estados
                        child_node = TreeNode(next_puzzle)
                        curr_node_obj.append_child(child_node)
                        next_nodes_obj.append(child_node)

                        # Agregar el clon al proximo nivel a iterar
                        next_puzzles_obj.append(next_puzzle)

            curr_puzzles_obj = next_puzzles_obj
            curr_nodes_obj = next_nodes_obj

            # Intentar mejorar este algo. de busqueda
            for node_obj in curr_nodes_obj:
                for node_scr in curr_nodes_scr:
                    if node_obj.value.board == node_scr.value.board:
                        path_obj = []
                        path_scr = []

                        node_obj.goto_root(path_obj)
                        node_scr.goto_root(path_scr)

                        return  path_obj[::-1] + path_scr    
     
            # Generar arbol desde el mezclado
            for h in range(len(curr_puzzles_scr)):

                curr = curr_puzzles_scr[h]
                moves = curr.__getmoves__()

                curr_node_scr = curr_nodes_scr[h]

                # Generar los hijos para el tablero actual
                for move in moves:
                    if move != curr.prev_pos:
                        # Crear un clon del puzzle y realizar el movimiento en el
                        next_puzzle = deepcopy(curr)
                        next_puzzle.move(move[0], move[1])

                        # Agregar el clon al arbol de estados
                        child_node = TreeNode(next_puzzle)
                        curr_node_scr.append_child(child_node)
                        next_nodes_scr.append(child_node)

                        # Agregar el clon al proximo nivel a iterar
                        next_puzzles_scr.append(next_puzzle)

            curr_puzzles_scr = next_puzzles_scr
            curr_nodes_scr = next_nodes_scr

            # Intentar mejorar este algo. de busqueda
            for node_obj in curr_nodes_obj:
                for node_scr in curr_nodes_scr:
                    if node_obj.value.board == node_scr.value.board:
                        path_obj = []
                        path_scr = []

                        node_obj.goto_root(path_obj)
                        node_scr.goto_root(path_scr)

                        return  path_obj[::-1] + path_scr

if __name__ == "__main__":
    puzz = Puzzle()

    print("MEZCLANDO...\n")
    puzz.mezclar(50)
    print(puzz.board)
    
    match input("[1] Random\n[2] Anchura\n[3] Bidireccional\nSeleccione metodo de resolucion [1, 2, 3]: "):
        case "1":
            s = RandomSolver()
        case "2":
            s = BFSSolver()
        case "3":
            s = BidirectionalBFSSolver()

    print("RESOLVIENDO...")
    solution = s.solve(puzz)

    print("MOSTRANDO SOLUCION...\n")
    [print(s) for s in solution]    

