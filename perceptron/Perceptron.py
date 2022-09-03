"""
PERCEPTRON
Basicamente, consiste de un algoritmo de aprendizaje supervisado
para la clasificacion binaria. Que sea supervisado significa que 
se provee a la funcion/algoritmo con un conjunto de ejemplos para
que esta mapee entradas con salidas.

Definiciones:
    Y = f(X)
        Es la salida Y del perceptron para un vector X

    D = { ( X1, d1 ), (X2, d2), ..., (Xn, dn) }
        Son el conjunto de ejemplos para el aprendizaje. Se compone
        de pares ( Xi, di ) donde Xi es el vector de entradas y di
        es la salida deseada para dicho vector.

    Wi = (w1, w2, ..., wm)
        Representa el vector de pesos por los que se multiplicara
        cada elemento de un vector X

Aclaracion:
Cuanto hacemos aprender a este tipo de algoritmos, lo unico que somos
capaces de modificar son los pesos que se asignan a cada una de las
entradas. Con lo cual a lo largo de las iteraciones, lo que cambiara
"dentro" del perceptron seran las w's.

Peso anterior
  |     Learning Rate
  |     |          Error (Lo esperado - Lo obtenido)
  |     |          |        Entrada recibida
  |     |          |        |
  V     V          V        V
wj(k) + η(k) [z(k) - y(k)] xj(k) = Nuevo peso


Referencias:
    - Wikipedia
    - https://zaguan.unizar.es/record/69205/files/TAZ-TFG-2018-148.pdf

"""

from random import uniform
from statistics import mean

# OR
TRUTH_TABLE = [
    [0, 0, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1],
]

# Euler number
e = 2.7182818284

TRAINING_DATA = TRUTH_TABLE

class Perceptron:
    """
    Clase que replica el comportamiento de un perceptron con tasa de
    aprendizaje (Learning rate) fija.
    """
    def __init__(self, no_of_inputs) -> None:
        self.weights: list[float] = [uniform(-1, 1) for i in range(no_of_inputs + 1)]
        self.learning_rate = 0.1

    def run(self, input: list[int]) -> float:
        # Agregar el bias en las entradas
        input = [1] + input

        # Producto escalar entre vector de entradas y pesos
        x = sum([i*w for w, i in zip(self.weights, input)])

        # Pasarlo por la fc. de activacion y devolver resultado
        return 1/(1+e**(-x))
    
    def train(self, training_data: list[list]) -> None:
        for t_input in training_data:
            y = t_input[-1]
            X = [1] + t_input[:-1]            
            z = self.run(t_input[:-1])
            
            for i, weight in enumerate(self.weights):
                error = y - z
                self.weights[i] += self.learning_rate * error * X[i]


class Trainer:
    """
    Clase encargada de entrenar un perceptron simple hasta alcanzar un
    determinado error.
    """
    def error_based_train(self, p: Perceptron, training_set: list[list], err: float) -> tuple[Perceptron, float]:
        """
        Entrena un perceptron dado p haciendo uso de un set de entrenamiento,
        hasta alcanzar un error promedio menor o igual a err. Retorna el
        perceptron entrenado y su error promedio.
        """
        for _ in range(1_000_000):
            p.train(training_set)

            # Promedio de errores absolutos
            curr_err = mean([abs(x[-1] - p.run(x)) for x in training_set])

            if curr_err <= err:
                print(f"Entrenado despues de {_} iteraciones. Error alcanzado: {curr_err}")
                return p, curr_err


if __name__ == "__main__":
    p = Perceptron(2)
    t = Trainer()

    t.error_based_train(p, TRUTH_TABLE, 0.1)

    # print(f"{p.weights=}")
    # p.train(TRAINING_DATA)
    # print(f"{p.weights=}")
    # print(f"{p.run([0, 0])=}")

