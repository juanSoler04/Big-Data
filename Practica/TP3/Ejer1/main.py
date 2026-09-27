import os
import sys
sys.path.append("../..") 
import emulador_MR


inputDir = "input"
outputDir = "output"
tmpDir = "tmp"

## JOB 1

def fmap(key, value, context):
    vars = context["incognitas"]
    coefs = value.split("\t")

    # El índice 0 corresponde al término independiente
    res = float(coefs[0])
    for i in range(15):
        res = res + vars[i] * float(coefs[i+1])

    context.write(key, res)


        
def fred(key, values, context):
    res=0
    for v in values:
        res = v
    context.write(key, res)




if __name__ == "__main__":

    error = 0.01
    dif = 1
    incog = [1] * 15        ## cheq para que es esto
    while (dif >=error):
        job = emulador_MR.Job(inputDir, tmpDir, fmap, fred)
        coefs = {"incognitas" : incog}
        job.setParams(coefs)
        success = job.waitForCompletion()

        # 1. Abrir y leer el archivo de texto generado en 'tmpDir'
        # 2. Extraer los 15 nuevos valores resultantes
        # 3. Calcular la diferencia matemática entre los nuevos valores y la lista 'incog'
        # 4. Asignar esa diferencia a la variable 'dif'
        # 5. Reemplazar la lista 'incog' con los 15 nuevos valores obtenidos
        nuevos_incog = [0.0] * len(incog)
        resultado = os.path.join(tmpDir, "output.txt")

        with open(resultado, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                clave, valor = linea.rstrip("\n").split("\t", 1)
                indice = int(clave.removeprefix("var")) - 1
                nuevos_incog[indice] = float(valor)

        dif = max(abs(nuevo - anterior)
                  for nuevo, anterior in zip(nuevos_incog, incog))
        incog = nuevos_incog


    print("Proceso terminado. Revisa la carpeta output.")
    ## el result queda en la carpeta tmp, no en output

   
