import numpy as np
import matplotlib.pyplot as plt

class ShopSimulation:
    def __init__(self, params):
        # Inicjalizacja obiektu symulacji sklepu z parametrami
        self.params = params  # Parametry symulacji
        self.yearsTimeResults = []
        self.results = {}  # Wyniki symulacji

    def run(self):
        # Metoda do przeprowadzenia symulacji
        days_of_week = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        daily_variation = [0, self.params['daily_variation']]

        # Pętla 56 tyg czyli cały rok jeden tydzień to jedna iteracja
        for _ in range(56):
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

            for day_idx, day in enumerate(days_of_week):
                # Daily variation
                daily_variation = np.random.normal(loc=0, scale=self.params['daily_variation'])

                # Yearly variation
                month = (_ // 4) % 12  # Assuming 4 weeks in a month
                yearly_variation = np.random.normal(loc=0, scale=self.params['yearly_variation'])

                # Customer count
                customer_count = np.random.normal(
                    loc=max(self.params['mu_hours'] + daily_variation + yearly_variation, self.params['mu_min_hours']),
                    scale=self.params['sigma_hours']
                )
                # Zapewnienie, że liczba klientów nie jest ujemna
                customer_count = max(int(customer_count), 0)
                self.results['customer_count'].append(customer_count)

                # Losowe generowanie danych dotyczących zadowolenia, koszyka, i wydatków klientów
                satisfaction = np.random.normal(loc=0.5, scale=0.2)
                satisfaction = max(min(satisfaction, 1), 0)  # Zapewnienie, że zadowolenie jest w przedziale [0, 1]
                basket_price = np.random.normal(loc=55, scale=20)
                basket_price = max(basket_price, 10)  # Minimalna cena koszyka to 10
                spending = customer_count * basket_price

                self.results['average_satisfaction'].append(satisfaction)
                self.results['average_basket_price'].append(basket_price)
                self.results['average_spending'].append(spending)

            # Losowe generowanie kosztów pracowników
            self.results['employee_costs'] = np.random.normal(loc=3000, scale=1000)
            self.results['employee_costs'] = max(self.results['employee_costs'], 1000)  # Minimalne koszty to 1000
            # Obliczanie dochodu
            self.results['revenue'] = sum(self.results['average_spending'])
            # Obliczanie zysku netto
            self.results['net_earnings'] = self.results['revenue'] - self.results['employee_costs']

            # Dodawanie do listy z informacjami z tygodni
            self.yearsTimeResults.append(self.results)
