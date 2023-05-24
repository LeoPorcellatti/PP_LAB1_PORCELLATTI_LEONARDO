import re 
import json
import csv

with open("C:\\Users\\user\\Desktop\\Programación\\Examen\\dt.json") as archivo:
    data_nba = json.load(archivo)

lista_nba = data_nba["jugadores"]

def imprimir_dato(dato:str):
    '''
    Recibe un dato str y lo muestra por consola
    '''
    print(dato)

def mostrar_jugadores(lista:list):
    '''
    Recibe una lista y devuevle Nombre y posición por consola

    Parametro
    lista:list

    Retorna:
    '''
    for jugador in lista:
        nombre_y_posicion = (f"Nombre Jugador: {jugador['nombre']} - Posición: {jugador['posicion']}")
        imprimir_dato(nombre_y_posicion)
    
mostrar_jugadores(lista_nba)