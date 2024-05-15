import numpy as np
import matplotlib.pyplot as plt

class ShopSimulation:
    def __init__(self, params):
        self.params = params
        self.yearsTimeResults = []

    def run(self):
        days_of_week = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

        # Define possible daily changes for Monte Carlo simulation
        possible_changes = [0, 5, -5, 10, -10, 15, -15]  # Example changes in customer counts

        for _ in range(56):  # Run simulation for 56 weeks
            self.results = {
                'customer_count': [],
                'average_satisfaction': [],
                'average_basket_price': [],
                'average_spending': [],
                'employee_costs': 0,
                'revenue': 0,
                'net_earnings': 0
            }

            for day_idx, day in enumerate(days_of_week):
                # Monte Carlo simulation for daily variation
                daily_variation =  np.random.choice(possible_changes)

                # Yearly variation remains the same
                month = (_ // 4) % 12
                yearly_variation = np.random.normal(loc=0, scale=self.params['yearly_variation'])

                # Customer count influenced by both daily and yearly variations
                customer_count = np.random.normal(
                    loc=max(self.params['mu_hours'] + daily_variation + yearly_variation, self.params['mu_min_hours']),
                    scale=self.params['sigma_hours']
                )
                customer_count = max(int(customer_count), 0)
                self.results['customer_count'].append(customer_count)

                # Generate data for customer satisfaction, basket price, and spending
                satisfaction = np.clip(np.random.normal(0.5, 0.2), 0, 1)
                basket_price = np.clip(np.random.normal(55, 20), 10, None)
                spending = customer_count * basket_price

                self.results['average_satisfaction'].append(satisfaction)
                self.results['average_basket_price'].append(basket_price)
                self.results['average_spending'].append(spending)

                self.results['employee_costs'] = np.clip(np.random.normal(3000, 1000), 1000, None)
                self.results['revenue'] = sum(self.results['average_spending'])
                self.results['net_earnings'] = self.results['revenue'] - self.results['employee_costs']

            self.yearsTimeResults.append(self.results)