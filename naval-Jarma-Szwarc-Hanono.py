import os
import msvcrt

N: int = 10

from colorama import Fore, Back, Style, init
init(autoreset=True)

class Barco:
    def __init__(self, x: int, y: int, orientacion: str, longitud: int):
        self.x: int = x
        self.y: int = y
        self.longitud: int = longitud
        self.orientacion: str = orientacion
    
    def __str__(self) -> str:
        return f"Barco en X: {self.x}, Y: {self.y}, Orientación: {self.orientacion}, Longitud: {self.longitud}"

class Tablero:
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        self.matriz_barcos = [[False for _ in range(tamaño)] for _ in range(tamaño)]
        self.matriz_marcada = [["⬛" for _ in range(tamaño)] for _ in range(tamaño)]
    
    def colocar_barco(self, barco: Barco) -> bool:
        dx = 0
        dy = 0

        if barco.orientacion == "h":
            dx = 1
        elif barco.orientacion == "v":
            dy = 1
        else:
            print(Fore.RED + "Orientación inválida. Usa 'h' para horizontal o 'v' para vertical.")
            return False

        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            if not (0 <= nx < self.tamaño and 0 <= ny < self.tamaño):
                print(Fore.RED + "El barco se sale del tablero.")
                return False
            
            if self.matriz_barcos[ny][nx]:
                print(Fore.RED + f"Ya hay un barco en X: {nx}, Y: {ny}")
                return False

        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            self.matriz_barcos[ny][nx] = True

        self.graficar(show_ships=True)
        return True

    def graficar(self, show_ships: bool = False) -> None:
        for i in range(self.tamaño):
            fila = []
            for j in range(self.tamaño):
                celda = self.matriz_marcada[i][j]
                
                if celda == "⬛":
                    if show_ships and self.matriz_barcos[i][j]:
                        fila.append("🚢")
                    else:
                        fila.append(celda)
                else:
                    fila.append(celda)
            
            print(" ".join(fila))    

    def recibir_disparo(self, x: int, y: int) -> (bool, str):
        if not (0 <= y < self.tamaño and 0 <= x < self.tamaño):
            return False, Fore.RED + "Coordenadas fuera del rango." + Style.RESET_ALL

        if self.matriz_marcada[y][x] != "⬛":
            return False, Fore.YELLOW + "¡Ya elegiste esa casilla!" + Style.RESET_ALL

        if self.matriz_barcos[y][x]:
            self.matriz_marcada[y][x] = "🔲"
            return True, Fore.GREEN + "¡Acertaste! Había un barco." + Style.RESET_ALL
        else:
            self.matriz_marcada[y][x] = "🔳"
            return False, Fore.CYAN + "¡Uops! No había un barco." + Style.RESET_ALL

    def graficar_placeholder_de_barcos(self, barco):
        matriz_placeholder_barcos = [[False for _ in range(self.tamaño)] for _ in range(self.tamaño)]

        # Copiamos los barcos ya colocados
        for y in range(self.tamaño):
            for x in range(self.tamaño):
                if self.matriz_barcos[y][x]:
                    matriz_placeholder_barcos[y][x] = True

        dx = 0
        dy = 0

        if barco.orientacion == "h":
            dx = 1
        elif barco.orientacion == "v":
            dy = 1

        valor = True
        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            if not (0 <= nx < self.tamaño and 0 <= ny < self.tamaño):
                print(Fore.RED + "El barco se sale del tablero.")
                return False
            
            if self.matriz_barcos[ny][nx]:
                
                print(Fore.RED + f"Ya hay un barco en X: {nx}, Y: {ny}")
            
                return False
        for i in range(barco.longitud):
                nx = barco.x + i * dx
                ny = barco.y + i * dy
                matriz_placeholder_barcos[ny][nx] = True    

        for i in range(self.tamaño):
            fila = []
            for j in range(self.tamaño):
                celda = self.matriz_marcada[i][j]
                
                if celda == "⬛":
                    if  matriz_placeholder_barcos[i][j]:
                        fila.append("🚢")
                    else:
                        fila.append(celda)
                else:
                    fila.append(celda)
            
            print(" ".join(fila))  
            
        return True  
    

