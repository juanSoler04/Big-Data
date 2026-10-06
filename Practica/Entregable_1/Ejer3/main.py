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


inputPr = os.path.join(BASE_DIR, "inputPr")
inputPl = os.path.join(BASE_DIR, "inputPl")
outputDir = os.path.join(BASE_DIR, "output")
#tmpDir = os.path.join(BASE_DIR, "tmp")

#----------- ENUNCIADO ---------------- #
# Implemente una solución MapReduce que devuelva todos los equipos que jugando
#como local tuvieron más de X (parámetro de la cosulta) veces más de apuestas que las
#recibidas por el equipo visitante. Interesa saber los equipos que cumplen esa condición
#que son elegidos por los usuarios PLATINIUM, pero no por los usuarios PREMIUM
#(diferencia de conjuntos)


#In: <idLocal, idVisitante, votosLocal, votosVisitante>
def fmapPl(key, values, context):
    factor = int(context["factor"])
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    if(votos_local > votos_visitante*factor):
        context.write(id_local, "PL")

#In: <idLocal, idVisitante, votosLocal, votosVisitante>
def fmapPr(key, values, context):
    factor = int(context["factor"])
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    if(votos_local > votos_visitante*factor):
        context.write(id_local, "PR")

#In: <idLocal, PR/PL>
def fredCombinado(key, values, context):
    pr=0
    pl=0
    for v in values:
        if(v=="PR"):
            pr=1
        elif(v=="PL"):
            pl=1
        #context.write(key, v)
    if pl and (not pr) :
        equipo = key
        context.write(equipo, "")

    
if __name__ == "__main__":

    factor = input("Ingrese el factor X: ")    
    job = emulador_MR.Job(inputPl, outputDir, fmapPl, fredCombinado)
    job.addInputPath(inputPr, fmapPr)
    job.setParams({"factor": factor})
    success = job.waitForCompletion()
    print("Proceso terminado. Revisa la carpeta output.")
