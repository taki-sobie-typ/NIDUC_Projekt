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

        checkouts_number = self.params['checkouts_number']
        selfcheckouts_number = self.params['selfcheckouts_number']
        open_hours = self.params['open_hours']

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
                for _ in range(customer_count):
                  satisfaction = np.clip(np.random.normal(0.5, 0.2), 0, 1)
                  basket_price = np.clip(np.random.normal(55, 20), 10, None)

                 # Additional factors influencing spending based on satisfaction
                  if satisfaction > 0.7:
                    basket_price *= 1.1  # Buy more things if very satisfied
                  elif satisfaction < 0.3:
                    basket_price *= 0.9  # Forget something if unsatisfied
                  
                  #Forgot item
                  forgot_item = np.random.rand()
                  if forgot_item < 0.1:
                     basket_price *= 0.8  # Forget some items (10% probability)

                 #Bought more
                  bought_more = np.random.rand()
                  if bought_more < 0.15:
                     basket_price *= 1.2  # Buy more items (15% probability)
                 
                 
                 #Super spender
                  super_spender = np.random.rand()
                  if super_spender < 0.02:  # 2% probability of being a super spender
                     basket_price *= 2.0  # Spend twice as much

                #Low spender
                  low_spender = np.random.rand()
                  if low_spender < 0.3:  # 30% probability of spending less
                     basket_price *= 0.7  # Spend 30% less

                  spending = basket_price

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
                hourly_customers = customer_count / open_hours

                for hours in range(int(open_hours)):
                    hourly_standard_queue = 0
                    hourly_self_queue = 0

                    for _ in range(int(hourly_customers)):
                        # Generate age for each customer
                        age = np.random.randint(15, 91)
                        prob = np.random.rand()
                        self.results['age_distribution'].append(age)


                        # Determine queue choice based on age
                        if 15 <= age <= 45:
                            if prob < 0.7:
                                daily_self_queue += 1
                                hourly_self_queue += 1
                                self.results['queue_choices']['self'] += 1
                            else:
                                daily_standard_queue += 1
                                hourly_standard_queue += 1
                                self.results['queue_choices']['standard'] += 1
                        elif 45 < age <= 60:
                            if prob < 0.5:
                                daily_self_queue += 1
                                hourly_self_queue += 1
                                self.results['queue_choices']['self'] += 1
                            else:
                                daily_standard_queue += 1
                                hourly_standard_queue += 1
                                self.results['queue_choices']['standard'] += 1
                        else:
                            if prob < 0.1:
                                daily_self_queue += 1
                                hourly_self_queue += 1
                                self.results['queue_choices']['self'] += 1
                            else:
                                daily_standard_queue += 1
                                hourly_standard_queue += 1
                                self.results['queue_choices']['standard'] += 1


                    standard_waiting_time = self.calculate_time(hourly_standard_queue, checkouts_number, checkout_time)
                    self_waiting_time = self.calculate_time(hourly_self_queue, selfcheckouts_number, selfcheckout_time)


                    satisfaction = self.calculate_satisfaction(standard_waiting_time, self_waiting_time)
                    self.results['customer_satisfaction']['very_satisfied'] += satisfaction['very_satisfied']
                    self.results['customer_satisfaction']['satisfied'] += satisfaction['satisfied']
                    self.results['customer_satisfaction']['unsatisfied'] += satisfaction['unsatisfied']
                    self.results['waiting_time'].append((self.calculate_avg(standard_waiting_time, hourly_standard_queue),self.calculate_avg(self_waiting_time, hourly_self_queue)))
                self.results['queue_length'].append((daily_standard_queue, daily_self_queue))


            self.yearsTimeResults.append(self.results)

    def calculate_time(self, queue, checkouts, time ):
        waiting_time = []
        for i in range(queue):
            if i < checkouts:
                waiting_time.append(time)
            else :
                waiting_time.append(time * ((i+1) // checkouts))


        return waiting_time

    def calculate_avg(self, queue, len):
        if( queue == 0 or len == 0):
            return 0
        else:
            return sum(queue) / len

    def calculate_satisfaction(self, standard_waiting_times, self_waiting_times):
        satisfaction = {'very_satisfied': 0, 'satisfied': 0, 'unsatisfied': 0}

        for time in standard_waiting_times:
            if time < 3: #3
                satisfaction['very_satisfied'] += 1
            elif time < 5.5: #5
                satisfaction['satisfied'] += 1
            else:
                satisfaction['unsatisfied'] += 1

        for time in self_waiting_times:
            if time < 2: #2
                satisfaction['very_satisfied'] += 1
            elif time < 4: #4
                satisfaction['satisfied'] += 1
            else:
                satisfaction['unsatisfied'] += 1

        return satisfaction

