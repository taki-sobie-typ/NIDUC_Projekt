import tkinter as tk
from tkinter import ttk
from simulation_frame import SimulationFrame

def main():
    root = tk.Tk()
    root.title("Symulacja Sklepu")  # Ustawienie tytułu głównego okna aplikacji

    # Konfiguracja stylu dla całej aplikacji
    style = ttk.Style(root)
    # Ustawienie koloru tła dla widżetu Notebook, aby pasował do ciemniejszego motywu
    style.configure('TNotebook', background='#ffffff', foreground='#ffffff')
    style.configure('TFrame', background='#333333')
    style.configure('TButton', background='#0066ff', foreground='white', font=('Helvetica', 10))
    style.map('TButton', background=[('active', '#0055cc')])

    # Konfiguracja koloru tekstu dla wszystkich etykiet w ramkach, aby zapewnić spójność
    style.configure('TLabel', background='#ffffff', foreground='#ffffff')

    # Inicjalizacja ramki aplikacji
    app = SimulationFrame(master=root)
    # Uruchomienie głównej pętli Tkinter
    app.mainloop()

if __name__ == "__main__":
    main()
