import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from simulation import ShopSimulation  # Import klasy ShopSimulation z modułu simulation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SimulationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#fff')  # Inicjalizacja ramki tkinter z tłem #333333
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.pack(padx=10, pady=10)  # Pakowanie ramki z marginesem 10 pikseli
        self.create_widgets()  # Wywołanie metody do tworzenia widżetów

    def create_widgets(self):
        # Definicja schematu kolorów
        label_color = '#000'  # Kolor etykiet
        label_bg = '#fff'  # Kolor tła etykiet
        entry_bg = '#bbb'  # Kolor tła pól wprowadzania tekstu
        entry_fg = '#000'  # Kolor tekstu w polach wprowadzania tekstu
        button_color = '#00bbff'  # Kolor przycisków
        button_fg = 'black'  # Kolor tekstu na przyciskach

        # Konfiguracja dla wszystkich etykiet
        label_options = {'bg': label_bg, 'fg': label_color, 'padx': 10, 'pady': 10, 'font': ('Arial', 13)}

        # Utworzenie zakładek (interfejs z zakładkami)
        self.notebook = ttk.Notebook(self, style='TNotebook', width=1000, height=800)
        self.notebook.pack(fill='both', expand=True)

        # Zakładka z parametrami
        parameters_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(parameters_frame, text='Parametry')

        # Create a canvas and scrollbar for the parameters frame
        self.canvas = tk.Canvas(parameters_frame, bg='#fff')
        self.scrollbar = tk.Scrollbar(parameters_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Inner frame for parameters
        self.parameters_inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.parameters_inner_frame, anchor='nw')

        # Configure the inner frame to resize properly
        self.parameters_inner_frame.bind('<Configure>',
                                         lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Centering the parameters_inner_frame within the canvas
        self.parameters_inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.create_window((self.canvas.winfo_width() // 2, 0), window=self.parameters_inner_frame, anchor='n')

        # Form fields and labels
        tk.Label(self.parameters_inner_frame, text="Maksymalna ilość osób", **label_options).grid(row=0, column=0,
                                                                                                  sticky='w')
        self.mu_hours_entry = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                       insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.mu_hours_entry.grid(row=0, column=1, pady=5)

        #RESZTA UI
        tk.Label(self.parameters_inner_frame, text="Minimalna ilość osób", **label_options).grid(row=1, column=0,
                                                                                                 sticky='w')
        self.mu_hours_entry_min = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                           insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.mu_hours_entry_min.grid(row=1, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Liczba kas standardowych", **label_options).grid(row=2, column=0,
                                                                                                     sticky='w')
        self.checkouts_number = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                         insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.checkouts_number.grid(row=2, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Liczba kas samoobslugowych", **label_options).grid(row=3, column=0,
                                                                                                       sticky='w')
        self.selfcheckouts_number = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                             insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.selfcheckouts_number.grid(row=3, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Rozmiar sklepu", **label_options).grid(row=4, column=0, sticky='w')
        self.shop_size = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                  insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.shop_size.grid(row=4, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Odchylenie standardowe dla godzinowych przyjść klientów:",
                 **label_options).grid(row=5, column=0, sticky='w')
        self.sigma_hours_entry = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                          insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.sigma_hours_entry.grid(row=5, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Odchylenie standardowe dla dziennych przyjść klientów:",
                 **label_options).grid(row=6, column=0, sticky='w')
        self.daily_variation_entry = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                              insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.daily_variation_entry.grid(row=6, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Odchylenie standardowe w skali rocznej:", **label_options).grid(
            row=7, column=0, sticky='w')
        self.yearly_variation_entry = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                               insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.yearly_variation_entry.grid(row=7, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Godzina otwarcia (24h format):", **label_options).grid(row=8, column=0, sticky='w')
        self.open_time = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.open_time.grid(row=8, column=1, pady=5)

        tk.Label(self.parameters_inner_frame, text="Godzina zamknięcia (24h format):", **label_options).grid(row=9, column=0, sticky='w') 
        self.close_time = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.close_time.grid(row=9, column=1, pady=5)

        

        tk.Label(self.parameters_inner_frame, text="Markup (%)", **label_options).grid(row= 10, column=0, sticky='w')
        self.markup_entry = tk.Entry(self.parameters_inner_frame, width=20, bg=entry_bg, fg=entry_fg,
                                     insertbackground=entry_fg, borderwidth=0, font=('Arial', 13))
        self.markup_entry.grid(row=10, column=1, pady=5)

        self.submit_button = tk.Button(self.parameters_inner_frame, text="Zatwierdź", bg=button_color, fg=button_fg,
                                       borderwidth=0, command=self.submit, font=('Arial', 13))
        self.submit_button.grid(row=11, columnspan=2, padx=10, pady=10, sticky='ew')

        tk.Label(self.parameters_inner_frame, text="Predefiniowane modele sklepów", **label_options).grid(row=12,
                                                                                                          column=0,
                                                                                                          sticky='w')

        self.prep1_button = tk.Button(self.parameters_inner_frame, text="Duży Sklep", bg='#ddd', fg=button_fg,
                                      borderwidth=0, command=lambda: self.update_entries(1), font=('Arial', 13))
        self.prep1_button.grid(row=13, column=0, padx=10, pady=10, sticky='ew')

        self.prep2_button = tk.Button(self.parameters_inner_frame, text="Średni Sklep", bg='#ddd', fg=button_fg,
                                      borderwidth=0, command=lambda: self.update_entries(2), font=('Arial', 13))
        self.prep2_button.grid(row=14, column=0, padx=10, pady=10, sticky='ew')

        self.prep3_button = tk.Button(self.parameters_inner_frame, text="Mały Sklep", bg='#ddd', fg=button_fg,
                                      borderwidth=0, command=lambda: self.update_entries(3), font=('Arial', 13))
        self.prep3_button.grid(row=15, column=0, padx=10, pady=10, sticky='ew')

        self.prep4_button = tk.Button(self.parameters_inner_frame, text="Mini Sklep", bg='#ddd', fg=button_fg,
                                      borderwidth=0, command=lambda: self.update_entries(4), font=('Arial', 13))
        self.prep4_button.grid(row=16, column=0, padx=10, pady=10, sticky='ew')

        # Druga zakładka (Wyniki Roczne)
        """"""
        self.weekly_results_frame = ttk.Frame(self.notebook,
                                              style='TFrame')  # Utworzenie ramki dla wyników tygodniowych
        self.notebook.add(self.weekly_results_frame, text='Wyniki Roczne')  # Dodanie zakładki z tytułem "Wyniki Roczne"
        # Create a canvas and scrollbar for the weekly results frame
        self.canvas_results = tk.Canvas(self.weekly_results_frame, bg='#fff')
        self.scrollbar_results = tk.Scrollbar(self.weekly_results_frame, orient='vertical',
                                              command=self.canvas_results.yview)
        self.canvas_results.configure(yscrollcommand=self.scrollbar_results.set)

        self.scrollbar_results.pack(side='right', fill='y')
        self.canvas_results.pack(side='left', fill='both', expand=True)

        # Inner frame for weekly results
        self.results_inner_frame = ttk.Frame(self.canvas_results)
        self.canvas_results.create_window((0, 0), window=self.results_inner_frame, anchor='nw')

        # Configure the inner frame to resize properly
        self.results_inner_frame.bind('<Configure>', lambda e: self.canvas_results.configure(
            scrollregion=self.canvas_results.bbox('all')))
        #self.weekly_results_text = tk.Text(self.weekly_results_frame, wrap='word')  # Utworzenie pola tekstowego do wyświetlania wyników
        #self.weekly_results_text.pack(fill='both', expand=True)  # Pakowanie pola tekstowego z rozszerzeniem

        #Trzecia zakładka (Wyniki roczne podsumowanie numeryczne)

        self.summary_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.summary_frame, text='Podsumowanie Roczne Liczby')

        #Drop menu do 3 zakładki

        self.week_label = tk.Label(self.summary_frame, text="Wybierz tydzień:", **label_options)
        self.week_label.pack(pady=5)

        self.week_combobox = ttk.Combobox(self.summary_frame, values=[f"Week {i}" for i in range(1, 57)] + ["Total"],
                                          font=('Arial', 12))
        self.week_combobox.current(56)
        self.week_combobox.pack(pady=5)
        self.week_combobox.bind("<<ComboboxSelected>>", self.update_summary_combobox)

        #Trzecia zakładka wygląd tabeli

        self.summary_table = ttk.Treeview(self.summary_frame, columns=("Metric", "Value"), show='headings', height=8)
        self.summary_table.heading("Metric", text="Metric")
        self.summary_table.heading("Value", text="Value")
        self.summary_table.column("Metric", anchor='center', width=150)
        self.summary_table.column("Value", anchor='center', width=200)

        #Wiekszy font i separacja tabeli
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'), padding=(10, 5))
        style.configure("Treeview", font=('Arial', 14), rowheight=75)

        self.summary_table.pack(fill='both', expand=True, pady=10, padx=10)

    def submit(self):
        params = {
            'mu_hours': float(self.mu_hours_entry.get()),  # Pobranie max liczby osób
            'mu_min_hours': float(self.mu_hours_entry_min.get()),  # Pobranie min liczby osób
            'checkouts_number': float(self.checkouts_number.get()),  #Pobranie liczby kas standardowych
            'selfcheckouts_number': float(self.selfcheckouts_number.get()),  # Pobranie liczby kas samoobslugowych
            # Pobranie wartosci dla rozmiaru sklepu
            'shop_size': float(self.shop_size.get()),
            'sigma_hours': float(self.sigma_hours_entry.get()),
            # Pobranie odchylenia standardowego dla godzinowych przyjść klientów
            'daily_variation': float(self.daily_variation_entry.get()),
            # Pobranie odchylenia standardowego dla dziennych przyjść klientów
            'yearly_variation': float(self.yearly_variation_entry.get()),
            # Pobranie odchulenia standardowego w skali rocznej
            'open_time': int(self.open_time.get()),  # Pobranie godziny otwarcia sklepu
            'close_time': int(self.close_time.get()),  # Pobranie godziny zamknięcia sklepu
            'markup_percentage': float(self.markup_entry.get())  # Pobranie wartości markup
        }
        simulation = ShopSimulation(params)  # Utworzenie obiektu symulacji sklepu
        simulation.run()  # Uruchomienie symulacji

        # Przechowywanie wyników w drugiej zakładce
        self.display_results(simulation.yearsTimeResults)

        #Przechowywanie wyników w trzeciej zakładce
        self.display_summary(simulation.yearsTimeResults)

    def display_summary(self, yearsTimeResults):
        self.yearsTimeResults = yearsTimeResults
        self.week_combobox.set("Total")
        self.update_summary(0)

    def update_summary(self, week):
        week = int(week)
        for row in self.summary_table.get_children():
            self.summary_table.delete(row)

        if week == 0:
            total_customers = sum(sum(result['customer_count']) for result in self.yearsTimeResults)
            total_revenue = sum(result['revenue'] for result in self.yearsTimeResults)
            total_employee_costs = sum(result['employee_costs'] for result in self.yearsTimeResults)
            total_net_earnings = sum(result['net_earnings'] for result in self.yearsTimeResults)
            total_product_costs = sum(result['product_costs'] for result in self.yearsTimeResults)  
            total_days = len(self.yearsTimeResults) * 7  # 56 tygodni x 7 dni = 392 dni
            total_standard_queue_customers = sum(
                sum(waiting_time[0] for waiting_time in result['waiting_time']) for result in
                self.yearsTimeResults) / 12
            total_self_queue_customers = sum(
                sum(waiting_time[1] for waiting_time in result['waiting_time']) for result in
                self.yearsTimeResults) / 12

            avg_waiting_time_standard = total_standard_queue_customers / total_days
            avg_waiting_time_self = total_self_queue_customers / total_days
            satisfaction_levels = {
                'very_satisfied': sum(
                    result['customer_satisfaction']['very_satisfied'] for result in self.yearsTimeResults),
                'satisfied': sum(result['customer_satisfaction']['satisfied'] for result in self.yearsTimeResults),
                'unsatisfied': sum(result['customer_satisfaction']['unsatisfied'] for result in self.yearsTimeResults)
            }

            summary_data = [
                ("Liczba klientów", total_customers),
                ("Całkowity dochód", f"${total_revenue:.2f}"),
                ("Koszt produktów", f"${total_product_costs:.2f}"), 
                ("Koszty pracowników", f"${total_employee_costs:.2f}"),
                ("Zysk netto", f"${total_net_earnings:.2f}"),  
                ("Średni czas oczekiwania (standardowe kasy)", f"{avg_waiting_time_standard:.2f} min"),
                ("Średni czas oczekiwania (kasy samoobsługowe)", f"{avg_waiting_time_self:.2f} min"),
                ("Ilość osób bardzo zadowolonych", satisfaction_levels['very_satisfied']),
                ("Ilość osób zadowolonych", satisfaction_levels['satisfied']),
                ("Ilość osób niezadowolonych", satisfaction_levels['unsatisfied'])
            ]
        else:
            week_result = self.yearsTimeResults[week - 1]
            total_customers = sum(week_result['customer_count'])
            total_revenue = week_result['revenue']
            total_employee_costs = week_result['employee_costs']
            total_net_earnings = week_result['net_earnings']
            total_product_costs = week_result['product_costs'] 
            total_standard_queue_customers = sum(waiting_time[0] for waiting_time in week_result['waiting_time']) / 12
            total_self_queue_customers = sum(waiting_time[1] for waiting_time in week_result['waiting_time']) / 12

            avg_waiting_time_standard = total_standard_queue_customers / 7  # 7 dni w tygodniu
            avg_waiting_time_self = total_self_queue_customers / 7  # 7 dni w tygodniu

            satisfaction_levels = week_result['customer_satisfaction']

            summary_data = [
                ("Liczba klientów", total_customers),
                ("Całkowity dochód", f"${total_revenue:.2f}"),
                ("Koszt produktów", f"${total_product_costs:.2f}"), 
                ("Koszty pracowników", f"${total_employee_costs:.2f}"),
                ("Zysk netto", f"${total_net_earnings:.2f}"),
                ("Średni czas oczekiwania (standardowe kasy)", f"{avg_waiting_time_standard:.2f} min"),
                ("Średni czas oczekiwania (kasy samoobsługowe)", f"{avg_waiting_time_self:.2f} min"),
                ("Ilość osób bardzo zadowolonych", satisfaction_levels['very_satisfied']),
                ("Ilość osób zadowolonych", satisfaction_levels['satisfied']),
                ("Ilość osób niezadowolonych", satisfaction_levels['unsatisfied'])
            ]

        for metric, value in summary_data:
            self.summary_table.insert("", "end", values=(metric, value))

    #Naprawia problem podczas kolejnego wyświetlenia total
    def update_summary_combobox(self, event):
        selection = self.week_combobox.get()
        if selection == "Total":
            self.update_summary(0)  #jezeli wyswietlamy total to przekazujemy 0
        elif selection.startswith("Week"):
            week = int(selection.split()[1])
            self.update_summary(week)
        else:
            pass

    def display_results(self, yearsTimeResults):
        week_numbers = list(range(0, 56))
        customer_counts = [sum(result['customer_count']) for result in yearsTimeResults]

        # Informacje do wykresów
        revenue_total = [(result['revenue']) for result in yearsTimeResults]
        employee_cost_total = [(result['employee_costs']) for result in yearsTimeResults]
        net_earnings_total = [(result['net_earnings']) for result in yearsTimeResults]

        # Wyłuskiwanie infomracji o stanie zadowolenia klientow
        very_satisfied_total = [result['customer_satisfaction']['very_satisfied'] for result in yearsTimeResults]
        satisfied_total = [result['customer_satisfaction']['satisfied'] for result in yearsTimeResults]
        unsatisfied_total = [result['customer_satisfaction']['unsatisfied'] for result in yearsTimeResults]

        # Subplot
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(10, 10))

        # Wykres dla liczby klientow
        ax1.plot(week_numbers, customer_counts, label='Liczba klientów')
        #ax1.set_xlabel('Numer tygodnia w roku')
        ax1.set_ylabel('Liczba klientów w skali roku')
        ax1.set_title('Dla kolejnych tygodni w roku')
        ax1.legend()

        # Wykres dla dochodu całkowitego
        ax2.plot(week_numbers, revenue_total, label='Calkowity dochód', color='orange')
        #ax2.set_xlabel('Numer tygodnia w roku')
        ax2.set_ylabel('Całkowity dochód')
        ax2.legend()

        # Wykres dla dochodu całkowitego
        ax3.plot(week_numbers, employee_cost_total, label='Koszt pracowników', color='green')
        #ax3.set_xlabel('Numer tygodnia w roku')
        ax3.set_ylabel('Koszt pracowników')
        ax3.legend()

        # Wykres dla dochodu całkowitego
        ax4.plot(week_numbers, net_earnings_total, label='Dochód netto', color='red')
        ax4.set_xlabel('Numer tygodnia w roku')
        ax4.set_ylabel('Dochód netto')
        ax4.legend()

        # Wykres dla satysfakcji klientów
        ax5.plot(week_numbers, very_satisfied_total, label='Bardzo zadowoleni', color='g')
        ax5.plot(week_numbers, satisfied_total, label='Zadowoleni', color='b')
        ax5.plot(week_numbers, unsatisfied_total, label='Niezadowoleni', color='r')
        ax5.set_ylabel('Liczba klientów')
        ax5.set_title('Satysfakcja klientów w skali roku')
        ax5.legend()

        plt.tight_layout()

        # Create a FigureCanvasTkAgg
        self.results_canvas = FigureCanvasTkAgg(fig, master=self.results_inner_frame)
        self.results_canvas.draw()

        # Pack the FigureCanvasTkAgg
        self.results_canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

    # Dodanie predefiniowanych rozmiarów
    def update_entries(self, button_distinguish):
        self.mu_hours_entry.delete(0, tk.END)
        self.mu_hours_entry_min.delete(0, tk.END)
        self.checkouts_number.delete(0, tk.END)
        self.selfcheckouts_number.delete(0, tk.END)
        self.sigma_hours_entry.delete(0, tk.END)
        self.daily_variation_entry.delete(0, tk.END)
        self.yearly_variation_entry.delete(0, tk.END)
        self.shop_size.delete(0, tk.END)
        self.markup_entry.delete(0, tk.END)

        if button_distinguish == 1:
            self.mu_hours_entry.insert(0, "1200")
            self.mu_hours_entry_min.insert(0, "250")
            self.checkouts_number.insert(0, "20")
            self.selfcheckouts_number.insert(0, "30")
            self.sigma_hours_entry.insert(0, "16")
            self.daily_variation_entry.insert(0, "5")
            self.yearly_variation_entry.insert(0, "6")
            self.shop_size.insert(0, "PLACEHOLDER")
            
        if button_distinguish == 2:
            self.mu_hours_entry.insert(0, "600")
            self.mu_hours_entry_min.insert(0, "120")
            self.checkouts_number.insert(0, "10")
            self.selfcheckouts_number.insert(0, "20")
            self.sigma_hours_entry.insert(0, "12")
            self.daily_variation_entry.insert(0, "6")
            self.yearly_variation_entry.insert(0, "9")
            self.shop_size.insert(0, "PLACEHOLDER")
           
        if button_distinguish == 3:
            self.mu_hours_entry.insert(0, "250")
            self.mu_hours_entry_min.insert(0, "30")
            self.checkouts_number.insert(0, "6")
            self.selfcheckouts_number.insert(0, "8")
            self.sigma_hours_entry.insert(0, "14")
            self.daily_variation_entry.insert(0, "4")
            self.yearly_variation_entry.insert(0, "11")
            self.shop_size.insert(0, "PLACEHOLDER")
            
        if button_distinguish == 4:
            self.mu_hours_entry.insert(0, "40")
            self.mu_hours_entry_min.insert(0, "5")
            self.checkouts_number.insert(0, "4")
            self.selfcheckouts_number.insert(0, "4")
            self.sigma_hours_entry.insert(0, "10")
            self.daily_variation_entry.insert(0, "7")
            self.yearly_variation_entry.insert(0, "7")
            self.shop_size.insert(0, "PLACEHOLDER")
            
    def on_close(self):
        # Stopuje symulacje
        if hasattr(self, 'simulation'):
            self.simulation.stop()
        # Kończy okno
        self.master.destroy()
