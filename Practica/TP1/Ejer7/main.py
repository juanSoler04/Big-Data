from datetime import date
import random
import sys
# "../.." le dice a Python: sube un nivel (a TP1) y luego sube otro (a la raíz)
sys.path.append("../..") 
import emulador_MR


# Usamos rutas relativas simples porque ya estamos dentro de la carpeta ejer1
inputDir = "input"
outputDir = "output"

def fmap(key, value, context):
    # en KEY voy a tener el DNI
    clave = random.randint(1, 30)
    nombre, dia, mes, anio, inversion = value.split("\t")

    context.write(clave, (key, nombre, dia, mes, anio, inversion))
        
def fred(key, values, context):
    max_nombre = None
    max_dni = None
    cant_Inversion=0
    cant_Personas=0
    prom_Edad=0
    suma_edades =0

    hoy = date.today()

    for dni,nom,dia,mes,anio,inv in values:
        nacimiento = date(int(anio), int(mes), int(dia))

        dni = int(dni)

        inv = int(inv)

        cant_Inversion+=inv

        cant_Personas+=1

        edad = hoy.year - nacimiento.year
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1

        suma_edades += edad

        if (max_dni is None or dni>max_dni):
            max_dni = dni
            max_nombre = nom

    prom_Edad = suma_edades / cant_Personas if cant_Personas > 0 else 0

    context.write(key, (max_dni,max_nombre,cant_Inversion,cant_Personas,prom_Edad))



if __name__ == "__main__":
    # Agregamos el prefijo 'emulador_mr.' antes de Job
    job = emulador_MR.Job(inputDir, outputDir, fmap, fred)
    success = job.waitForCompletion()
    
    print("Proceso terminado. Revisa la carpeta output.")

# deberia con un script aparte repasar el output final
