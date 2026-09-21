import sys
sys.path.append("../..") 
import emulador_MR


# Usamos rutas relativas simples porque ya estamos dentro de la carpeta ejer1
inputDir = "input"
outputDir = "output"
tmpDir = "tmp"

# FORMATO DEL INPUT : <id_user, id_page, time>

## JOB 1A        -- jUNTA LOS TIEMPOS DE LA MISMA PAGINA PARA CADA USUARIO 

def fmapA(key, value, context):

    id_user = key
    data = value.split("\t")
    id_page = data[0]
    time = int(data[1]) # lo paso a entero para dsp sumarlo
    
    context.write((id_user,id_page),time) 

#COMBINER

def fcomA(key, values, context):
    suma = sum(values)  # esta notacion remplaza tener que hacer el for each
    context.write(key, suma )

        
def fredA(key, values, context):
    tot_Time=0

    for v in values:
        tot_Time+=v

    context.write(key, tot_Time)    #sigo usando como clave el id del user y de la pag

## JOB 2        SE ENCARGA DE VER LOS TIEMPOS DE CADA PAG Y SACAR MAX

def fmap2A(key, value, context):
    id_user = key
    data = value.split("\t")
    id_page = data[0]
    time_acum = int(data[1])

    context.write(id_user, (id_page,time_acum)) #envio la pag y su tiempo tot


def fred2A(key, values, context):
    max_Time = -1

    for v in values:
            id_page= v[0]
            time_acum = v[1]
            if (time_acum > max_Time):
                max_Time = time_acum
                max_Page = id_page

    context.write("Id User | Id Pag max visualizacion | max time : ", (key,max_Page, max_Time))
        ## MUESTRO LA LONG DEL PARRAFO Y SU CONTENIDO

# JOB 1B
def fmap1B(key, value, context):    # usa el tempDir generado por Job1A
    id_user = key

    context.write(id_user, 1) #separo por id user y le mando un 1 por pagina visitada

def fred1B(key, values, context):   #aca podria meter combiner para sumas parciales
    cant_pag=0

    for v in values:
        cant_pag+=v 

    context.write(key, cant_pag)   

# JOB 2B

def fmap2B(key, value, context):
    id_user = key
    cant_pag = int(value)
    

    context.write("user", (id_user,cant_pag)) 

def fred2B(key, values, context):
    max_Paginas = -1

    for v in values:
            id_user= v[0]
            cantPaginas = v[1]
            if (cantPaginas > max_Paginas):
                max_Paginas = cantPaginas
                max_User = id_user

    context.write("Id User | Paginas visitadas : ", (max_User,max_Paginas))


###### JOB C

def fmap1C(key, value, context):
    data = value.split("\t")
    id_page = data[0]

    context.write(id_page, 1)


def fred1C(key, values, context):
    tot_visitas = 0

    for v in values:
        tot_visitas += v

    context.write(key, tot_visitas)


def fmap2C(key, value, context):
    id_page = key
    visitas = int(value)

    context.write("global_max", (id_page, visitas))


def fred2C(key, values, context):
    max_visitas = -1
    max_page = ""

    for id_page, visitas in values:
        if visitas > max_visitas:
            max_visitas = visitas
            max_page = id_page

    context.write(
        "Pagina mas visitada | Visitas totales :",
        (max_page, max_visitas)
    )


if __name__ == "__main__":

    # Agregamos el prefijo 'emulador_mr.' antes de Job
    job1 = emulador_MR.Job(inputDir, tmpDir, fmapA, fredA)
    job1.setCombiner(fcomA)
    success = job1.waitForCompletion()


    job2 = emulador_MR.Job(tmpDir, outputDir, fmap2A, fred2A)
    success = job2.waitForCompletion()

    # --- RAMA B ---
    # lee de tmp_A1 aprovechando el trabajo previo
    jobB1 = emulador_MR.Job(tmpDir, "tmpDirB", fmap1B, fred1B)
    jobB1.waitForCompletion()

    jobB2 = emulador_MR.Job("tmpDirB", "output_B", fmap2B, fred2B)
    jobB2.waitForCompletion()

    # --- RAMA C ---
    jobC1 = emulador_MR.Job(inputDir, "tmp_C1", fmap1C, fred1C)
    jobC1.setCombiner(fcomA)
    jobC1.waitForCompletion()

    jobC2 = emulador_MR.Job("tmp_C1", "output_C", fmap2C, fred2C)
    jobC2.waitForCompletion()

    
    print("Proceso terminado. Revisa la carpeta output.")

   
