N: int = 10


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
        # Estado interno: matriz para los barcos (True si hay barco)
        self.matriz_barcos = [[False for _ in range(tamaño)] for _ in range(tamaño)]
        # Matriz para marcar los intentos (por ejemplo, "⬛", "🔲", "🔳")
        self.matriz_marcada = [["⬛" for _ in range(tamaño)] for _ in range(tamaño)]
    
    def colocar_barco(self, barco: Barco) -> bool:
        dx = 0
        dy = 0

        if barco.orientacion == "h":
            dx = 1
        elif barco.orientacion == "v":
            dy = 1
        else:
            print("Orientación inválida. Usa 'h' para horizontal o 'v' para vertical.")
            return False

        # Verificar que el barco no se salga del tablero
        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            if not (0 <= nx < self.tamaño and 0 <= ny < self.tamaño):
                print("El barco se sale del tablero.")
                return False
            
            if self.matriz_barcos[ny][nx]:
                print(f"Ya hay un barco en X: {nx}, Y: {ny}")
                return False

        # Colocar el barco
        for i in range(barco.longitud):
            nx = barco.x + i * dx
            ny = barco.y + i * dy
            self.matriz_barcos[ny][nx] = True

        return True

    def graficar(self, show_ships: bool = False) -> None:
        for i in range(self.tamaño):
            fila = []
            for j in range(self.tamaño):
                # Si la celda ya fue marcada (disparo), se respeta ese símbolo.
                if self.matriz_marcada[i][j] != "⬛":
                    fila.append(self.matriz_marcada[i][j])
                else:
                    # Si se desea ver los barcos y hay uno, se muestra el barco (por ejemplo, "🚢")
                    if show_ships and self.matriz_barcos[i][j]:
                        fila.append("🚢")
                    else:
                        fila.append("⬛")
            print(" ".join(fila))
    
    def recibir_disparo(self, x: int, y: int) -> (bool, str):

        if not (0 <= y < self.tamaño and 0 <= x < self.tamaño):
            return False, "Coordenadas fuera del rango."

        if self.matriz_marcada[y][x] != "⬛":
            return False, "¡Ya elegiste esa casilla!"

        if self.matriz_barcos[y][x]:
            self.matriz_marcada[y][x] = "🔲"
            return True, "¡Acertaste! Había un barco."
        else:
            self.matriz_marcada[y][x] = "🔳"
            return False, "¡Uops! No había un barco."

class Jugador:
    def __init__(self, nombre: str, tamaño_tablero: int, intentos: int, cantidad_barcos: int):
        self.nombre = nombre
        self.tablero = Tablero(tamaño_tablero)
        self.intentos = intentos
        self.cantidad_barcos = cantidad_barcos
        self.pedazos_barcos_restantes = 0
    
    def colocar_barcos(self):
        print(f"\n\n[!] {self.nombre}: Momento de poner tus barcos.")
        barcos_colocados = 0
        while barcos_colocados < self.cantidad_barcos:
            try:
                x = int(input(f"{self.nombre} - X inicial del barco: "))
                y = int(input(f"{self.nombre} - Y inicial del barco: "))
                orientacion = input(f"{self.nombre} - Orientación (h para horizontal, v para vertical): ").lower()
                longitud = int(input(f"{self.nombre} - Longitud del barco: "))

                self.pedazos_barcos_restantes += longitud

            except ValueError:
                print("Entrada inválida. Intenta de nuevo.")
                continue

            barco = Barco(x, y, orientacion, longitud)
            if self.tablero.colocar_barco(barco):
                barcos_colocados += 1
                print(f"[+] Barco colocado: {barco}")
            else:
                print("[-] No se pudo colocar el barco. Intenta de nuevo.")

    
    def jugar_turno(self, adversario: 'Jugador') -> bool:
        try:
            x = int(input(f"{self.nombre}, ingresa la coordenada en X para disparar: "))
            y = int(input(f"{self.nombre}, ingresa la coordenada en Y para disparar: "))
        except ValueError:
            print("Por favor ingresa valores numéricos válidos.")
            return False

        acierto, mensaje = adversario.tablero.recibir_disparo(x, y)
        print(mensaje)
        adversario.tablero.graficar()
        if acierto:
            adversario.pedazos_barcos_restantes -= 1

        self.intentos -= 1
        print(f"{self.nombre} tiene {self.intentos} intentos restantes.")
        print(f"{adversario.nombre} tiene {adversario.pedazos_barcos_restantes} pedazos de barcos restantes.\n")
        return adversario.pedazos_barcos_restantes == 0

def main():
    tamaño = 10
    intentos_iniciales = 20
    cantidad_barcos = 2

    # Crear jugadores
    jugador1 = Jugador("Jugador 1", tamaño, intentos_iniciales, cantidad_barcos)
    jugador2 = Jugador("Jugador 2", tamaño, intentos_iniciales, cantidad_barcos)

    # Cada jugador coloca sus barcos
    jugador1.colocar_barcos()
    jugador1.tablero.graficar(show_ships=True)
    jugador2.colocar_barcos()
    jugador2.tablero.graficar(show_ships=True)


    print("\n[!] ¡Momento de JUGAR!\n")
    turno = 1  # 1 para jugador1 y 2 para jugador2

    while jugador1.intentos > 0 and jugador2.intentos > 0:
        if turno == 1:
            print("[!] Turno de Jugador 1")
            if jugador1.jugar_turno(jugador2):
                print("[+] ¡Jugador 1 gana!")
                break
            turno = 2
        else:
            print("[!] Turno de Jugador 2")
            if jugador2.jugar_turno(jugador1):
                print("[+] ¡Jugador 2 gana!")
                break
            turno = 1

    if jugador1.intentos == 0 and jugador2.intentos == 0:
        print("¡Se han acabado los intentos! Empate.")

if __name__ == "__main__":
    main()
