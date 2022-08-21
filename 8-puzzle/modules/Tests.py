from Puzzle import Puzzle
import signal

def signal_handler(signum, frame):
    raise TimeoutError

signal.signal(signal.SIGALRM, signal_handler)



class Test:
    def __getmethods__(self):
        return [method for method in dir(self.__class__) if method.startswith('__') is False]

    def __run__(self):
        log = dict()
        for method in self.__getmethods__():
            exec(f"log['{method}'] = self.{method}()")
            print(f"{method}:{log[method]}")
        return log

    def test_mezclar(self):
        p = Puzzle()
        p.mezclar(20)
        return (p.board != Puzzle().board) and (p.prev_pos != None)

    def test_solve_random(self):
        p = Puzzle()
        p.mezclar(50)
        try:
            signal.alarm(10)   # Ten seconds
            s = p.solve_random()
            return 0 != len(s)
        except TimeoutError:
            return False

    def test_solve_anchura(self):
        return True

    def test_solve_bidireccional(self):
        return True


if __name__ == "__main__":
    t = Test()
    t.__run__()