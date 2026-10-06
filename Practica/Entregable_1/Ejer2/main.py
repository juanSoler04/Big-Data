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


inputSt = os.path.join(BASE_DIR, "inputSt")
inputPl = os.path.join(BASE_DIR, "inputPl")
outputDir = os.path.join(BASE_DIR, "output")
#tmpDir = os.path.join(BASE_DIR, "tmp")

#----------- ENUNCIADO ---------------- #
# Implemente una solución MapReduce que devuelva todos los equipos que jugando
#como visitantes tuvieron más apuestas a ganador, que las recibidas por el equipo local.
#Interesa saber cuáles son los equipos, que cumplen la condición, en los datasets
#estándar y platinium (intersección de conjuntos).


#In: <idLocal, idVisitante, votosLocal, votosVisitante>
def fmapSt(key, values, context):
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    if(votos_visitante > votos_local):
        context.write((id_local,id_visitante), "ST")

#In: <idLocal, idVisitante, votosLocal, votosVisitante>
def fmapPl(key, values, context):
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    if(votos_visitante > votos_local):
        context.write((id_local,id_visitante), "PL")

#In: <idLocal, idVisitante, votosLocal, votosVisitante, ST/PL>
def fredCombinado(key, values, context):
    st=0
    pl=0
    for v in values:
        if(v=="ST"):
            st=1
        elif(v=="PL"):
            pl=1
        #context.write(key, v)
    if st and pl:
        equipoL,equipoV = key
        context.write(equipoV, "")
    
#OBS de la resolución: Debido a que en los datasets (apuestasEstandar y apuestasPremium),
# No existia un mismo partido (idLocal,idVisitante) el cual cumpla con la premisa de que
# "el visitante haya ganado en cantidad de apuestas respecto al local", decidimos añadir
# manualmente la tupla: 100	101	10	200.   


#pregunta: será que en cada map solamente se debe rescatar el equipo visitante que ganó
# y ver si el visitante ganador se repite para ambos datasets? (independientemente de si 
#es el mismo partido)
if __name__ == "__main__":

    job = emulador_MR.Job(inputSt, outputDir, fmapSt, fredCombinado)
    job.addInputPath(inputPl, fmapPl)
    success = job.waitForCompletion()


    print("Proceso terminado. Revisa la carpeta output.")

   
