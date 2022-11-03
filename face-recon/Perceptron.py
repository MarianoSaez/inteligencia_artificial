from random import uniform
from math import exp
import numpy as np


class Perceptron:
    """
    Clase que replica el comportamiento de un perceptron con tasa de
    aprendizaje (Learning rate) fija.
    """

    def __init__(self, no_of_inputs: int = 0, weights: list[float] = [], LR: float = 0.1) -> None:
        self.weights: list[float] = weights# or [uniform(-1, 1) for i in range(no_of_inputs + 1)]
        self.learning_rate = LR
        self.last_input = []
        self.last_output = None

    def run(self, input: list[int]) -> float:
        # Agregar el bias en las entradas
        input = np.append(input, [1])
        self.last_input = input

        # Producto escalar entre vector de entradas y pesos
        # x = sum([i*w for w, i in zip(self.weights, input)]) # Python way
        x = np.dot(input, self.weights) # Numpy way

        # Pasarlo por la fc. de activacion y devolver resultado
        self.last_output = 1/(1+exp(-x))
        return self.last_output
    
    def learn(self, dw_list: list[float]) -> list[float]:
        self.weights = [dw + w for dw, w in zip(dw_list, self.weights)]
        return self.weights


    def __str__(self) -> str:
        return f"Perceptron( weights = {[round(w, 5) for w in self.weights]} )\n\tI: {self.last_input}\n\tO: {self.last_output}\n"

if __name__ == "__main__":
    w1 = [0.9, 0.7, 0.5]
    w2 = [0.3, -0.9, -1]
    w3 = [0.8, 0.35, 0.1]
    # w4 = [-0.23, -0.79, 0.56]
    # w5 = [0.6, -0.6, 0.22]
    # w6 = [-0.22, -0.55, 0.31, -0.32]
    
    w4 = [-0.23, -0.79, 0.56, 0.6]

    print("Entrada: ", [0, 1])
    print("SALIDAS DE CADA CAPA:")

    # Capa de entrada
    input_layer_w = [
        w1,
        w2,
        w3,
    ]
    input_layer = [Perceptron(2, w) for w in input_layer_w]
    input_layer_results = [p.run([0, 0]) for p in input_layer]
    print(input_layer_results)



    # Capas ocultas
    hidden_layer_w = [
        w4,
        # w5,
    ]
    hidden_layer_1 = [Perceptron(len(input_layer), w) for w in hidden_layer_w]
    hidden_layer_1_results = [p.run(input_layer_results) for p in hidden_layer_1]
    print(hidden_layer_1_results)

    print(f"\n\n La salida de la red neuronal es: {hidden_layer_1_results[0]}")

    # print("ENTRENAMIENTO")

    # Capa de salida
    # output_layer_w = [
    #     # w6,
    # ]
    # output_layer = [Perceptron(len(hidden_layer_1), w) for w in output_layer_w]
    # output_layer_results = [p.run(hidden_layer_1_results) for p in output_layer]
    # print(output_layer_results)

    # [print(p) for p in input_layer]
    # [print(p) for p in hidden_layer_1]
    # [print(p) for p in output_layer]
