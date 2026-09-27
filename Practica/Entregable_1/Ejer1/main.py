import os
import sys
sys.path.append("../..") 
import emulador_MR


inputDir = "input"

#inputDir1 = "input1"
#inputDir2 = "input2"

outputDir = "output"
tmpDir = "tmp"

# id local - id visitante - votante local - votante visitante 

## JOB 1

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


# <id equipo - votos>
def fred(key, values, context):
    cantX = context["limite"]
    suma=0
    for v in values:
        suma += v

    context.write(key, suma)




if __name__ == "__main__":

    cantX = input("Ingrese el limite: ")
    print(cantX)
    
    job = emulador_MR.Job(inputDir, tmpDir, fmap, fred)
    job.setCombiner(fcom)
    success = job.waitForCompletion()


    job.setParams({"limite": cantX})


    print("Proceso terminado. Revisa la carpeta output.")
    ## el result queda en la carpeta tmp, no en output

   
