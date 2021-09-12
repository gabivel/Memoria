import socket
import json
import copy
import time
print("*** Bienvenido ***")
HOST = input("Ingrese la dirección a la que se quiere conectar: ")
PORT = int(input("Ingrese el puerto destino: "))
#serverAddressPort = (HOST, PORT)
buffer_size = 1024

def mostrarTablero(tablero):
    print("Tablero actual")
    for n_fila in range(len(tablero)):
        for valor in tablero[n_fila]:
            print("\t", valor, end=" ")
        print()

def casillaValida(tablero,casilla):
    lista_posibles = []
    for n_fila in range(len(tablero)):
        for valor in range(len(tablero[n_fila])):
            lista_posibles.append(string.ascii_uppercase[n_fila] + str(valor))
    
    if casilla in lista_posibles:
        return True
    else:
        return False

#def casillaVolteada(tablero,casilla):

def validarCasillas(casilla1,casilla2):
    #Verifica el rango del tablero, que sea valido 
    if(casillaValida(tablero,casilla1)==False or casillaValida(tablero,casilla2)==False):
        print("No son validos esos valores, intentalo otra vez!")
        return False
    
    #Verifica que no escojas la misma casilla
    elif(casilla1==casilla2):
        print ("Oh no! Encogiste casillas iguales, vamos de nuevo:")
        return False

    #elif(casillaVolteada(tablero_real,tablero_juego,casilla1)==True or casillaVolteada(tablero_real,tablero_juego,casilla2)==True)
    #   print("Casilla ya volteada, intentalo de nuevo")

def actualizarTablero(tablero,casilla,cas_actual):
    for n_fila in range(len(tablero)):
        for valor in range(len(tablero[n_fila])):
            if tablero[n_fila][valor]==casilla:
                tablero[n_fila][valor]=cas_actual
    return tablero

def mostrarTableroTemporal(tablero_t,casilla1,casilla2,cas1_actual,cas2_actual):
    print()
    for n_fila in range(len(tablero_t)):
        for valor in range(len(tablero_t[n_fila])):
            if tablero_t[n_fila][valor]==casilla1:
                print("\t",cas1_actual, end=" ")
                #tablero_t[n_fila][valor]=cas1_actual
            elif tablero_t[n_fila][valor]==casilla2:
                print("\t",cas2_actual, end=" ")
                #tablero_t[n_fila][valor]=cas2_actual
            else:
                print("\t",tablero_t[n_fila][valor], end=" ")
        print()

def tableroCompleto(tablero_cpy,tablero):
    for n_fila in range(len(tablero_cpy)):
        for valor in range(len(tablero_cpy[n_fila])):
            if tablero_cpy[n_fila][valor]==tablero[n_fila][valor]:
                return False

    return True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    while(True):
        print("************************************************")
        print("¿Que deseas hacer?")
        print("0: Jugar")
        print("1: Salir")

        seleccion=int(input())
        print("************************************************")
        if seleccion==0:
            print("Escoge tu nivel:")
            print("1: Principiante")
            print("2: Avanzado")
            nivel=input()
            print("Enviando nivel:...")
            TCPClientSocket.sendall(nivel.encode())
            print("Esperando tablero...")
            tablero = TCPClientSocket.recv(buffer_size)
            tablero = json.loads(tablero.decode())
            tablero_cpy = copy.deepcopy(tablero)
            mostrarTablero(tablero)
            inicio_tiempo = time.time()
            while tableroCompleto(tablero_cpy,tablero)==False:
                mi_turno = TCPClientSocket.recv(buffer_size)
                turno = str(mi_turno, 'utf-8')
        
                #turno del cliente
                if(turno=="True"):
                    print("\n\nIngresa las casillas a destapar (lo conforman una letra MAYUSCULA y un numero)")
                    casilla1 = str(input("Casilla 1 a voltear:"))
                    casilla2 = str(input("Casilla 2 a voltear:"))

                    #Enviando casillas a verificar
                    TCPClientSocket.sendall(casilla1.encode())
                    TCPClientSocket.sendall(casilla2.encode())

                    #Recibiendo valores de las casillas
                    cas1_actual = str(TCPClientSocket.recv(buffer_size), 'utf-8')
                    cas2_actual = str(TCPClientSocket.recv(buffer_size), 'utf-8')

                    #Esto es para actualizar del lado del cliente
                    #Del lado del servidor tambien se hace        
                    if(cas1_actual==cas2_actual):
                        print("\nTuviste un par correcto, tienes +1 punto\n")
                        tablero = actualizarTablero(tablero,casilla1,cas1_actual)
                        tablero = actualizarTablero(tablero,casilla2,cas2_actual)
                        mostrarTablero(tablero)

                    else:
                        print("\nNO tuviste un par correcto")
                        mostrarTableroTemporal(tablero,casilla1,casilla2,cas1_actual,cas2_actual)

                #Es el turno del servidor
                elif(turno=="False"):
                    print("\n\nEs el turno de tu oponente, ¿Continuar?\n1: Si\n2:Escoger pares de nuevo")
                    continuar = str(input())
                    TCPClientSocket.sendall(continuar.encode())

                    #jugar con el servidor
                    if continuar == "1":
                        #Nombres de las casillas
                        cas1 = str(TCPClientSocket.recv(buffer_size), 'utf-8')
                        cas2 = str(TCPClientSocket.recv(buffer_size), 'utf-8')
                        #valores de las casillas
                        cas1_actual = str(TCPClientSocket.recv(buffer_size), 'utf-8')
                        cas2_actual = str(TCPClientSocket.recv(buffer_size), 'utf-8')

                        if(cas1_actual==cas2_actual):
                            tablero = actualizarTablero(tablero,cas1,cas1_actual)
                            tablero = actualizarTablero(tablero,cas2,cas2_actual)
                            print("\nTu oponente tiene +1 punto, encontro: {}, {}".format(cas1_actual,cas2_actual))
                            mostrarTablero(tablero)
                        else:
                            print("\nTu oponente NO tuvo par correcto: {}, {}\n".format(cas1_actual,cas2_actual))
                            mostrarTableroTemporal(tablero,cas1,cas2,cas1_actual,cas2_actual)
            fin_tiempo = time.time()
            tiempo = fin_tiempo - inicio_tiempo
            print("\nJUEGO TERMINADO")
            resultado = str(TCPClientSocket.recv(buffer_size), 'utf-8')
            if resultado== "G":
                print("\nHa ganado la partida")
            elif resultado == "P":
                print("\nHa perdido la partida")
            elif resultado == "E":
                print("Esto fue un empate")
            print("\nTiempo de partida: {} seg".format(tiempo))

        elif seleccion==1:
            break
        else:
            print("ERROR! Ingrese 1 o 0")
    