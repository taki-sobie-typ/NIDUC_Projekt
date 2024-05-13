import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from simulation import ShopSimulation  # Import klasy ShopSimulation z modułu simulation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#fff')  # Inicjalizacja ramki tkinter z tłem #333333
        self.pack(padx=10, pady=10)  # Pakowanie ramki z marginesem 10 pikseli
        self.create_widgets()  # Wywołanie metody do tworzenia widżetów

    def create_widgets(self):
        # Definicja schematu kolorów
        label_color = '#000'  # Kolor etykiet
        entry_bg = '#bbb'  # Kolor tła pól wprowadzania tekstu
        entry_fg = '#000'  # Kolor tekstu w polach wprowadzania tekstu
        button_color = '#0066ff'  # Kolor przycisków
        button_fg = 'white'  # Kolor tekstu na przyciskach

        # Konfiguracja dla wszystkich etykiet
        label_options = {'bg': '#fff', 'fg': label_color, 'padx': 10, 'pady': 10, 'font': ('Arial', 13)}


        # Utworzenie zakładek (interfejs z zakładkami)
        self.notebook = ttk.Notebook(self, style='TNotebook', width=1000, height=1000)
        self.notebook.pack(fill='both', expand=True)

        # Zakładka z parametrami
        parameters_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(parameters_frame, text='Parametry')

        # Pole wprowadzenia dziennej ilosci osob? nie kminie tego Gaussa
        tk.Label(parameters_frame, text="Maksymalna ilość osób", **label_options).grid(row=0, column=0, sticky='w')
        self.mu_hours_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.mu_hours_entry.grid(row=0, column=1, pady=5)

        tk.Label(parameters_frame, text="Minimalna ilość osób", **label_options).grid(row=1, column=0, sticky='w')
        self.mu_hours_entry_min = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.mu_hours_entry_min.grid(row=1, column=1, pady=5)

        # Pole wprowadzania odchylenia standardowego dla godzinowych przyjść klientów
        tk.Label(parameters_frame, text="Odchylenie standardowe dla godzinowych przyjść klientów:", **label_options).grid(row=2, column=0, sticky='w')
        self.sigma_hours_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.sigma_hours_entry.grid(row=2, column=1, pady=5)

        # Pole wprowadzania odchylenia standardowego dla dziennych przyjść klientów
        tk.Label(parameters_frame, text="Odchylenie standardowe dla dziennych przyjść klientów:", **label_options).grid(row=3, column=0, sticky='w')
        self.daily_variation_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.daily_variation_entry.grid(row=3, column=1, pady=5)

        # Pole wprowadzania odchylenia standardowego w skali rocznej
        tk.Label(parameters_frame, text="Odchylenie standardowe w skali rocznej:", **label_options).grid(row=4, column=0, sticky='w')
        self.yearly_variation_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.yearly_variation_entry.grid(row=4, column=1, pady=5)

        # Przycisk Zatwierdź
        self.submit_button = tk.Button(parameters_frame, text="Zatwierdź", bg=button_color, fg=button_fg, borderwidth=0, command=self.submit, font=('Arial', 13))
        self.submit_button.grid(row=5, columnspan=2, pady=10)


        # Druga zakładka (Tygodniowe wyniki)
        """"""
        self.weekly_results_frame = ttk.Frame(self.notebook, style='TFrame')  # Utworzenie ramki dla wyników tygodniowych
        self.notebook.add(self.weekly_results_frame, text='Wyniki Roczne')  # Dodanie zakładki z tytułem "Wyniki Tygodniowe"
        #self.weekly_results_text = tk.Text(self.weekly_results_frame, wrap='word')  # Utworzenie pola tekstowego do wyświetlania wyników
        #self.weekly_results_text.pack(fill='both', expand=True)  # Pakowanie pola tekstowego z rozszerzeniem

    def submit(self):
        params = {
            'mu_hours': float(self.mu_hours_entry.get()),  # Pobranie max godzin
            'mu_min_hours': float(self.mu_hours_entry_min.get()), # Pobranie min godzin
            'sigma_hours': float(self.sigma_hours_entry.get()),  # Pobranie odchylenia standardowego dla godzinowych przyjść klientów
            'daily_variation': float(self.daily_variation_entry.get()),  # Pobranie odchylenia standardowego dla dziennych przyjść klientów
            'yearly_variation': float(self.yearly_variation_entry.get()) # Pobranie odchulenia standardowego w skali rocznej
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

        revenue_total = [(result['revenue']) for result in yearsTimeResults]
        employee_cost_total = [(result['employee_costs']) for result in yearsTimeResults]
        net_earnings_total = [(result['net_earnings']) for result in yearsTimeResults]

        # Subplot
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 9))

        # Graf dla liczby klientow
        ax1.plot(week_numbers, customer_counts, label='Liczba klientów')
        ax1.set_xlabel('Numer tygodnia w roku')
        ax1.set_ylabel('Liczba klientów w skali roku')
        ax1.set_title('Liczba klientów dla kolejnych tygodni')
        ax1.legend()

        # Graf dla dochodu całkowitego
        ax2.plot(week_numbers, revenue_total, label='Calkowity dochód', color='orange')
        ax2.set_xlabel('Numer tygodnia w roku')
        ax2.set_ylabel('Całkowity dochód')
        ax2.legend()

        # Graf dla dochodu całkowitego
        ax3.plot(week_numbers, employee_cost_total, label='Koszt pracowników', color='green')
        ax3.set_xlabel('Numer tygodnia w roku')
        ax3.set_ylabel('Koszt pracowników')
        ax3.legend()

        # Graf dla dochodu całkowitego
        ax4.plot(week_numbers, net_earnings_total, label='Dochód netto', color='red')
        ax4.set_xlabel('Numer tygodnia w roku')
        ax4.set_ylabel('Dochód netto')
        ax4.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self.weekly_results_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)


        # Show plot
        # plt.tight_layout()
        # plt.show()

