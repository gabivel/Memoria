import socket
import random
import copy
import string
import json
import time
HOST = input("Direccion que recibirá solicitudes: ")
PORT = int(input("Puerto a utilizar: "))
buffer_size = 1024

#--------------------------------------------------------------------------------------
def llenarMatriz(filas,columnas,nivel):
    tablero = []
    #se inicializa la matriz
    for inicializar in range(filas):
            tablero.append([0]*columnas)

    #se ingresan valores a la matriz
    for i in range(filas):
        for j in range(columnas):
            tablero[i][j] = nivel[i][j]
    return tablero


def llenarTabJuego(tablero):
    tab_juego = copy.deepcopy(tablero)
    for n_fila in range(len(tab_juego)):
        for valor in range(len(tab_juego[n_fila])):
            tab_juego[n_fila][valor]=string.ascii_uppercase[n_fila] + str(valor)
    return tab_juego

def mostrarTablero(tablero):
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

def obtenerValor(tablero_real,tablero_juego,casilla):
    for n_fila in range(len(tablero_juego)):
        for valor in range(len(tablero_juego[n_fila])):
            if tablero_juego[n_fila][valor]==casilla:
                return tablero_real[n_fila][valor]
    



def nivelEscogido(nivel):
    if nivel==1:
        filas=4;columnas=4
        nivel_p = [['llave','mesa','mango','plata'],['mora','libro','dulce','globo'],
                ['llave','mesa','mango','plata'],['mora','libro','dulce','globo']]

        #se mezclan las opciones
        random.shuffle(nivel_p)
        for x in nivel_p:
            random.shuffle(x)

        tablero_real = llenarMatriz(filas,columnas,nivel_p)
        return tablero_real
    elif nivel==2:
        filas=6;columnas=6
        nivel_a = [['mono','azul','mar','vaca','negro','pato'],['menta','avion','rosa','gato','perro','pollo'],
                    ['coco','pluma','buho','fresa','flor','nube'],['mono','azul','mar','fresa','negro','pato'],
                    ['menta','avion','rosa','gato','perro','pollo'],['coco','pluma','buho','vaca','flor','nube']]

        #se mezclan las opciones
        random.shuffle(nivel_a)
        for z in nivel_a:
            random.shuffle(z)

        tablero_real = llenarMatriz(filas,columnas,nivel_a)
        return tablero_real

def checarPar(tablero_real,tablero_juego,casilla1,casilla2):    
    if(obtenerValor(tablero_real,tablero_juego,casilla1)==obtenerValor(tablero_real,tablero_juego,casilla2)):
        print(obtenerValor(tablero_real,tablero_juego,casilla1),obtenerValor(tablero_real,tablero_juego,casilla2))
        return True
        #mandar actualizacion del tablero
    else:
        print("oh no, las casillas no son iguales")
        return False

def casillaAleatoria(tablero_juego):
    randomfila = random.randrange(len(tablero_juego))
    randomcolumna = random.randrange(len(tablero_juego[0]))
    return tablero_juego[randomfila][randomcolumna]

def casillaRepetida(casilla1,casilla2):
    #Verifica que no escojas la misma casilla
    if(casilla1==casilla2):
        print ("Oh no! Encogiste casillas iguales, vamos de nuevo:")
        return True#esta repetida la casilla
    return False#son casillas diferentes

def casillaVolteada(tablero_juego,casilla):
    for n_fila in range(len(tablero_juego)):
        for valor in range(len(tablero_juego[n_fila])):
            if tablero_juego[n_fila][valor]!=casilla1:
                return False#casilla disponible
    return True #no se encontro casilla a destapar

def actualizarTablero(tablero_real,tablero_juego,casilla):
    valor_real = obtenerValor(tablero_real,tablero_juego,casilla)
    for n_fila in range(len(tablero_juego)):
        for valor in range(len(tablero_juego[n_fila])):
            if tablero_juego[n_fila][valor]==casilla:
                tablero_juego[n_fila][valor]=valor_real
            #else:
                #tablero_juego = tablero_juego
    return tablero_juego

def tableroCompleto(tablero_juego,tablero_real):
    for n_fila in range(len(tablero_juego)):
        for valor in range(len(tablero_juego[n_fila])):
            if tablero_juego[n_fila][valor]!=tablero_real[n_fila][valor]:
                return False

    return True


