import sys
# "../.." le dice a Python: sube un nivel (a TP1) y luego sube otro (a la raíz)
sys.path.append("../..") 
import emulador_MR


# Usamos rutas relativas simples porque ya estamos dentro de la carpeta ejer1
inputDir = "input"
outputDir = "output"

def fmap(key, value, context):
    vocales = 'aeiouAEIOU'  #declaro para preguntar despues

    for char in value:
        if char.isalpha():  # Solo si es una letra
            if char in vocales:
                context.write('vocal', 1)
            else:
                context.write('consonante', 1)
        elif char.isdigit():
                context.write('digito', 1)
        else:
            context.write('otro', 1)
        
def fred(key, values, context):
    c=0
    for v in values:
        c=c+1
    context.write(key, c)

#job = Job(inputDir, outputDir, fmap, fred)
#success = job.waitForCompletion()


if __name__ == "__main__":
    # Agregamos el prefijo 'emulador_mr.' antes de Job
    job = emulador_MR.Job(inputDir, outputDir, fmap, fred)
    success = job.waitForCompletion()
    
    print("Proceso terminado. Revisa la carpeta output.")
