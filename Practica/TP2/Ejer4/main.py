import sys
# "../.." le dice a Python: sube un nivel (a TP1) y luego sube otro (a la raíz)
sys.path.append("../..") 
import emulador_MR


# Usamos rutas relativas simples porque ya estamos dentro de la carpeta ejer1
inputDir = "input"
outputDir = "output"
tmpDir = "tmp"

def leer_promedio_de_archivo(directorio):
    with open(directorio + "/output.txt", "r", encoding="latin-1") as archivo:
        for linea in archivo:
            clave, valor = linea.rstrip("\n").split("\t", 1)
            if clave == "promedio":
                return float(valor)

    raise ValueError("No se encontró la clave 'promedio' en el archivo de salida")

## JOB 1        -- Cuenta prom

def fmap(key, value, context):
    
    context.write(1, (len(value), 1) )  #clave general cte y la long del parrafo recibido

#COMBINER

def fcom(key, values, context):
    tot_longitudes=0
    tot_parrafos=0
    for v in values:
        tot_longitudes+=v[0]
        tot_parrafos+=v[1]
    context.write(key, (tot_longitudes,tot_parrafos) )

        
def fred(key, values, context):
    tot_longitudes=0
    tot_parrafos=0
    prom=0

    for v in values:
        tot_longitudes+=v[0]
        tot_parrafos+=v[1]

    prom = tot_longitudes / tot_parrafos
    context.write("promedio", prom)

## JOB 2

def fmap2(key, value, context):
    prom_Global = context ["prom_parrafos"]
    if len(value) > prom_Global:
        context.write(key, (len(value), value)) #envio el parrafo y su longitud


def fred2(key, values, context):

    for v in values:
        context.write("Parrafo mayor al promedio", (v[0], v[1]))
        ## MUESTRO LA LONG DEL PARRAFO Y SU CONTENIDO




if __name__ == "__main__":

    # Agregamos el prefijo 'emulador_mr.' antes de Job
    job1 = emulador_MR.Job(inputDir, tmpDir, fmap, fred)
    job1.setCombiner(fcom)
    success = job1.waitForCompletion()

    promedio_calculado = leer_promedio_de_archivo(tmpDir)

    job2 = emulador_MR.Job(inputDir, outputDir, fmap2, fred2)

    diccionario = {"prom_parrafos": promedio_calculado}
    job2.setParams(diccionario)

    success = job2.waitForCompletion()


    
    print("Proceso terminado. Revisa la carpeta output.")

   
