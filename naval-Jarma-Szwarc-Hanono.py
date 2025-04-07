N: int = 10
tableroJugador1: list[list[bool]] = [[False for _ in range(N)] for _ in range(N)]
tableroMarcadoJugador1: list[list[str]] =  [["⬛" for _ in range(N)] for _ in range(N)]

tableroJugador2: list[list[bool]] = [[False for _ in range(N)] for _ in range(N)]
tableroMarcadoJugador2: list[list[str]] =  [["⬛" for _ in range(N)] for _ in range(N)]

# Definir códigos de colores
RED: str = "\033[31m"
GREEN: str = "\033[32m"
BLUE: str = "\033[34m"
RESET: str = "\033[0m"

def colocarBarcos(tablero: list[list[bool]], jugador: int ):
    print(f"\n\n{BLUE}[!] Momento de poner los barcos del jugador {jugador}{RESET}")
    CantidadBarcos: int = 2
    barcosPuestos: int = 0

    while barcosPuestos != CantidadBarcos: 
        #Poner los barcos
        x: int = int(input(f"{BLUE}Jugador {jugador}, elige en qué X poner el barco: {RESET}"))
        y: int = int(input(f"{BLUE}Jugador {jugador}, elige en qué Y poner el barco: {RESET}"))

        if not tablero[y][x]:
            barcosPuestos += 1
            tablero[y][x] = True
            print(f"{GREEN}[+] Se colocó el barco en Y: {y} y en X: {x}{RESET}")
        else:
            print(f"{RED}[-] No se puede. Ya hay un barco en Y: {y} y en X: {x}{RESET}")

colocarBarcos(tableroJugador1, 1)
colocarBarcos(tableroJugador2, 2)

print(f"{BLUE}[!] Momento de JUGAR!{RESET}")

barcosRestantesDeJugador1: int = 2
barcosRestantesDeJugador2: int = 2

intentosJugador1: int = 20
intentosJugador2: int = 20

turno: int = 1

def graficarTablero(tablero: list[list[bool]]):
    for i in range(N):
        for j in range(N):
            print(tablero[i][j], end=" ")
        print()

def jugarTurno(tablero: list[list[bool]], tableroMarcado: list[list[str]], intentos: int, barcosRestantes: int):
    userY: int = int(input(f"{BLUE}Jugador {turno} ingresa la coordenada en Y: {RESET}"))
    userX: int = int(input(f"{BLUE}Jugador {turno} ingresa la coordenada en X: {RESET}"))

    if not (0 <= userY < N and 0 <= userX < N):
        print(f"{RED}[!] Coordenadas fuera del rango.{RESET}")
        return -1, barcosRestantes

    if tableroMarcado[userY][userX] != "⬛":
        print(f"{RED}[!] ¡Ya elegiste esa casilla!{RESET}")
        return -1, barcosRestantes

    if tablero[userY][userX]:
        print(f"{GREEN}[+] ¡Acertaste! Había un barco.{RESET}")
        tableroMarcado[userY][userX] = "🔲"
        barcosRestantes -= 1
    else:
        print(f"{RED}[-] ¡Uops! No había un barco.{RESET}")
        tableroMarcado[userY][userX] = "🔳"

    graficarTablero(tableroMarcado)

    if barcosRestantes == 0:
        return 1, barcosRestantes

    return 0, barcosRestantes

while (barcosRestantesDeJugador1 > 0 and barcosRestantesDeJugador2 > 0) or (intentosJugador1 > 0 and intentosJugador2 > 0): 

    if turno == 1:
        print(f"{BLUE}[!] Turno de Jugador 1{RESET}")
        resultado, barcosRestantesDeJugador2 = jugarTurno(tableroJugador2, tableroMarcadoJugador2, intentosJugador1, barcosRestantesDeJugador2)
        if resultado == 1:
            print(f"{GREEN}[+] Jugador 1 GANA{RESET}")
            break
        elif resultado == 0:
            intentosJugador1 -= 1
            print(f"{BLUE}Intentos restantes: {intentosJugador1}{RESET}")
            print(f"{BLUE}Barcos restantes (Jugador 2): {barcosRestantesDeJugador2}{RESET}")
            turno = 2

    else:
        print(f"{BLUE}[!] Turno de Jugador 2{RESET}")
        resultado, barcosRestantesDeJugador1 = jugarTurno(tableroJugador1, tableroMarcadoJugador1, intentosJugador2, barcosRestantesDeJugador1)
        if resultado == 1:
            print(f"{GREEN}[+] Jugador 2 GANA{RESET}")
            break
        elif resultado == 0:
            intentosJugador2 -= 1
            print(f"{BLUE}Intentos restantes: {intentosJugador2}{RESET}")
            print(f"{BLUE}Barcos restantes (Jugador 1): {barcosRestantesDeJugador1}{RESET}")
            turno = 1