class Jugador:
    def __init__(self, nombre: str, tamaño_tablero: int, intentos: int, cantidad_barcos: int):
        self.nombre = nombre
        self.tablero = Tablero(tamaño_tablero)
        self.intentos = intentos
        self.cantidad_barcos = cantidad_barcos
        self.pedazos_barcos_restantes = 0
    
    def colocar_barcos(self):
        print(f"\n\n{Fore.MAGENTA}[!] {self.nombre}: Momento de poner tus barcos.{Style.RESET_ALL}")
        barcos_colocados = 0
        while barcos_colocados < self.cantidad_barcos:
            confirmed: bool = False
            orientacion = "h"
            longitud = int(input(f"{self.nombre} - Longitud del barco: "))
            
            x = 0
            y = 0
            print("Usa las teclas WASD para mover el barco o C para confirmar:")

            while not confirmed:
                if msvcrt.kbhit():
                    os.system("cls" if os.name == "nt" else "clear")
                    tecla = msvcrt.getch().decode('utf-8').lower()
                    
                    if tecla == 'w':
                        y -= 1
                    elif tecla == 'a':
                        x -= 1
                    elif tecla == 's':
                        y += 1
                    elif tecla == 'd':
                        x += 1
                    elif tecla == 'r':
                        if orientacion == "v":
                            orientacion = "h"
                        elif orientacion == "h":
                            orientacion = "v"
                    preBarco = Barco(x, y, orientacion, longitud)

                    if tecla == 'c':
                        if self.tablero.colocar_barco(preBarco):
                            confirmed = True
                            barcos_colocados += 1
                            self.pedazos_barcos_restantes += longitud
                            print(Fore.GREEN + f"[+] Barco colocado: {preBarco}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + "[-] No se pudo colocar el barco. Intenta de nuevo." + Style.RESET_ALL)
                    else:
                        if not self.tablero.graficar_placeholder_de_barcos(preBarco):
                            if tecla == 'w':
                                y += 1 
                            elif tecla == 'a':
                                x += 1
                            elif tecla == 's':
                                y -= 1
                            elif tecla == 'd':
                                x -= 1
                            elif tecla == 'r':
                                if orientacion == "v":
                                    orientacion = "h"
                                elif orientacion == "h":
                                    orientacion = "v"

    def jugar_turno(self, adversario: 'Jugador') -> bool:
        try:
            x = int(input(f"{self.nombre}, ingresa la coordenada en X para disparar: "))
            y = int(input(f"{self.nombre}, ingresa la coordenada en Y para disparar: "))
        except ValueError:
            print(Fore.RED + "Por favor ingresa valores numéricos válidos." + Style.RESET_ALL)
            return False

        acierto, mensaje = adversario.tablero.recibir_disparo(x, y)
        print(mensaje)
        adversario.tablero.graficar()
        if acierto:
            adversario.pedazos_barcos_restantes -= 1

        self.intentos -= 1
        print(Fore.MAGENTA + f"{self.nombre} tiene {self.intentos} intentos restantes." + Style.RESET_ALL)
        print(Fore.MAGENTA + f"{adversario.nombre} tiene {adversario.pedazos_barcos_restantes} pedazos de barcos restantes.\n" + Style.RESET_ALL)
        return adversario.pedazos_barcos_restantes == 0

def main():
    tamaño = 10
    intentos_iniciales = 20
    cantidad_barcos = 4

    jugador1 = Jugador("Jugador 1", tamaño, intentos_iniciales, cantidad_barcos)
    jugador2 = Jugador("Jugador 2", tamaño, intentos_iniciales, cantidad_barcos)

    jugador1.colocar_barcos()
    jugador1.tablero.graficar(show_ships=True)

    input("Chequealo, si esta bien toca cualquier tecla: ")
    os.system("clear")

    jugador2.colocar_barcos()
    jugador2.tablero.graficar(show_ships=True)

    input("Chequealo, si esta bien toca cualquier tecla: ")
    os.system("clear")


    print(f"\n{Fore.MAGENTA}[!] ¡Momento de JUGAR!{Style.RESET_ALL}\n")

    while jugador1.intentos > 0 and jugador2.intentos > 0:
        if turno == 1:
            print(Fore.BLUE + "[!] Turno de Jugador 1" + Style.RESET_ALL)
            if jugador1.jugar_turno(jugador2):
                print(Fore.GREEN + "[+] ¡Jugador 1 gana!" + Style.RESET_ALL)
                break
            turno = 2
        else:
            print(Fore.BLUE + "[!] Turno de Jugador 2" + Style.RESET_ALL)
            if jugador2.jugar_turno(jugador1):
                print(Fore.GREEN + "[+] ¡Jugador 2 gana!" + Style.RESET_ALL)
                break
            turno = 1

    if jugador1.intentos == 0 and jugador2.intentos == 0:
        print(Fore.YELLOW + "¡Se han acabado los intentos! Empate." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
