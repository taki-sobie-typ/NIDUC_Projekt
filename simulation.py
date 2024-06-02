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

        # Define time needed to serve one customer
        checkout_time = 1
        selfcheckout_time = 0.5

        for _ in range(56):  # Run simulation for 56 weeks
            self.results = {
                'customer_count': [],
                'average_satisfaction': [],
                'average_basket_price': [],
                'average_spending': [],
                'employee_costs': 0,
                'revenue': 0,
                'net_earnings': 0,
                'queue_length': [],
                'waiting_time': [],
                'customer_satisfaction': {'very_satisfied': 0, 'satisfied': 0, 'unsatisfied': 0},
                'age_distribution': [],
                'queue_choices': {'standard': 0, 'self': 0}

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

                # Initialize queue counts for the day
                daily_standard_queue = 0
                daily_self_queue = 0

                # Adding queue
                checkouts_number = self.params['checkouts_number']
                selfcheckouts_number = self.params['selfcheckouts_number']
                open_hours = self.params['open_hours']

                for _ in range(customer_count):
                    # Generate age for each customer
                    age = np.random.randint(15, 91)
                    self.results['age_distribution'].append(age)

                    # Determine queue choice based on age
                    if 15 <= age <= 45:
                        if np.random.rand() < 0.7:
                            daily_self_queue += 1
                            self.results['queue_choices']['self'] += 1
                        else:
                            daily_standard_queue += 1
                            self.results['queue_choices']['standard'] += 1
                    elif 45 < age <= 60:
                        if np.random.rand() < 0.5:
                            daily_self_queue += 1
                            self.results['queue_choices']['self'] += 1
                        else:
                            daily_standard_queue += 1
                            self.results['queue_choices']['standard'] += 1
                    else:
                        if np.random.rand() < 0.1:
                            daily_self_queue += 1
                            self.results['queue_choices']['self'] += 1
                        else:
                            daily_standard_queue += 1
                            self.results['queue_choices']['standard'] += 1

                hourly_customers = customer_count / open_hours
                standard_queue_length = max(0, hourly_customers / checkouts_number)
                self_queue_length = max(0, hourly_customers / selfcheckouts_number)

                self.results['queue_length'].append((standard_queue_length, self_queue_length))
                self.results['waiting_time'].append((standard_queue_length * checkout_time, self_queue_length * selfcheckout_time))



            self.yearsTimeResults.append(self.results)