class Board(list):
    """
    Clase que extiende el comportamiento de las listas.
    """
    def __str__(self):
        s = ""
        for item in self:
            s += item.__str__() + "\n"
        return s


if __name__ == "__main__":
    b = Board([[1,2,3],[4,5,6],[6,7,8]])
    c = Board([[1,2,3],[4,5,6],[6,7,9]])
    
    print(b)