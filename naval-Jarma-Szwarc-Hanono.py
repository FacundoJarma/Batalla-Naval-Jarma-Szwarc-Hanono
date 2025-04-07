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
        # Matriz para los barcos (True si hay barco)
        self.matriz_barcos = [[False for _ in range(tamaño)] for _ in range(tamaño)]
        # Matriz para marcar los disparos: "⬛" celda sin disparo, "🔲" impacto, "🔳" fallo
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

        # Verificar que el barco no se salga del tablero y no colisione con otro barco
        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            if not (0 <= nx < self.tamaño and 0 <= ny < self.tamaño):
                print(Fore.RED + "El barco se sale del tablero.")
                return False
            
            if self.matriz_barcos[ny][nx]:
                print(Fore.RED + f"Ya hay un barco en X: {nx}, Y: {ny}")
                return False

        # Colocar el barco en la matriz
        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            self.matriz_barcos[ny][nx] = True

        return True

    def graficar(self, show_ships: bool = False) -> None:
        # Definir colores para cada símbolo
        # ⬛: celda sin disparo, se muestra en gris
        # 🚢: barco, se muestra en azul
        # 🔲: impacto, se muestra en rojo
        # 🔳: disparo fallido, se muestra en amarillo
        for i in range(self.tamaño):
            fila = []
            for j in range(self.tamaño):
                celda = self.matriz_marcada[i][j]
                if celda != "⬛":
                    # Si ya fue disparada, usamos el color según el resultado.
                    if celda == "🔲":
                        fila.append(Fore.RED + celda + Style.RESET_ALL)
                    elif celda == "🔳":
                        fila.append(Fore.YELLOW + celda + Style.RESET_ALL)
                    else:
                        fila.append(celda)
                else:
                    # Si se desea ver los barcos (modo depuración) y hay barco, se muestra en azul.
                    if show_ships and self.matriz_barcos[i][j]:
                        fila.append(Fore.CYAN + "🚢" + Style.RESET_ALL)
                    else:
                        fila.append(Fore.WHITE + celda + Style.RESET_ALL)
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
            try:
                x = int(input(f"{self.nombre} - X inicial del barco: "))
                y = int(input(f"{self.nombre} - Y inicial del barco: "))
                orientacion = input(f"{self.nombre} - Orientación (h para horizontal, v para vertical): ").lower()
                longitud = int(input(f"{self.nombre} - Longitud del barco: "))
                self.pedazos_barcos_restantes += longitud
            except ValueError:
                print(Fore.RED + "Entrada inválida. Intenta de nuevo." + Style.RESET_ALL)
                continue

            barco = Barco(x, y, orientacion, longitud)
            if self.tablero.colocar_barco(barco):
                barcos_colocados += 1
                print(Fore.GREEN + f"[+] Barco colocado: {barco}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "[-] No se pudo colocar el barco. Intenta de nuevo." + Style.RESET_ALL)

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

    # Crear jugadores
    jugador1 = Jugador("Jugador 1", tamaño, intentos_iniciales, cantidad_barcos)
    jugador2 = Jugador("Jugador 2", tamaño, intentos_iniciales, cantidad_barcos)

    # Cada jugador coloca sus barcos
    jugador1.colocar_barcos()
    jugador1.tablero.graficar(show_ships=True)
    jugador2.colocar_barcos()
    jugador2.tablero.graficar(show_ships=True)

    print(f"\n{Fore.MAGENTA}[!] ¡Momento de JUGAR!{Style.RESET_ALL}\n")
    turno = 1  # 1 para jugador1 y 2 para jugador2

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
