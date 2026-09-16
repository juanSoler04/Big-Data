import sys
# "../.." le dice a Python: sube un nivel (a TP1) y luego sube otro (a la raíz)
sys.path.append("../..") 
import emulador_MR


# Usamos rutas relativas simples porque ya estamos dentro de la carpeta ejer1
inputDir = "input"
outputDir = "output"
tmpDir = "tmp"

## JOB 1

def fmap(key, value, context):
    words = value.split()
    for w in words:
        context.write(w, 1)

#COMBINER

def fcom(key, values, context):
    c=0
    for v in values:
        c = c + v
    context.write(key, c)

        
def fred(key, values, context):
    c=0
    for v in values:
        c=c+v
    context.write(key, c)

## JOB 2

def fmap2(key, value, context):
    context.write("global", (key, int(value)))     ## asi le llega todo al mismo reducer 


def fred2(key, values, context):
    min_cant = None
    min_palabra = None
    max_cant = None
    max_palabra = None
    total = 0
    suma = 0
    suma_cuadrados = 0

    for palabra, cant in values:
        if min_cant is None or cant < min_cant:
            min_cant = cant
            min_palabra = palabra

        if max_cant is None or cant > max_cant:
            max_cant = cant
            max_palabra = palabra

        total += 1
        suma += cant
        suma_cuadrados += cant ** 2

    promedio = suma / total
    varianza = (suma_cuadrados / total) - promedio ** 2
    desvio = varianza ** 0.5

    context.write("minimo", min_cant)
    context.write("palabra_minima", min_palabra)
    context.write("maximo", max_cant)
    context.write("palabra_maxima", max_palabra)
    context.write("promedio", promedio)
    context.write("desvio", desvio)




if __name__ == "__main__":

    # Agregamos el prefijo 'emulador_mr.' antes de Job
    job1 = emulador_MR.Job(inputDir, tmpDir, fmap, fred)
    job1.setCombiner(fcom)
    success = job1.waitForCompletion()

    job2 = emulador_MR.Job(tmpDir, outputDir, fmap2, fred2)
    success = job2.waitForCompletion()


    
    print("Proceso terminado. Revisa la carpeta output.")

   