#--------------------------------------------------------------------------------------------------------------------------------------

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP para el juego de memoria está disponible :)")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        #Esperando el nivel
        nivel = int(Client_conn.recv(buffer_size))
        puntos_usuario = 0
        puntos_servidor = 0
        turno_usuario = True
        tablero_real = nivelEscogido(nivel)
        tablero_juego = llenarTabJuego(tablero_real)
        mostrarTablero(tablero_real)
        
        #Se envia el tablero al cliente, de acuerdo a su nivel escogido
        bytesToSend = json.dumps(tablero_juego)
        print("Enviando tablero a", Client_addr)
        Client_conn.sendall(bytesToSend.encode())

        #Comienza el juego
        inicio_tiempo = time.time()

        while tableroCompleto(tablero_juego,tablero_real)==False:

            #el turno del usuario depende de los aciertos que tenga
            turno_enviar = str(turno_usuario)
            Client_conn.sendall(str.encode(turno_enviar)) 
            if turno_usuario==True:
                print("\nTurno del usuario")
                casilla1 = Client_conn.recv(buffer_size)
                casilla1 = casilla1.decode('utf-8')
                casilla2 = Client_conn.recv(buffer_size)
                casilla2 = casilla2.decode('utf-8')
                print("casilla1: {}, casilla2: {}".format(casilla1,casilla2))


                #se obtienen los valores de cada casilla y se envian al usuario
                casilla1_real = obtenerValor(tablero_real,tablero_juego,casilla1)
                casilla2_real = obtenerValor(tablero_real,tablero_juego,casilla2)
                print("Real1: {}, Real2: {}".format(casilla1_real,casilla2_real))

                #Envio de casillas
                Client_conn.sendall(str.encode(casilla1_real))
                Client_conn.sendall(str.encode(casilla2_real))

                #verificacion de los pares seleccionados
                if(checarPar(tablero_real,tablero_juego,casilla1,casilla2)):
                    #se actualuza el tablero
                    tablero_juego = actualizarTablero(tablero_real,tablero_juego,casilla1)
                    tablero_juego = actualizarTablero(tablero_real,tablero_juego,casilla2)
                    puntos_usuario+=1

                else:#los pares no son iguales
                    #El turno es para el servidor
                    turno_usuario = False

            #turno del servidor
            elif turno_usuario==False:
                print("\nTurno del servidor")
                #continuar con el turno del servidor
                continuar = Client_conn.recv(buffer_size)
                continuar = continuar.decode('utf-8')

                if(continuar=="1"):
                    casilla1 = casillaAleatoria(tablero_juego)
                    casilla2 = casillaAleatoria(tablero_juego)
                    while casilla1==casilla2:
                        casilla1 = casillaAleatoria(tablero_juego)
                        casilla2 = casillaAleatoria(tablero_juego)
                    while casillaVolteada(tablero_juego,casilla1) or casillaVolteada(tablero_juego,casilla2):
                        casilla1 = casillaAleatoria(tablero_juego)
                        casilla2 = casillaAleatoria(tablero_juego)

                    print("Cas1_servidor: {}, Cas2_servidor: {}".format(casilla1,casilla2))
                    
                    #Obtener valores de las casillas
                    casilla1_real = obtenerValor(tablero_real,tablero_juego,casilla1)
                    casilla2_real = obtenerValor(tablero_real,tablero_juego,casilla2)
                    print("Cas1_destapada: {}, Cas2_destapada: {}".format(casilla1_real,casilla2_real))

                    #enviando nombre de las casillas
                    Client_conn.sendall(str.encode(casilla1))
                    Client_conn.sendall(str.encode(casilla2))

                    #Enviando valores de casillas al usuario para que las vea
                    Client_conn.sendall(str.encode(casilla1_real))
                    Client_conn.sendall(str.encode(casilla2_real))
                    
                    #verificar pares seleccionados
                    if(checarPar(tablero_real,tablero_juego,casilla1,casilla2)):
                        #se manda la actualizacion del par encontrado
                        tablero_juego = actualizarTablero(tablero_real,tablero_juego,casilla1)
                        tablero_juego = actualizarTablero(tablero_real,tablero_juego,casilla2)
                        puntos_servidor += 1

                    else:#Casillas del servidor no son iguales
                        #Se regresa el turno al cliente
                        turno_usuario = True
                else:#El jugador quiere jugar contra si mismo
                    turno_usuario = True

        fin_tiempo = time.time()
        print("El tiempo de jugada fue de {} ".format(fin_tiempo-inicio_tiempo))

        #enviar al usuario si gano, perdio o empato
        if(puntos_usuario>puntos_servidor):
            Client_conn.sendall(str.encode("G")) 
        elif(puntos_usuario<puntos_servidor):
            Client_conn.sendall(str.encode("P")) 
        elif(puntos_usuario==puntos_servidor):
            Client_conn.sendall(str.encode("E")) 

        print("Usuario: ",puntos_usuario)
        print("Servidor: ",puntos_servidor)
        
        '''msgFromServer = input("respuesta al cliente:")
        bytesToSend = str.encode(msgFromServer)
        print("Enviando respuesta a", Client_addr)
        Client_conn.sendall(bytesToSend)'''