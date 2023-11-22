import tkinter as tk


# Funzione chiamata quando l'utente fa clic su un canvas
def colpo_su_griglia(event, grid):
    cell_width = 30
    x, y = event.x, event.y
    row, col = y // cell_width, x // cell_width

    # Esegui la logica del colpo sulla casella (row, col)

    if grid[row][col] == 0:
        print("Colpo a vuoto!")
        grid[row][col] = 3  # Segna come nave mancata
    elif grid[row][col] == 1:
        print("Nave colpita!")
        grid[row][col] = 2  # Rimane come nave colpita

    # Aggiorna la griglia grafica dopo il colpo
    update_grid(player_canvas, PlayerGrid)
    update_grid(ai_canvas, AiGrid)
    checkGameOver(AiGrid)
    checkGameOver(PlayerGrid)


# Funzione per aggiornare la griglia grafica
def update_grid(canvas, grid):
    canvas.delete("all")
    rows = len(grid)
    cols = len(grid[0])
    cell_width = 30

    for i in range(rows):
        for j in range(cols):
            x1, y1 = j * cell_width, i * cell_width
            x2, y2 = x1 + cell_width, y1 + cell_width
            cell_value = grid[i][j]

            if cell_value == 0 or cell_value == 1:
                color = "white"  # Casella vuota o con nave
            elif cell_value == 2:
                color = "red"  # Nave colpita
            elif cell_value == 3:
                color = "gray"  # Nave mancata

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")


def checkGameOver(griglia):
    for ele in griglia:
        for num in ele:
            if num == 1:
                return False
    print("GAME OVER")
    return True


def colpisci(x, y, griglia):
    if 0 <= x <= 9 and 0 <= y <= 9:
        if griglia[x][y] == 1:
            print("nave colpita!")
            griglia[x][y] = 2
        elif griglia[x][y] == 0:
            print("colpo a vuoto")

        elif griglia[x][y] == 2:
            print("nave gia' colpita in precendenza, riprova")
            x = input("x")
            y = input("y")
            colpisci(int(x), int(y), griglia)
        elif griglia[x][y] == 3:
            print("nave gia' mancata in precendenza, riprova")
            x = input("x")
            y = input("y")
            colpisci(int(x), int(y), griglia)

    else:
        print("coordinate invalide come te")
        return False


def ruota_nave_90gradi(forma):
    # Ruota la nave di 90 gradi in senso orario
    nuova_forma = [(y, -x) for (x, y) in forma]
    return nuova_forma


def inserisci_nave(grid, riga, colonna, forma):  # una forma è definita come forma_nave = [(0, 0), (0, 1), (0, 2)]
    altezza = len(grid)
    larghezza = len(grid[0])

    # Verifica se la nave esce dalla griglia
    for coord in forma:
        nuova_riga = riga + coord[0]
        nuova_colonna = colonna + coord[1]

        if (nuova_riga < 0 or nuova_riga >= altezza or
                nuova_colonna < 0 or nuova_colonna >= larghezza):
            print("nave fuori griglia")
            return False  # La nave esce dalla griglia

    # Se la nave non esce dalla griglia, inserisci la nave
    for coord in forma:
        nuova_riga = riga + coord[0]
        nuova_colonna = colonna + coord[1]
        grid[nuova_riga][nuova_colonna] = 1  # Segno della nave (1, ad esempio)
    print("nave inserita con successo")
    return True


if __name__ == '__main__':
    AiGrid = [[0 for _ in range(10)] for _ in range(10)]
    PlayerGrid = [[0 for _ in range(10)] for _ in range(10)]
    naviAi = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2), (3, 2)],
    ]
    naviPlayer = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2), (3, 2)],
    ]

    inserisci_nave(AiGrid, 5, 2, ruota_nave_90gradi(naviPlayer[2]))
    inserisci_nave(PlayerGrid, 0, 0, (naviPlayer[3]))

    # Creazione della finestra principale
    root = tk.Tk()
    root.title("Battaglia Navale")

    # Creazione di due canvas per visualizzare le griglie
    ai_canvas = tk.Canvas(root, width=300, height=300, borderwidth=2, relief="ridge")
    player_canvas = tk.Canvas(root, width=300, height=300, borderwidth=2, relief="ridge")

    ai_canvas.grid(row=0, column=0, padx=10, pady=10)
    player_canvas.grid(row=0, column=1, padx=10, pady=10)

    # Aggiornamento delle griglie grafiche
    update_grid(ai_canvas, AiGrid)
    update_grid(player_canvas, PlayerGrid)

    # Associa la funzione del colpo al clic del mouse sul canvas del giocatore
    player_canvas.bind("<Button-1>", lambda event: colpo_su_griglia(event, PlayerGrid))
    ai_canvas.bind("<Button-1>", lambda event: colpo_su_griglia(event, AiGrid))

    root.mainloop()