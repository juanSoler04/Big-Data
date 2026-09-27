import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR = BASE_DIR

while not os.path.exists(os.path.join(CURRENT_DIR, "emulador_MR.py")):
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    if PARENT_DIR == CURRENT_DIR:
        raise FileNotFoundError("No se encontro emulador_MR.py en las carpetas superiores")
    CURRENT_DIR = PARENT_DIR

sys.path.insert(0, CURRENT_DIR)

import emulador_MR


inputDir = os.path.join(BASE_DIR, "input")
outputDir = os.path.join(BASE_DIR, "output")
tmpDir = os.path.join(BASE_DIR, "tmp")

#----------- ENUNCIADO ---------------- #

# Implemente una solución MapReduce que devuelva todos los equipos (sin importar si
# jugaron como locales o como visitantes) que tuvieron más de X (parámetro de la
# consulta) apuestas como ganador. Esta consulta debe hacerse para los datasets
# premium y estándar(unión de conjuntos).
# <id local, id visitante , votante local , votante visitante>
def fmap(key, value, context):
    data = value.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])

    context.write(id_local, votos_local)
    context.write(id_visitante, votos_visitante)

def fcom(key, values, context):
    suma=0
    for v in values:
        suma += v
    context.write(key, suma)


# <id equipo, votos>
def fred(key, values, context):
    cantX = int(context["limite"])
    suma=0
    for v in values:
        suma += v
    if(cantX < suma):
        context.write(key, suma)


if __name__ == "__main__":

    cantX = input("Ingrese el limite: ")
    print(cantX)

    
    job = emulador_MR.Job(inputDir, outputDir, fmap, fred)
    job.setCombiner(fcom)
    job.setParams({"limite": cantX})
    success = job.waitForCompletion()


    print("Proceso terminado. Revisa la carpeta output.")

   
