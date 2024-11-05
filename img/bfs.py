import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq

# Tablero actualizado basado en la imagen proporcionada
# Usando -1 para representar los obstáculos en lugar de 0
tablero = [
    [5, 4, 5, 6, 7, 8, 9, 10,-1, 18, 19, 20],
    [4, 3, 4, 5,-1, 7, 8, 9, -1, 17, 18, 19],
    [3, 2, 3, 4,-1, 6, 7, 8, -1, 16, 17, 18],
    [2, 1, 2, 3,-1, 5, 6, 7, -1, 15, 16, 17],
    [1, 0, 1, 2, 3, 4, 5, 6, -1, 14, 15, 16],
    [2, 1, 2, 3, 4, 5, 6, 7, -1, 13, 14, 15],
    [3, 2, 3, 4, 5, 6, 7, 8, -1, 12, 13, 14],
    [4, -1, -1,-1, -1, -1, -1,9,10,11,12,13],
    [5, 4, 5, 6, 7, 8, 9, 10, 11,12, 13, 14]
]

inicio = (4, 1)  # Casilla verde en la imagen de la tarea
meta = (1, 11)   # Casilla azul en la imagen de la tarea

movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos permitidos

# Función para mostrar el tablero y el camino encontrado
def mostrar_tablero(tablero, camino, algoritmo):
    ventana = tk.Toplevel()
    ventana.title(f"Camino encontrado con {algoritmo}")

    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            color = "white"
            if tablero[i][j] == -1:
                color = "grey"  # Obstáculos
            elif (i, j) == inicio:
                color = "green"  # Estado inicial
            elif (i, j) == meta:
                color = "blue"  # Estado final
            elif (i, j) in camino:
                color = "yellow"  # Camino encontrado

            cell = tk.Label(ventana, text=str(tablero[i][j]), width=4, height=2, bg=color, relief="ridge")
            cell.grid(row=i, column=j)

    ventana.mainloop()

# Búsqueda ciega (BFS)
def bfs(tablero, inicio, meta):
    filas, columnas = len(tablero), len(tablero[0])
    visitado = set()
    cola = deque([(inicio, [inicio])])

    while cola:
        (actual, camino) = cola.popleft()
        if actual == meta:
            mostrar_tablero(tablero, camino, "Búsqueda Ciega (BFS)")
            return camino

        for mov in movimientos:
            siguiente = (actual[0] + mov[0], actual[1] + mov[1])
            if 0 <= siguiente[0] < filas and 0 <= siguiente[1] < columnas and tablero[siguiente[0]][siguiente[1]] != -1 and siguiente not in visitado:
                visitado.add(siguiente)
                cola.append((siguiente, camino + [siguiente]))
    
    messagebox.showinfo("Resultado", "No se encontró camino con BFS.")
    return None

# Búsqueda A*
def heuristica(posicion, meta):
    return abs(posicion[0] - meta[0]) + abs(posicion[1] - meta[1])

def a_estrella(tablero, inicio, meta):
    filas, columnas = len(tablero), len(tablero[0])
    visitado = set()
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0 + heuristica(inicio, meta), 0, inicio, [inicio]))

    while cola_prioridad:
        (f, g, actual, camino) = heapq.heappop(cola_prioridad)
        
        if actual == meta:
            mostrar_tablero(tablero, camino, "Búsqueda A*")
            return camino

        for mov in movimientos:
            siguiente = (actual[0] + mov[0], actual[1] + mov[1])
            if 0 <= siguiente[0] < filas and 0 <= siguiente[1] < columnas and tablero[siguiente[0]][siguiente[1]] != -1 and siguiente not in visitado:
                visitado.add(siguiente)
                nuevo_g = g + tablero[siguiente[0]][siguiente[1]]
                nuevo_f = nuevo_g + heuristica(siguiente, meta)
                heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, siguiente, camino + [siguiente]))
    
    messagebox.showinfo("Resultado", "No se encontró camino con A*.")
    return None

# Interfaz gráfica principal
def interfaz_grafica():
    root = tk.Tk()
    root.title("Búsquedas Ciega y A*")
    
    # Botón para BFS
    boton_bfs = tk.Button(root, text="Búsqueda Ciega (BFS)", command=lambda: bfs(tablero, inicio, meta), width=30, height=2)
    boton_bfs.pack(pady=10)

    # Botón para A*
    boton_a_estrella = tk.Button(root, text="Búsqueda A*", command=lambda: a_estrella(tablero, inicio, meta), width=30, height=2)
    boton_a_estrella.pack(pady=10)

    root.mainloop()

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    interfaz_grafica()
