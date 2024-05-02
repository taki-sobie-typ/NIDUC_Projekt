import numpy as np
import matplotlib.pyplot as plt

class ShopSimulation:
    def __init__(self, params):
        # Inicjalizacja obiektu symulacji sklepu z parametrami
        self.params = params  # Parametry symulacji
        self.results = {}  # Wyniki symulacji

    def run(self):
        # Metoda do przeprowadzenia symulacji
        days_of_week = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        # Tworzenie słownika na wyniki symulacji
        self.results = {
            'customer_count': [],  # Liczba klientów
            'average_satisfaction': [],  # Średnie zadowolenie klientów
            'average_basket_price': [],  # Średnia wartość koszyka
            'average_spending': [],  # Średnie wydatki
            'employee_costs': 0,  # Koszty pracowników
            'revenue': 0,  # Dochód
            'net_earnings': 0  # Zysk netto
        }

        for day in days_of_week:
            # Generowanie liczby klientów na podstawie rozkładu normalnego
            customer_count = np.random.normal(loc=self.params['mu_hours'], scale=self.params['sigma_hours'])
            self.results['customer_count'].append(max(int(customer_count), 0))

            # Losowe generowanie danych dotyczących zadowolenia, koszyka, i wydatków klientów
            self.results['average_satisfaction'].append(np.random.random())
            self.results['average_basket_price'].append(np.random.uniform(10, 100))
            self.results['average_spending'].append(customer_count * np.random.uniform(10, 100))

        # Losowe generowanie kosztów pracowników
        self.results['employee_costs'] = np.random.uniform(1000, 5000)
        # Obliczanie dochodu
        self.results['revenue'] = sum(self.results['average_spending'])
        # Obliczanie zysku netto
        self.results['net_earnings'] = self.results['revenue'] - self.results['employee_costs']
