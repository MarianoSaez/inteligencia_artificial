from random import randint
from MLP import MLP, Grapher
import numpy as np
import cv2
import argparse as ap
from tqdm import tqdm

parser = ap.ArgumentParser()
parser.add_argument("-l", "--learningrate", default=0.5, type=float)
parser.add_argument("-p", "--hiddenlayerperc", default=100, type=int)
parser.add_argument("--layers", default=1, type=int)
parser.add_argument("-i", "--iter", default=500, type=int)
args = parser.parse_args()

# IMAGE SETTINGS
BASE_PATH = "./img/original/"
EXTENTION = "jpg"
TEST_IMAGES = ["6A59161", "7A59161", "8A59161", "6B59161", "7B59161", "8B59161"]
IMG_SIZE = 80*96
IMG_LIMIT = 5
IMG_RANGE = sorted([i for i in range(1, IMG_LIMIT + 1)]*2)
PERSON_RANGE = ["A", "B"]*5

# MLP SETTINGS
LR = args.learningrate
HIDDEN_LAYER_PERCEPTRONS = args.hiddenlayerperc
HIDDEN_LAYERS = args.layers
ITERACIONES = args.iter

# PLOT SETTINGS
SAVE_PATH = "./resultados/"

if __name__ == "__main__":
    
    # Leer imagenes
    print("CARGANDO IMAGENES")
    img_list = []
    for gesture, person in zip(IMG_RANGE, PERSON_RANGE):
        print(f"CARGANDO: {BASE_PATH}{gesture}{person}59161.{EXTENTION}")
        flat_img = cv2.imread(f"{BASE_PATH}{gesture}{person}59161.{EXTENTION}", 0).flatten()/255
        if person == "A":
            np.append(flat_img, [0])
        else:
            np.append(flat_img, [1])
        img_list.append(flat_img)

    # Instanciar y entrenar MLP
    print("CREANDO RED NEURONAL")
    print([HIDDEN_LAYER_PERCEPTRONS]*HIDDEN_LAYERS)
    mlp = MLP(IMG_SIZE, [HIDDEN_LAYER_PERCEPTRONS]*HIDDEN_LAYERS + [1], learning_rate=LR)
    
    print("ENTRENANDO RED NEURONAL")
    global_err_hist = {}
    for i in tqdm(range(ITERACIONES)):
        w_hist, err_hist = mlp.train(img_list)
        for k in err_hist:
            if k not in global_err_hist:
                global_err_hist[k] = err_hist[k]
            else:
                global_err_hist[k] += err_hist[k]


    # Mostrar graficas de errores
    g = Grapher()
    g.graph(global_err_hist, "error ", save=SAVE_PATH + f"LR{LR}_HLP{HIDDEN_LAYER_PERCEPTRONS}_{HIDDEN_LAYERS}HL_ITER{ITERACIONES}_ID_{randint(0, 1_000_000)}.png")

    # Ejecutar
    for test_img in TEST_IMAGES:
        flat_img = cv2.imread(f"{BASE_PATH}{test_img}.{EXTENTION}", 1).flatten()/255
        r = mlp.run(flat_img)
        print(f"EXAMPLE: {test_img}.{EXTENTION} --> {r}")

    # Dumpear pesos de la red
    if input("Desea guardar los pesos en un archivo de texto? [y/n]: ") == "y":
        with open("saved_weights.txt", "a+") as f:
            f.write(f"\n\n{LR = }\n{HIDDEN_LAYER_PERCEPTRONS = }\n{HIDDEN_LAYERS = }\n{ITERACIONES = }\n")
            f.write(str(mlp.weights))
            f.write("\n\n" + "-"*100)
