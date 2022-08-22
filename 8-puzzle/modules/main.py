import json
from statistics import mean
from time import time
from Puzzle import Puzzle
from Solver import *


SHUFFLE = 50
SAMPLES = 100
SIZES = range(3, 4)
ALGORITHMS: list[BaseSolver] = [RandomSolver, BFSSolver, BidirectionalBFSSolver]


if __name__ == "__main__":

    # Stats structure
    data = {
        "samples": SAMPLES,
        "shuffle": SHUFFLE,
        "sizes": []

    }

    for size in SIZES:
        print(f"SIZE: {size}")

        samples: dict = {
            "<class 'Solver.RandomSolver'> moves": [],
            "<class 'Solver.RandomSolver'> times": [],
            "<class 'Solver.BFSSolver'> moves": [],
            "<class 'Solver.BFSSolver'> times": [],
            "<class 'Solver.BidirectionalBFSSolver'> moves": [],
            "<class 'Solver.BidirectionalBFSSolver'> times": [],
        }

        for sample in range(SAMPLES):
            print(f"\tSAMPLE No.: {sample + 1}")
            p = Puzzle(size=size)
            p.mezclar(SHUFFLE)

            for algo in ALGORITHMS:
                print(f"\t\tALGORITHM: {str(algo)}")
                t1 = time()
                s = algo().solve(p)
                t2 = time()
                print(f"\t\t\tmoves: {len(s)}")
                print(f"\t\t\ttime: {t2 - t1}")

                samples[str(algo) + " moves"].append(len(s))
                samples[str(algo) + " times"].append(t2-t1)

        data["sizes"].append({
            "size": size,
            "random": {
                "mean_time": mean(samples["<class 'Solver.RandomSolver'> times"]),
                "mean_moves": mean(samples["<class 'Solver.RandomSolver'> moves"]),
                "data": {
                    "moves": samples["<class 'Solver.RandomSolver'> moves"],
                    "time": samples["<class 'Solver.RandomSolver'> times"],
                }
            },
            "BFS": {
                "mean_time": mean(samples["<class 'Solver.BFSSolver'> times"]),
                "mean_moves": mean(samples["<class 'Solver.BFSSolver'> moves"]),
                "data": {
                    "moves": samples["<class 'Solver.BFSSolver'> moves"],
                    "time": samples["<class 'Solver.BFSSolver'> times"],
                }
            },
            "BBFS": {
                "mean_time": mean(samples["<class 'Solver.BidirectionalBFSSolver'> times"]),
                "mean_moves": mean(samples["<class 'Solver.BidirectionalBFSSolver'> moves"]),
                "data": {
                    "moves": samples["<class 'Solver.BidirectionalBFSSolver'> moves"],
                    "time": samples["<class 'Solver.BidirectionalBFSSolver'> times"],
                }
            },

        })
        # [print(f"{k}: {mean(samples[k])}") for k in samples]

    # print(json.dumps(data, indent=4))

    with open("stats.json", "w+") as f:
        f.write(json.dumps(data, indent=4))





            

