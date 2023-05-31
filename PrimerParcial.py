from posixpath import split
import re 
import json
import csv

# path original "PP_LAB1_PORCELLATTI_LEONARDO\PP_LAB1_PORCELLATTI_LEONARDO\dt.json"
with open("dt.json", "r", encoding = "utf-8") as archivo:
    data_nba = json.load(archivo,)

lista_nba = data_nba["jugadores"]
separador = "*****************************************************"

def imprimir_dato(dato:str):
    '''
    Recibe un dato str y lo muestra por consola

    Parametro:
    dato:str
    '''
    print(dato)

def convertir_lista_str(list:list)->str:
    '''
    Recibe una lista y la convierte en str, con el salto de linea como parametro

    Parametro:
    lista:list

    Retorna:
    lista_str:str
    '''
    lista_str = "\n".join(list)
    return lista_str

def replace_guion_bajo (cadena:str)->str:
    '''
    Recibe una cadena y reemplaza los "_" con " "
    
    Parametro:
    cadena:str

    Retorna:
    cadena_modificada:str
    '''
    if "_" in cadena:
        cadena_modificada = cadena.replace("_", " ")        
    else:
        cadena_modificada = cadena
    return cadena_modificada

def convertir_str_int_float(numero:str):
    '''
    Recibe un número en formato string y lo convierte a flotante
    
    Parametro
    numero:str

    Retorna:
    numero_float:float
    numero_int:int
    '''
    valor_modificado = numero.replace(",", ".")
    if re.match(r'^[0-9.]+$', valor_modificado):
        if "." in valor_modificado:
            numero_convertido = float(valor_modificado)
            return numero_convertido
        else:
            numero_convertido = int(valor_modificado)
            return numero_convertido
    print("Ingrese un número válido.")
    return -1

# PUNTO 1 
def mostrar_jugadores_y_parametro (lista:list, parametro:str):
    '''
    Recibe una lista y devuevle Nombre y posición por consola

    Parametro
    lista:list
    '''    
    if len(lista) == 0:
        print("Lista Vacia")
    else:        
        for jugador in lista:
            nombre_y_posicion = (f"{separador}\nNombre Jugador: {jugador['nombre']} - {parametro} : {jugador[parametro]}")            
            imprimir_dato(nombre_y_posicion)

# PUNTO 2
def indice_jugador(lista:list)->str:
    '''
    Recibe una lista de jugadores y retorna el nombre del jugador junto su número de indice

    Parametro:
    lista:list

    Retorna:
    jugador_por_indice_str:str
    '''
    jugador_por_indice = []
    contador_indice = 0 
    for jugador in lista:
        contador_indice +=1
        nombre_mas_indice = f"{contador_indice} - {jugador['nombre']}"   
        jugador_por_indice.append(nombre_mas_indice)
        jugador_por_indice_str = "\n".join(jugador_por_indice)            
                 
    return jugador_por_indice_str

def mostrar_estadisticas(lista:list)->dict:
    '''
    Recibe una lista y un indice seleccionado por el usuario para evaluar los datos de ese jugador

    Parametro
    lista:list

    Retorna:
    jugador_seleccionado:dict
    '''
    jugador_por_indice_str = indice_jugador(lista)
    imprimir_dato(jugador_por_indice_str)
    indice_seleccionado = (input("Seleccione el Nro. de Jugador que desea elegir: "))
    if re.match(r'^([1-9]|1[0-2]$)', indice_seleccionado):
        indice_seleccionado_int = convertir_str_int_float(indice_seleccionado)
        indice_coincide = indice_seleccionado_int -1   
        if indice_coincide < len(lista):     
            estadisticas_jugador =(lista[indice_coincide]['estadisticas'])
            print(f"{separador}\n{(lista[indice_coincide]['nombre'])}")
            for clave, valor in estadisticas_jugador.items():
                clave_valor = f"{clave}: {valor}"
                clave_valor_modificado = replace_guion_bajo(clave_valor)
                imprimir_dato(clave_valor_modificado)
            jugador_selecionado = lista[indice_coincide] 
            return dict(jugador_selecionado)
        else:
            print("Opción invalida")
            return None
    else:
        print("Opción invalida")
        return None   

