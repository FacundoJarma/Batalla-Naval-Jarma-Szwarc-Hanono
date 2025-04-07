import random

N: int = 10
tableroJugador1: list[list[bool]] = [[False for _ in range(N)] for _ in range(N)]
tableroMarcadoJugador1: list[list[str]] =  [["⬛" for _ in range(N)] for _ in range(N)]

tableroJugador2: list[list[bool]] = [[False for _ in range(N)] for _ in range(N)]
tableroMarcadoJugador2: list[list[str]] =  [["⬛" for _ in range(N)] for _ in range(N)]

print("[!] Momento de poner los barcos!")

def colocarBarcos(tablero: list[list[bool]], jugador: int ):
    CantidadBarcos: int = 10; 
    barcosPuestos: int = 0

    while barcosPuestos != CantidadBarcos: 
        #Poner los barcos
        x: int = int(input("Jugador" + str(jugador) + " elegi en que X poner el barco: "))
        y: int =  int(input("Jugador" + str(jugador) + " elegi en que Y poner el barco: "))

        if not tablero[y][x]:
            barcosPuestos += 1
            tablero[y][x] = True
            print("[+] Se coloco el barco en Y: " + str(y) + " y en X: " + str(x))
        else:
            print("[-] NO se puede. Ya hay un barco en Y: " + str(y) + " y en X: " + str(x))

colocarBarcos(tableroJugador1, 1)
colocarBarcos(tableroJugador2, 2)


print("[!] Momento de JUGAR!")

barcosRestantes: int = CantidadBarcos
intentos: int = 20

def graficarTablero():
    for i in range(N):
        for j in range(N):
            print(tableroMarcado[i][j], end=" ")
        print()

while barcosRestantes != 0 or intentos != 0:
    userY: int = int(input("Ingresa la cordenada en Y:"))
    userX: int = int(input("Ingresa la cordenada en X:"))

    if not (0 <= userY < N and 0 <= userX < N):
        print("[!] Coordenadas fuera del rango.")
        continue

    if(tableroMarcado[userY][userX] != "⬛"):
        print("[!] Ya elejiste esa casilla!!")
        continue

    intentos -= 1

    if tablero[userY][userX]:
        print("[+] Acertaste! Habia un barco.")
        tableroMarcado[userY][userX] = "🔲"
        barcosRestantes -= 1
    else:
        print("[-] Uops! NO habia un barco.")
        tableroMarcado[userY][userX] = "🔳"
    
    print("Intento restantes: " + str(intentos))
    graficarTablero()
    
    if barcosRestantes == 0:
        print("Ganaste!")

if barcosRestantes > 0:
        print("Perdiste!")