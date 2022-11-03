from random import uniform
from Perceptron import Perceptron
import numpy as np

LR = 0.5
ITERACIONES = 10_000
TABLA_XOR = [
    [0, 0, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 0]
]
EJEMPLO_PESOS = [
    # Capa de entrada
    [
        [0.9, 0.7, 0.5],
        [0.3, -0.9, -1],
        [0.8, 0.35, 0.1],
    ],

    # Capa de salida
    [
        [-0.23, -0.79, 0.56, 0.6]
    ]
]


class MLP:
    def __init__(self, no_of_inputs: int = 0,
                 perceptrons_per_layer: list[int] = [],
                 weights: list = [],
                 learning_rate: float = 0.1) -> None:
        self.learning_rate = learning_rate
        self.no_of_inputs = no_of_inputs
        self.perceptrons_per_layer = perceptrons_per_layer
        self.weights: list[list[list[float]]] = weights
        self.layers: list[list[Perceptron]] = []
        self.build()

    def build(self) -> None:
        if not self.weights:
            # Caso en el que solo se indiquen las cantidades de cada capa
            no_of_layer_inputs = self.no_of_inputs
            for l in self.perceptrons_per_layer:
                w_list = [[uniform(-1, 1) for i in range(no_of_layer_inputs + 1)] for j in range(l)]
                no_of_layer_inputs = len(w_list)
                self.weights.append(w_list)

        for layer in self.weights:
            new_layer = [Perceptron(weights=w, LR=self.learning_rate) for w in layer]
            self.layers.append(new_layer)

    def run(self, inputs: list[int]) -> list[int|float]:
        layer_inputs = inputs
        for layer in self.layers:
            layer_inputs = np.array([p.run(layer_inputs) for p in layer])
        return layer_inputs

    def train(self, table: list[list[int]]) -> tuple[dict[str, list[float]], dict[str, list[float]]]:
        """
        Entrena al MLP dada una tabla de valores y salidas esperadas.
        Retorna w_hist: dict[str, list[float]], err_hist: dict[str, list[float]]
        """
        delta = 0
        w_hist = {}
        err_hist = {}

        for r, row in enumerate(table):
            # Cargar el MLP de inputs y outputs en cada perceptron
            self.run(row[:-1])
            for i, layer in enumerate(reversed(self.layers)):
                for j, perceptron in enumerate(layer):
                    z = perceptron.last_output
                    y = row[-1]

                    # Comprobar si es el caso tradicional o es necesario estimar
                    if i == 0:
                        epsilon = y - z

                        # Guardar error en histograma
                        if f"{row}" not in err_hist:
                            err_hist[f"{row}"] = []
                        err_hist[f"{row}"].append(epsilon)
                        
                    else:
                        epsilon = delta
                        
                    # Calcular el delta
                    df = z*(1 - z)*epsilon                        
                    
                    # Hacer aprender al perceptron con los dW calculados
                    dw_list = [perceptron.learning_rate * x * df for x in perceptron.last_input]
                    w_list = perceptron.learn(dw_list)

                    # Guardar pesos en el histograma
                    for k, w in enumerate(w_list):
                        if f"{i}{j}{k}" not in w_hist.keys():
                            w_hist[f"{i}{j}{k}"] = []
                        w_hist[f"{i}{j}{k}"].append(w)

                # Supongo que cada capa utilizara la estimacion de la anterior
                delta = df
        return w_hist, err_hist
        
    def __str__(self) -> str:
        s = ""
        for i, layer in enumerate(self.layers):
            s += f"------------- CAPA {i} -------------\n"
            for perceptron in layer:
                s += str(perceptron) + "\n"
            s += "\n"
        return s


if __name__ == "__main__":
    # n = MLP(weights=EJEMPLO_PESOS, learning_rate=LR)
    n = MLP(2, [2, 1], learning_rate=LR)
    # print(n)
    w_hist, err_hist = n.train(TABLA_XOR*ITERACIONES)
    print(n.run([0, 1]))

    # g = Grapher()
    # g.graph(err_hist, "err")
    # g.graph(w_hist, "w")

    # xerr = range(ITERACIONES)
    # for i, err in enumerate(err_hist.values()):
    #     plot.plot(xerr, err, label=f"err{i}")
    # plot.legend()
    # plot.show()

    # xw = range(ITERACIONES*4)
    # for i, w in enumerate(w_hist.values()):
    #     plot.plot(xw, w, label=f'w{i}')
    # plot.legend()
    # plot.show()

    # print(n)

        