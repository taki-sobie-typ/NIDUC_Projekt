import tkinter as tk
from tkinter import ttk
from simulation import ShopSimulation

class SimulationFrame(tk.Frame):
    def __init__(self, master=None):
        # Inicjalizacja głównej ramki aplikacji
        super().__init__(master, bg='#333333')
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        # Ustawienie kolorów i stylów dla elementów GUI
        label_color = '#ffffff'
        entry_bg = '#555555'
        entry_fg = '#ffffff'
        button_color = '#0066ff'
        button_fg = 'white'
        label_options = {'bg': '#333333', 'fg': label_color, 'padx': 10, 'pady': 10}

        # Tworzenie i konfiguracja zakładek
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # Zakładka z parametrami
        parameters_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(parameters_frame, text='Parametry')

        # Etykieta i pole tekstowe dla średniej ilości osób
        tk.Label(parameters_frame, text="Średnia ilość osób", **label_options).grid(row=0, column=0, sticky='w')
        self.mu_hours_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.mu_hours_entry.grid(row=0, column=1, pady=5)

        # Etykieta i pole tekstowe dla odchylenia standardowego godzinowego przyjścia klientów
        tk.Label(parameters_frame, text="Odchylenie standardowe dla godzinowych przyjść klientów:", **label_options).grid(row=1, column=0, sticky='w')
        self.sigma_hours_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.sigma_hours_entry.grid(row=1, column=1, pady=5)

        # Lista wyboru dni tygodnia
        tk.Label(parameters_frame, text="Dni tygodnia:", **label_options).grid(row=2, column=0, sticky='w')
        self.weekday_select = tk.Listbox(parameters_frame, selectmode='multiple', height=7)
        for day in ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Niedz"]:
            self.weekday_select.insert(tk.END, day)
        self.weekday_select.grid(row=2, column=1, pady=5)

        # Etykieta i pole tekstowe dla ilości tygodni
        tk.Label(parameters_frame, text="Ilość tygodni:", **label_options).grid(row=3, column=0, sticky='w')
        self.weeks_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.weeks_entry.grid(row=3, column=1, pady=5)

        # Etykieta i pole tekstowe dla odchylenia standardowego liczby klientów w tygodniu
        tk.Label(parameters_frame, text="Odchylenie standardowe dla liczby klientów w tygodniu:", **label_options).grid(row=4, column=0, sticky='w')
        self.sigma_weekly_entry = tk.Entry(parameters_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0)
        self.sigma_weekly_entry.grid(row=4, column=1, pady=5)

        # Przycisk zatwierdzający dane i uruchamiający symulację
        self.submit_button = tk.Button(parameters_frame, text="Zatwierdź", bg=button_color, fg=button_fg, borderwidth=0, command=self.submit)
        self.submit_button.grid(row=5, columnspan=2, pady=10)

        # Zakładka z wynikami
        results_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(results_frame, text='Wyniki Tygodniowe')

        # Wybór zakładki z wynikami i pole tekstowe do ich wyświetlania
        self.result_option = ttk.Combobox(results_frame, width=50)
        self.result_option.pack(pady=10)
        self.result_option.bind('<<ComboboxSelected>>', self.update_results_display)
        self.results_text = tk.Text(results_frame, wrap='word', bg='#333333', fg='#ffffff')
        self.results_text.pack(fill='both', expand=True)

    def submit(self):
        # Pobranie danych z formularza i uruchomienie symulacji
        params = {
            'mu_hours': float(self.mu_hours_entry.get()),
            'sigma_hours': float(self.sigma_hours_entry.get()),
            'selected_days': [self.weekday_select.get(idx) for idx in self.weekday_select.curselection()],
            'weeks': int(self.weeks_entry.get()),
            'sigma_weekly': float(self.sigma_weekly_entry.get())
        }
        simulation = ShopSimulation(params)
        simulation.run()
        self.display_results(simulation.results, params['weeks'])

    def display_results(self, results, weeks):
        # Wyświetlanie wyników symulacji
        self.results = results
        self.weeks = weeks
        options = ['Summary'] + [f'Week {i+1}' for i in range(weeks)]
        self.result_option['values'] = options
        self.result_option.current(0)  # Ustawienie domyślnego wyboru na podsumowanie

    def update_results_display(self, event=None):
        # Aktualizacja wyświetlania wyników na podstawie wyboru użytkownika
        selected = self.result_option.get()
        self.results_text.delete('1.0', 'end')
        if selected == 'Summary':
            self.results_text.insert('end', f"Wyniki z {self.weeks} tygodni:\n\n")
            for day, counts in self.results['customer_count'].items():
                self.results_text.insert('end', f"{day}: {sum(counts)}\n")
            self.results_text.insert('end', f"\nCałkowity dochód: ${self.results['revenue']:.2f}\n")
            self.results_text.insert('end', f"Koszty pracowników: ${self.results['employee_costs']:.2f}\n")
            self.results_text.insert('end', f"Zysk netto: ${self.results['net_earnings']:.2f}\n")
        elif selected.startswith('Week'):
            week_num = int(selected.split()[1]) - 1
            self.results_text.insert('end', f"Wyniki z tygodnia {week_num + 1}:\n")
            for day, counts in self.results['customer_count'].items():
                if week_num < len(counts):
                    self.results_text.insert('end', f"{day}: {counts[week_num]}\n")
            #Logika do wyswietlania informacji z danego tygodnia
