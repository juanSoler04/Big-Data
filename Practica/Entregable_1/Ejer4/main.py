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
inputSt = os.path.join(BASE_DIR, "inputSt")
outputDir = os.path.join(BASE_DIR, "output")
#tmpDir = os.path.join(BASE_DIR, "tmp")

#----------- ENUNCIADO ---------------- #
#Implemente una solución MapReduce que devuelva todos los equipos (locales para
#platinium, visitantes para premium y ambos (locales y visitantes) para estándar) que
#resulten de:
#𝑋 = [𝑃𝑙𝑎𝑡 − (𝑃𝑟𝑒𝑚 ∪ 𝐸𝑠𝑡)] ∪ [𝑃𝑟𝑒𝑚 − (𝑃𝑙𝑎𝑡 ∪ 𝐸𝑠𝑡)] ∪ [𝐸𝑠𝑡 − (𝑃𝑙𝑎𝑡 ∪ 𝑃𝑟𝑒𝑚)]


#In: <idLocal, idVisitante, votosLocal, votosVisitante>
#locales y visitantes para standar
def fmapSt(key, values, context):
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    context.write(id_local, "ST")
    context.write(id_visitante, "ST")

#In: <idLocal, idVisitante, votosLocal, votosVisitante>
#visitantes para premium
def fmapPr(key, values, context):
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    context.write(id_visitante, "PR")

#In: <idLocal, idVisitante, votosLocal, votosVisitante>
#Locales para platinium
def fmapPl(key, values, context):
    data = values.split()
    id_local = key
    id_visitante = data[0]
    votos_local = int(data[1])
    votos_visitante = int(data[2])
    context.write(id_local, "PL")


#In: <idEquipo, PR/PL/ST>
def fredCombinado(key, values, context):
    pr=0
    pl=0
    st=0
    for v in values:
        if(v=="PR"):
            pr=1
        elif(v=="PL"):
            pl=1
        elif(v=="ST"):
            st=1

    if (pl+pr+st ==1 ):
        equipo = key
        context.write(equipo,"")

    
if __name__ == "__main__":

    job = emulador_MR.Job(inputPl, outputDir, fmapPl, fredCombinado)
    job.addInputPath(inputPr, fmapPr)
    job.addInputPath(inputSt, fmapSt)
    success = job.waitForCompletion()
    print("Proceso terminado. Revisa la carpeta output.")
