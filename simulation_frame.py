import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from simulation import ShopSimulation  # Import klasy ShopSimulation z modułu simulation

class SimulationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#999999')  # Inicjalizacja ramki tkinter z tłem #333333
        self.pack(padx=10, pady=10)  # Pakowanie ramki z marginesem 10 pikseli
        self.create_widgets()  # Wywołanie metody do tworzenia widżetów

    def create_widgets(self):
        # Definicja schematu kolorów
        label_color = '#ffffff'  # Kolor etykiet
        entry_bg = '#555555'  # Kolor tła pól wprowadzania tekstu
        entry_fg = '#ffffff'  # Kolor tekstu w polach wprowadzania tekstu
        button_color = '#0066ff'  # Kolor przycisków
        button_fg = 'white'  # Kolor tekstu na przyciskach

        # Konfiguracja dla wszystkich etykiet
        label_options = {'bg': '#999999', 'fg': label_color, 'padx': 10, 'pady': 10}

        # Utworzenie zakładek (interfejs z zakładkami)
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # Zakładka z parametrami
        parameters_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(parameters_frame, text='Parametry')

        # Pole wprowadzenia dziennej ilosci osob? nie kminie tego Gaussa
        tk.Label(parameters_frame, text="Maksymalna ilość osób", **label_options).grid(row=0, column=0, sticky='w')
        self.mu_hours_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.mu_hours_entry.grid(row=0, column=1, pady=5)

        tk.Label(parameters_frame, text="Minimalna ilość osób", **label_options).grid(row=1, column=0, sticky='w')
        self.mu_hours_entry_min = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.mu_hours_entry_min.grid(row=1, column=1, pady=5)

        # Pole wprowadzania odchylenia standardowego dla godzinowych przyjść klientów
        tk.Label(parameters_frame, text="Odchylenie standardowe dla godzinowych przyjść klientów:", **label_options).grid(row=2, column=0, sticky='w')
        self.sigma_hours_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.sigma_hours_entry.grid(row=2, column=1, pady=5)

        # Pole wprowadzania odchylenia standardowego dla dziennych przyjść klientów
        tk.Label(parameters_frame, text="Odchylenie standardowe dla dziennych przyjść klientów:", **label_options).grid(row=3, column=0, sticky='w')
        self.daily_variation_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.daily_variation_entry.grid(row=3, column=1, pady=5)

        # Pole wprowadzania odchylenia standardowego w skali rocznej
        tk.Label(parameters_frame, text="Odchylenie standardowe w skali rocznej:", **label_options).grid(row=4, column=0, sticky='w')
        self.yearly_variation_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.yearly_variation_entry.grid(row=4, column=1, pady=5)

        # Przycisk Zatwierdź
        self.submit_button = tk.Button(parameters_frame, text="Zatwierdź", bg=button_color, fg=button_fg, borderwidth=0, command=self.submit)
        self.submit_button.grid(row=5, columnspan=2, pady=10)

        # Druga zakładka (Tygodniowe wyniki)
        self.weekly_results_frame = ttk.Frame(self.notebook, style='TFrame')  # Utworzenie ramki dla wyników tygodniowych
        self.notebook.add(self.weekly_results_frame, text='Wyniki Tygodniowe')  # Dodanie zakładki z tytułem "Wyniki Tygodniowe"
        self.weekly_results_text = tk.Text(self.weekly_results_frame, wrap='word')  # Utworzenie pola tekstowego do wyświetlania wyników
        self.weekly_results_text.pack(fill='both', expand=True)  # Pakowanie pola tekstowego z rozszerzeniem

    def submit(self):
        params = {
            'mu_hours': float(self.mu_hours_entry.get()),  # Pobranie średnich godzin
            'sigma_hours': float(self.sigma_hours_entry.get()),  # Pobranie odchylenia standardowego dla godzinowych przyjść klientów
            'daily_variation': float(self.daily_variation_entry.get())  # Pobranie odchylenia standardowego dla dziennych przyjść klientów
        }
        simulation = ShopSimulation(params)  # Utworzenie obiektu symulacji sklepu
        simulation.run()  # Uruchomienie symulacji

        # Przechowywanie wyników w drugiej zakładce
        self.display_results(simulation.yearsTimeResults)

    def display_results(self, yearsTimeResults):
        """
        # Wyświetlenie wyników w drugiej zakładce
        self.weekly_results_text.insert('end', "Liczba klientów wg dnia:\n")
        for day, count in zip(["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Niedz"], results['customer_count']):
            self.weekly_results_text.insert('end', f"{day}: {count}\n")
        self.weekly_results_text.insert('end', f"\nCałkowity dochód: ${results['revenue']:.2f}\n")
        self.weekly_results_text.insert('end', f"Koszty pracowników: ${results['employee_costs']:.2f}\n")
        self.weekly_results_text.insert('end', f"Zysk netto: ${results['net_earnings']:.2f}\n")
        """
        # Create a bar plot for customer count
        #days_of_week = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Niedz"]
        week_numbers = list(range(0, 56))
        customer_counts = [sum(result['customer_count']) for result in yearsTimeResults]
        #week_numbers = [str(i) for i in range(56)]

        #for result in yearsTimeResults:
        plt.plot(week_numbers, customer_counts)
        #plt.plot(week_numbers, sum(result['customer_count']))
        plt.xlabel('Numer tygodnia w roku')
        plt.ylabel('Liczba klientów w skali roku')
        plt.title('Liczba klientów dla kolejnych tygodni')
        plt.show()

