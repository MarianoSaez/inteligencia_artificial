from random import randint
from MLP import MLP
from GeneralizationGraph import Grapher
import numpy as np
import cv2
import argparse as ap
from tqdm import tqdm
import multiprocessing as mp

parser = ap.ArgumentParser()
parser.add_argument("-l", "--learningrate", default=0.5, type=float)
parser.add_argument("-p", "--hiddenlayerperc", default=100, type=int)
parser.add_argument("--layers", default=1, type=int)
parser.add_argument("-i", "--iter", default=500, type=int)
parser.add_argument("--folder", type=str, default="original")
parser.add_argument("--extention", type=str, default="jpg")
parser.add_argument("--identif", type=str, default="59161")
parser.add_argument("--runtimegraph", type=bool, action=ap.BooleanOptionalAction)
parser.add_argument("--graphstep", type=int, default=5)
args = parser.parse_args()

# IMAGE SETTINGS
SET = args.folder
BASE_PATH = f"./img/{SET}/"
EXTENTION = args.extention
ID = args.identif
IMG_SIZE = 80*96
IMG_LIMIT = 5
IMG_RANGE = sorted([i for i in range(1, IMG_LIMIT + 1)]*2)
PERSON_RANGE = ["A", "B"]*5
TEST_IMAGES = [f"6A{ID}", f"7A{ID}", f"8A{ID}", f"6B{ID}", f"7B{ID}", f"8B{ID}"]

# MLP SETTINGS
LR = args.learningrate
HIDDEN_LAYER_PERCEPTRONS = args.hiddenlayerperc
HIDDEN_LAYERS = args.layers
ITERACIONES = args.iter

# PLOT SETTINGS
SAVE_PATH = "./resultados/"
RUNTIME_PLOT = args.runtimegraph
RUNTIME_PLOT_STEP = args.graphstep

if __name__ == "__main__":
    
    # Leer imagenes
    print("CARGANDO IMAGENES")
    img_list = []
    path_list = []
    for gesture, person in zip(IMG_RANGE, PERSON_RANGE):
        path = f"{BASE_PATH}{gesture}{person}{ID}.{EXTENTION}"
        print(f"CARGANDO: {path}")
        flat_img = cv2.imread(path, 0).flatten()/255
        if person == "A":
            flat_img = np.append(flat_img, [0])
        else:
            flat_img = np.append(flat_img, [1])

        img_list.append(flat_img)
        path_list.append(path)

    # Instanciar y entrenar MLP
    print("CREANDO RED NEURONAL")
    print([HIDDEN_LAYER_PERCEPTRONS]*HIDDEN_LAYERS)
    mlp = MLP(IMG_SIZE, [HIDDEN_LAYER_PERCEPTRONS]*HIDDEN_LAYERS + [1], learning_rate=LR)
    
    print("ENTRENANDO RED NEURONAL")
    global_err_hist = {}
    runtime_test_hist = {}
    for i in tqdm(range(ITERACIONES)):
        w_hist, err_hist = mlp.train(img_list)
        
        # Comprobacion en tiempo de ejecucion
        if RUNTIME_PLOT:
            test_path_list = []
            for test_img in TEST_IMAGES:
                test_path = f"{BASE_PATH}{test_img}.{EXTENTION}"
                test_path_list.append(test_path)
                flat_img = cv2.imread(test_path, 0).flatten()/255
                r = mlp.run(flat_img)
                if str(flat_img) not in runtime_test_hist:
                    runtime_test_hist[str(flat_img)] = []
                runtime_test_hist[str(flat_img)] += [r]

            if (i+1)%RUNTIME_PLOT_STEP==0:
                def task():
                    g = Grapher()
                    g.graph(runtime_test_hist, test_path_list)

                p = mp.Process(target=task)
                p.start()

        for k in err_hist:
            if k not in global_err_hist:
                global_err_hist[k] = err_hist[k]
            else:
                global_err_hist[k] += err_hist[k]


    # Mostrar graficas de errores
    g = Grapher()
    g.graph(global_err_hist, path_list, save=SAVE_PATH + f"LR{LR}_HLP{HIDDEN_LAYER_PERCEPTRONS}_{HIDDEN_LAYERS}HL_ITER{ITERACIONES}_SET{SET}_ID_{randint(0, 1_000_000)}.png")

    try:
        # Ejecutar
        for test_img in TEST_IMAGES:
            flat_img = cv2.imread(f"{BASE_PATH}{test_img}.{EXTENTION}", 0).flatten()/255
            r = mlp.run(flat_img)
            print(f"EXAMPLE: {test_img}.{EXTENTION} --> {r}")
    except Exception:
        pass

    # Dumpear pesos de la red
    if input("Desea guardar los pesos en un archivo de texto? [y/n]: ") == "y":
        with open("saved_weights.txt", "a+") as f:
            f.write(f"\n\n{LR = }\n{HIDDEN_LAYER_PERCEPTRONS = }\n{HIDDEN_LAYERS = }\n{ITERACIONES = }\n")
            f.write(str(mlp.weights))
            f.write("\n\n" + "-"*100)