# PUNTO 3
def obtener_valores(jugador:dict)->list:
    '''
    Recibe el diccionario del punto anterior y devuelve sus valores 
    
    Parametro:
    jugador:dict

    Retorna:
    valores:list
    '''

    valores = []
    for clave, valor in jugador.items():
        if type(valor) is dict:
            valores.extend(obtener_valores(valor))
        elif type(valor) is list:
            pass
        else:
            valores.append(valor)
    return valores

def exportar_jugador_csv(jugador:dict):
    '''
    Recibe un diccionario con los datos del jugador selecionado en el item anteior y lo exporta a un archivo csv

    Parametro:
    lista:list
    '''

    path = "PP_LAB1_PORCELLATTI_LEONARDO\PP_LAB1_PORCELLATTI_LEONARDO\dt.csv"
    columnas = []
    for clave in jugador:
        if clave != "logros" and clave != "estadisticas" and clave not in columnas:
            columnas.append(clave)

    estadisticas = jugador['estadisticas']
    for clave in estadisticas:        
        if clave not in columnas:
            clave_modificada = replace_guion_bajo(clave)
            columnas.append(clave_modificada)

    with open(path, "w", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(columnas)
        valores = obtener_valores(jugador)        
        writer.writerow(valores)
        
# PUNTO 4
def revisar_coincidencia (lista:list, nombre:str)->list:
    '''
    Recibe un nombre y verifica si coincide con algún jugador de la lista
    
    Parametros:
    lista:list
    nombre:str

    Retorna:
    jugador:list
    '''
    flag_coincidencia = True 
    jugadores_coincidencia = []
    patron = r"{0}+".format(nombre)
    for jugador in lista:
        if re.search(patron, jugador['nombre']):
            flag_coincidencia = False 
            jugadores_coincidencia.append(jugador)
    if flag_coincidencia:
        print("No se encontró ningún jugador")

    return jugadores_coincidencia        

def mostrar_logros(lista:list):
    '''
    Recibe una lista de jugadores y permite al usuario buscar a un jugador por su nombre
    
    Parametro:
    lista:list
    '''

    jugador_por_indice_str = indice_jugador(lista)
    imprimir_dato(jugador_por_indice_str)
    seleccion_usuario = input("Ingrese el nombre del jugador cuyos logros desea ver: ").lower().title()
    jugadores_coincidencia = revisar_coincidencia(lista, seleccion_usuario)
    for jugador in lista:
        if jugador['nombre'] == seleccion_usuario:
            for logro in jugador['logros']:
                if re.search(r'\bFama\b', logro):
                    print(f"{jugador['nombre']} es miembro del hall de la fama!")
                    return 
            print(f"{jugador['nombre']} no tuvo ese logro")
            return     

    for jugador in jugadores_coincidencia:
        logros = convertir_lista_str(jugador['logros'])
        jugador_logros = f"{separador}\nNombre: {jugador['nombre']} - Logros: \n{logros}"
        imprimir_dato(jugador_logros)
    else:
        return    

# PUNTO 5
def calcular_promedio_equipo (lista:list, dato:str)->float:
    '''
    Recibe la lista de jugadores y el dato cuyo promedio queremos calcular

    Parametro:
    lista:list

    retorna
    promedio:float
    '''
    suma = 0

    if len(lista) == 0:
        print("Lista vacia")
        return -1 

    for jugador in lista:
        if 'estadisticas' in jugador:
            estadisticas = jugador['estadisticas']
            if dato in estadisticas:
                promedio_puntos_jugador = estadisticas[dato]
                suma += promedio_puntos_jugador                
                
    promedio_puntos_equipo = suma
    return round(promedio_puntos_equipo,2)

def quick_sort(lista:list, parametro:str, orden:str)->list:
    '''
    Recibe una lista y la ordena según el parametro y orden deseado

    Parametros:
    lista:list
    parametro:str
    orden:str

    Retorna:
    lista_izq:list
    '''
    
    lista_izq = []
    lista_der = []

    if (len(lista)<=1):
        return lista

    else:
        pivot = lista[0]
        if orden == 'ascendente':
            for jugador in lista[1:]:
                if parametro in jugador:
                    if jugador[parametro] > pivot[parametro]:
                            lista_der.append(jugador)
                    else:
                        lista_izq.append(jugador) 
                elif 'estadisticas' in jugador:
                    estadisticas = jugador['estadisticas']
                    if parametro in estadisticas:
                        if jugador['estadisticas'][parametro] > pivot['estadisticas'][parametro]:
                            lista_der.append(jugador)
                        else:
                            lista_izq.append(jugador)
                                       
        elif orden == 'descendente':
            for jugador in lista[1:]:
                if parametro in jugador:
                    if jugador[parametro] < pivot[parametro]:
                            lista_der.append(jugador)
                    else:
                        lista_izq.append(jugador)    
                elif 'estadisticas' in jugador:
                    estadisticas = jugador['estadisticas']
                    if parametro in estadisticas:
                        if jugador['estadisticas'][parametro] < pivot['estadisticas'][parametro]:
                            lista_der.append(jugador)
                        else:
                            lista_izq.append(jugador)
                              
        else:
            print("Tipo de parametro incorrecto, solo se acepta (asc o desc)...")
            return None

    lista_izq = quick_sort(lista_izq, parametro, orden)
    lista_izq.append(pivot)
    lista_der = quick_sort(lista_der, parametro, orden)
    lista_izq.extend(lista_der)       
    return lista_izq

# PUNTO 6:
def validar_info_jugador (lista:list):
    '''
    Recibe la lista de jugadores y le pide al usuario que ingrese el nombre y ver si ese jugador es miembro del Salón de la Fama.

    Parametro:
    lista:list
    '''
    jugador_por_indice_str = indice_jugador(lista)
    imprimir_dato(jugador_por_indice_str)
    seleccion_usuario = input("Ingrese el nombre del jugador cuyos logros desea ver: ").lower().title()

    if len(lista) == 0:
        print("Error, la lista esta vacia")
        return -1
    
    for jugador in lista:
        if jugador['nombre'] == seleccion_usuario:
            for logro in jugador['logros']:
                if re.search(r'\bFama\b', logro):
                    print(f"{jugador['nombre']} es miembro del hall de la fama!")
                    return 
            print(f"{jugador['nombre']} no tuvo ese logro")
            return        
    print("No se encontró al jugador en la lista.\nRevisa el nombre ingresado")       

# PUNTOS 7 / 8 / 9 / 13 / 14 / 19
def mayor_dato(lista:list, dato:str):
    '''
    Recibe la lista de jugadores y el dato a comparar para ver cual es el que más valor tiene

    Parametros:
    lista:list
    dato:str
    '''
    jugador_maximo_valor = lista[0]
    maximo_valor = 0 
    for jugador in lista:
        if 'estadisticas' in jugador:
            estadisticas = jugador['estadisticas']
            if dato in estadisticas:
                dato_a_comparar = estadisticas[dato]
                if dato_a_comparar > jugador_maximo_valor['estadisticas'][dato]:
                    jugador_maximo_valor = jugador
                    maximo_valor = dato_a_comparar
        elif dato in jugador:
            dato_a_comparar = jugador[dato]
            if dato_a_comparar > jugador_maximo_valor[dato]:
                jugador_maximo_valor = jugador
                maximo_valor = dato_a_comparar
    if "_" in dato:
        dato_modificado = dato.replace("_", " ")        
    else:
        dato_modificado = dato
    
    nombre_y_dato = f"{separador}\nEl jugador con mayor número de {dato_modificado} ({maximo_valor}) es {jugador_maximo_valor['nombre']}"    
      
    imprimir_dato (nombre_y_dato)

# PUNTO 10 / 11 / 12 / 15 / 18

def comparar_con_usuario (lista:list, dato:str)->list:
    '''
    Recibe la lista de jugadores y le pide al usuario que ingrese el valor de un dato para compararlo con el de los jugadores, retornando a los que promediado más valor que el dato pasado

    Parametros:
    lsita:list
    dato:str

    Retorna:
    lista_jugadores:list
    '''
    lista_jugadores = []
    valor_usuario = input("Ingrese el número con el que desee comparar: ")
    valor_validado = (convertir_str_int_float(valor_usuario))
    if valor_validado >= 0:
        for jugador in lista:
            if 'estadisticas' in jugador:
                estadisticas = jugador['estadisticas']
                if dato in estadisticas:
                    if jugador['estadisticas'][dato] >= valor_validado:
                        lista_jugadores.append(jugador)        

    if len(lista_jugadores) >= 1:
            if dato != 'porcentaje_tiros_de_campo':
                dato_modificado = replace_guion_bajo(dato) 
                print(f"{separador}\nLos de jugadores que superan al número {valor_usuario} en {dato_modificado}\n{separador}") 
                for jugador in lista_jugadores:                
                    nombre_y_dato = f"Nombre: {jugador['nombre']} - {dato_modificado}: {jugador['estadisticas'][dato]}"
                    imprimir_dato(nombre_y_dato)        
    else:
        print("No hay jugadores que hayan superado ese número")

    return lista_jugadores

# PUNTO 16
def promedio_menos_dato (lista:list, dato:str)->float:
    '''
    Recibe una lista de jugadores en la cual calcula el promedio del dato solicitado y le resta el monto del jugador con menos valor

    Parametro:
    lista:list

    Retorna:
    promedio_disminuido:float
    '''
    
    promedio = calcular_promedio_equipo (lista, dato)
    orden = 'ascendente'
    lista_ordenada = quick_sort(lista, dato, orden)
    promedio_mas_bajo = lista_ordenada[0]
    promedio_disminuido = promedio - promedio_mas_bajo['estadisticas'][dato]
    dato_modificado = replace_guion_bajo(dato)
    
    print(f"{separador}\nEl {dato_modificado} del equipo es {promedio_disminuido}\nEl jugador excluido es: {promedio_mas_bajo['nombre']} con {promedio_mas_bajo['estadisticas'][dato]} {dato_modificado}")
    return promedio_disminuido
# PUNTO 17
def contar_logros(lista:list):
    '''
    Recibe la lista que y verifica el valor de los datos de logros para contabilizarlos

    Parametro:
    lista:list

    '''
    
    max_logros = 0
    jugador_con_max_logros = ""

    for jugador in lista:
        if len(jugador["logros"]) > max_logros:
            max_logros = len(jugador["logros"])
            jugador_con_max_logros = jugador["nombre"]
            logros = convertir_lista_str(jugador['logros'])
    
    suma = 0
    lineas = logros.split("\n")

    for linea in lineas:
        primer_elemento = linea.split(" ")[0]
        if not primer_elemento.isdigit():
            primer_elemento = "1"
        suma += int(primer_elemento)
  
    
    nombre_y_dato = f"{separador}\nEl jugador con la mayor cantidad de logros conseguidos es {jugador_con_max_logros} con {max_logros} logros:\n{logros}\nLa suma de todos estos logros es {suma}"
    imprimir_dato(nombre_y_dato)    
            
# PUNTO 20
def comparar_ordenar (lista:list, dato:str, parametro:str):
    '''
    Recibe la lista de jugadores y permite al usuario ingresar el valor de un dato para compararlo con el de los jugadores, ordenandolos por el parametro deseado

    Parametros:
    lista:list
    dato:str
    parametro:str
    '''

    lista_jugadores = comparar_con_usuario(lista, dato)
    orden = 'ascendente'
    lista_jugadores_ordenada = quick_sort(lista_jugadores, parametro, orden)
    dato_modificado = replace_guion_bajo(dato)
    for jugador in lista_jugadores_ordenada:
        nombre_y_posicion = f"Nombre: {jugador['nombre']} - Posición: {jugador[parametro]} - {dato_modificado}: {jugador['estadisticas'][dato]}"
        imprimir_dato(nombre_y_posicion)

# PUNTO 23
def generar_ranking(lista:list, parametro_uno:str, parametro_dos:str, parametro_tres:str, parametro_cuatro:str):
    '''
    Recibe la lista de jugadores y devuelve una lista con los jugadores y su posición en el ranking para los parametros solicitados:

    Parametros:
    lista: list - Lista de jugadores.
    parametro_uno: str - Nombre del primer parámetro.
    parametro_dos: str - Nombre del segundo parámetro.
    parametro_tres: str - Nombre del tercer parámetro.
    parametro_cuatro: str - Nombre del cuarto parámetro.

    Retorna:
    columnas: list 
    posiciones: dict
    '''

    orden = 'descendente'

    posicion_parametro_uno = quick_sort(lista, parametro_uno, orden)
    posicion_parametro_dos = quick_sort(lista, parametro_dos, orden)
    posicion_parametro_tres = quick_sort(lista, parametro_tres, orden)
    posicion_parametro_cuatro = quick_sort(lista, parametro_cuatro, orden)

    columnas = ["Jugador",]
    parametro_uno_modificado = replace_guion_bajo(parametro_uno).title() 
    parametro_dos_modificado = replace_guion_bajo(parametro_dos).title() 
    parametro_tres_modificado = replace_guion_bajo(parametro_tres).title() 
    parametro_cuatro_modificado = replace_guion_bajo(parametro_cuatro).title()  
    columnas.append(parametro_uno_modificado)
    columnas.append(parametro_dos_modificado)
    columnas.append(parametro_tres_modificado)
    columnas.append(parametro_cuatro_modificado)

    diccionario_parametro_uno = {}
    diccionario_parametro_dos = {}
    diccionario_parametro_tres = {}
    diccionario_parametro_cuatro = {}

    for i in range(len(posicion_parametro_uno)):
        jugador = posicion_parametro_uno[i]        
        nombre_jugador = jugador['nombre']
        posicion_jugador = i + 1
        diccionario_parametro_uno[nombre_jugador] = posicion_jugador

    for i in range(len(posicion_parametro_dos)):
        jugador = posicion_parametro_dos[i]        
        nombre_jugador = jugador['nombre']
        posicion_jugador = i + 1
        diccionario_parametro_dos[nombre_jugador] = posicion_jugador

    for i in range(len(posicion_parametro_tres)):
        jugador = posicion_parametro_tres[i]        
        nombre_jugador = jugador['nombre']
        posicion_jugador = i + 1
        diccionario_parametro_tres[nombre_jugador] = posicion_jugador

    for i in range(len(posicion_parametro_cuatro)):
        jugador = posicion_parametro_cuatro[i]        
        nombre_jugador = jugador['nombre']
        posicion_jugador = i + 1
        diccionario_parametro_cuatro[nombre_jugador] = posicion_jugador

    posiciones_jugador = {
        'diccionario_parametro_uno':diccionario_parametro_uno,
        'diccionario_parametro_dos':diccionario_parametro_dos,
        'diccionario_parametro_tres':diccionario_parametro_tres,
        'diccionario_parametro_cuatro':diccionario_parametro_cuatro
    }   

    return lista, posiciones_jugador, columnas


def exportar_ranking_csv (lista:list, posiciones:dict, columnas:list):
    '''
    Recibe las posiciones de los jugadores para cada parametro y la columnas con los parametros a mostar en formato csv

    Parametro:
    posiciones:dict
    columnas:list
     '''

    path = "PP_LAB1_PORCELLATTI_LEONARDO\\PP_LAB1_PORCELLATTI_LEONARDO\\ranking.csv"
    parametro_uno = "puntos_totales"
    parametro_dos = "rebotes_totales"
    parametro_tres = "asistencias_totales"
    parametro_cuatro = "robos_totales"
    lista_nba, posiciones, columnas = generar_ranking(lista, parametro_uno, parametro_dos, parametro_tres, parametro_cuatro)



    with open(path, "w", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(columnas)
        for jugador in lista:
            nombre_jugador = jugador['nombre']
            valores = [
                posiciones['diccionario_parametro_uno'].get(nombre_jugador, ''),
                posiciones['diccionario_parametro_dos'].get(nombre_jugador, ''),
                posiciones['diccionario_parametro_tres'].get(nombre_jugador, ''),
                posiciones['diccionario_parametro_cuatro'].get(nombre_jugador, '')
            ]
            writer.writerow([nombre_jugador] + valores)

# PUNTO 24 
def contador_posiciones(lista:list, dato:str):
    '''
    Recibe una lista de jugadores e indica la cantida de jugadores por posicion que encontramos

    Parametro:
    lista:list
    dato:str
    '''
    posiciones = {}
    for jugador in lista:
        if dato in jugador:
            posicion = jugador[dato]
            if posicion not in posiciones:
                posiciones[posicion] = 1
            else:
                posiciones[posicion] +=1
    for clave, valor in posiciones.items():
        dato_valor = f'{dato} {clave}: {valor}'
        imprimir_dato(dato_valor)

# PUNTO 25

def obtener_cantidad_all_star(jugador: dict):
    for logro in jugador["logros"]:
        if "All-Star" in logro:
            cantidad_all_star = int(logro.split(" ")[0])
            return cantidad_all_star
    return 0

def mostrar_all_star_jugadores(lista_jugadores: list):
    lista_jugadores_ordenados = sorted(lista_jugadores, key=obtener_cantidad_all_star, reverse=True)
    for jugador in lista_jugadores_ordenados:
        cantidad_all_star = obtener_cantidad_all_star(jugador)
        print("{0} ({1} veces All-Star)".format(jugador["nombre"], cantidad_all_star))


# PUNTO 26
def mejor_jugador_estadistica(lista:list):
    '''
    Recibe la lista de jugadores y devuelve el mejor jugador por estadística junto con su valor

    Parametro:
    lista:list
    '''
    mejores_estadisticas = {}

    for jugador in lista:
        if 'estadisticas' in jugador:
            estadisticas = jugador['estadisticas']
            for estadistica, valor in estadisticas.items():
                if estadistica not in mejores_estadisticas or valor > mejores_estadisticas[estadistica][0]:
                    mejores_estadisticas[estadistica] = (valor, jugador['nombre'])

    for estadistica, (valor, jugador) in mejores_estadisticas.items():
        estadistica_modificada = replace_guion_bajo(estadistica)
        print(f"Mayor cantidad de {estadistica_modificada}: {jugador} ({valor})")


    

# PUNTO 27

def mejores_estadisticas(lista:list):
    '''
    Recibe la lista de Jugadores y muestra quien es el jugador con mejores estadísticas

    Parámetros:
    lista: list - Lista de jugadores.
    '''
    
    mejores_estadisticas = 0
    mejor_jugador = lista[0]

    for jugador in lista:
        suma = 0
        if 'estadisticas' in jugador:
            estadisticas = jugador['estadisticas']
            for clave, valor in estadisticas.items():
                suma += valor
                promedio_estadisticas = suma / len(jugador['estadisticas'])
                if promedio_estadisticas > mejores_estadisticas:
                    mejor_jugador = jugador
                    mejores_estadisticas = promedio_estadisticas
    print(f"El mejor jugador es {mejor_jugador['nombre']} con {round(mejores_estadisticas,2)} puntos de estadísticas total")



# MENU Y VALIDACIÓN OPCIONES
def validar_opcion(menu:str)->str:
    '''
    Define el menú de opciones y le pide al usuario que ingrese la opción deseada, validando que se trate de un RegEx y retornando el mismo si se trata de un dato válido o -1 caso cotrario

    Parametro:
    menu:str

    Retorna:
    opcion: str, la opción ingresada por el usuario en mayúsculas si es válida, o -1 en caso contrario. 
    '''    
    
    imprimir_dato(separador)
    imprimir_dato(menu)
    opcion = input("Ingrese el ejercicio que desea ejecutar: ")
    # uso re.match para ver si es una opción esta entra 0-9 "O" 10-19 "O" 20-23
    if re.match(r'^([0-9]|1[0-9]|20|2[3-7])$', opcion):
        return int(opcion)
    else:
        return -1



def parcial_app(lista_nba:list):
    '''
    Recibe la lista de héroes para poder ejecutar los ejercicios correspondientes 

    Parámetro:
    personajes: list

    Retorna:
    None
    '''
    lista_menu  = ["1- Listar Jugadores",
            "2- Mostrar estadísticas de un jugador",
            "3- Exportar datos del jugador del punto 2 a CSV",
            "4- Mostrar logros de un jugador",
            "5- Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team, ordenado por nombre de manera ascendente",
            "6- Permitir al usuario ingresar el nombre de un jugador y mostrar si ese jugador es miembro del Salón de la Fama del Baloncesto",
            "7- Calcular y mostrar el jugador con la mayor cantidad de rebotes totales",
            "8- Calcular y mostrar el jugador con el mayor porcentaje de tiros de campo",
            "9- Calcular y mostrar el jugador con la mayor cantidad de asistencias totales",
            "10- Permitir al usuario ingresar un valor y mostrar los jugadores que han promediado más puntos por partido que ese valor",
            "11- Permitir al usuario ingresar un valor y mostrar los jugadores que han promediado más rebotes por partido que ese valor",
            "12- Permitir al usuario ingresar un valor y mostrar los jugadores que han promediado más asistencias por partido que ese valor",
            "13- Calcular y mostrar el jugador con la mayor cantidad de robos totales",
            "14- Calcular y mostrar el jugador con la mayor cantidad de bloqueos totales",
            "15- Permitir al usuario ingresar un valor y mostrar los jugadores que hayan tenido un porcentaje de tiros libres superior a ese valor",
            "16- Calcular y mostrar el promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido",
            "17- Calcular y mostrar el jugador con la mayor cantidad de logros obtenidos",
            "18- Permitir al usuario ingresar un valor y mostrar los jugadores que hayan tenido un porcentaje de tiros triples superior a ese valor",
            "19- Calcular y mostrar el jugador con la mayor cantidad de temporadas jugadas",
            "20- Permitir al usuario ingresar un valor y mostrar los jugadores, ordenados por posición en la cancha, que hayan tenido un porcentaje de tiros de campo superior a ese valor",
            "23- BONUS!",
            "24- Extra 1!", 
            "25- Extra 2!",
            "26- Extra 3!",
            "27- Extra 4!",
            "0- Salir"]            
    menu = "\n".join(lista_menu) 
    jugador_seleccionado = None 
    while True:
        
        opcion = validar_opcion(menu)        
        match opcion:
            case 1:
                parametro = 'posicion'
                mostrar_jugadores_y_parametro(lista_nba, parametro)
            case 2:                
                jugador_seleccionado = mostrar_estadisticas(lista_nba)
            case 3:
                if jugador_seleccionado is None:
                    print("Primero realiza el punto 2 (mostrar estadísticas) para seleccionar un jugador.")
                else:
                    exportar_jugador_csv(jugador_seleccionado)
            case 4:
                mostrar_logros(lista_nba)
            case 5:      
                dato = 'promedio_puntos_por_partido'          
                parametro = 'nombre'
                orden = 'ascendente'                
                lista_ordenada = quick_sort(lista_nba, parametro, orden) 
                promedio = (calcular_promedio_equipo(lista_nba, dato))               
                print(f"{separador}\nPromedio de puntos por partido del equipo: {promedio}\n***Promedio por jugador***")  
                for jugador in lista_ordenada:
                    nombre_y_dato = f"Nombre: {jugador['nombre']} - Promedio: {jugador['estadisticas'][dato]} "
                    imprimir_dato(nombre_y_dato)
            case 6:
                validar_info_jugador(lista_nba)
            case 7:
                parametro = "rebotes_totales"                    
                mayor_dato(lista_nba, parametro)
            case 8:
                parametro = "porcentaje_tiros_de_campo"
                mayor_dato(lista_nba, parametro)
            case 9:
                parametro = "asistencias_totales"
                mayor_dato(lista_nba, parametro)
            case 10:
                dato = "promedio_puntos_por_partido"
                comparar_con_usuario(lista_nba, dato)
            case 11:
                dato = "promedio_rebotes_por_partido"
                comparar_con_usuario(lista_nba, dato)
            case 12:
                dato = "promedio_asistencias_por_partido"
                comparar_con_usuario(lista_nba, dato)  
            case 13:
                parametro = "robos_totales"
                mayor_dato(lista_nba, parametro) 
            case 14:
                parametro = "bloqueos_totales"
                mayor_dato(lista_nba, parametro) 
            case 15:
                dato = "porcentaje_tiros_libres"
                comparar_con_usuario(lista_nba, dato) 
            case 16:
                dato = 'promedio_puntos_por_partido'
                promedio_menos_dato(lista_nba, dato)
            case 17:
                contar_logros(lista_nba)
            case 18:
                dato = "porcentaje_tiros_triples"
                comparar_con_usuario(lista_nba, dato) 
            case 19:
                parametro = "temporadas"
                mayor_dato(lista_nba, parametro)
            case 20:
                dato = "porcentaje_tiros_de_campo"
                parametro = 'posicion'
                comparar_ordenar(lista_nba, dato, parametro)             
            case 23:
                parametro_uno = "puntos_totales"
                parametro_dos = "rebotes_totales"
                parametro_tres = "asistencias_totales"
                parametro_cuatro = "robos_totales"
                lista, posiciones, columnas = generar_ranking(lista_nba, parametro_uno, parametro_dos, parametro_tres, parametro_cuatro)
                exportar_ranking_csv(lista, posiciones, columnas)
            case 24:
                dato = "posicion"
                contador_posiciones(lista_nba, dato)
            case 25:
                mostrar_all_star_jugadores(lista_nba)
            case 26:
                mejor_jugador_estadistica(lista_nba)
            case 27:
                mejores_estadisticas(lista_nba)
            case 0:
                print("Adios...")
                break
            case _:
                print("Opción invalida")

parcial_app(lista_nba)

