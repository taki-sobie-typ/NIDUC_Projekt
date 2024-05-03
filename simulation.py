import numpy as np

class ShopSimulation:
    def __init__(self, params):
        # Inicjalizacja parametrów symulacji sklepu
        self.params = params
        # Inicjalizacja wyników symulacji
        self.results = {
            'customer_count': {day: [] for day in ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Niedz"]},
            'average_satisfaction': [],
            'average_basket_price': [],
            'average_spending': [],
            'employee_costs': 0,
            'revenue': 0,
            'net_earnings': 0
        }

    def run(self):
        # Główna pętla symulacyjna
        for week in range(self.params['weeks']):
            for day_name in self.params['selected_days']:
                # Symulacja liczby klientów na podstawie rozkładu normalnego
                customer_count = np.random.normal(loc=self.params['mu_hours'], scale=self.params['sigma_hours'])
                # Zapisywanie liczby klientów, zabezpieczenie przed wartościami ujemnymi
                self.results['customer_count'][day_name].append(max(int(customer_count), 0))

        # Obliczanie całkowitej liczby klientów
        total_customer_count = sum([sum(c) for c in self.results['customer_count'].values()])

        # Obliczanie całkowitego przychodu
        self.results['revenue'] = total_customer_count * np.random.uniform(10, 100)

        # Obliczanie całkowitych kosztów pracowniczych
        self.results['employee_costs'] = np.random.uniform(1000, 5000) * self.params['weeks']

        # Obliczanie zysków netto (przychody minus koszty)
        self.results['net_earnings'] = self.results['revenue'] - self.results['employee_costs']
