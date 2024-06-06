import numpy as np


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
        selfcheckout_time = 1

        # Getting starting paramaters
        checkouts_number = self.params['checkouts_number']
        selfcheckouts_number = self.params['selfcheckouts_number']
        open_time = self.params['open_time']
        close_time = self.params['close_time']
        open_hours = close_time - open_time  # Calculate the number of open hours
        sigma_hours = self.params['sigma_hours']  # Standard deviation for hourly customer arrivals

        peak1_time = open_time + 3  # First peak 3 hours after opening
        peak2_time = close_time - 3  # Second peak 3 hours before closing

        alter_basket = 0
        shop_size = self.params['shop_size']
        if (shop_size == 0):
            alter_basket = 0.75
        elif (shop_size == 1):
            alter_basket = 0.87
        else:
            alter_basket = 1

        for _ in range(52):  # Run simulation for 56 weeks
            self.results = {
                'customer_count': [],
                'average_satisfaction': [],
                'average_basket_price': [],
                'average_spending': [],
                'employee_costs': 0,
                'shop_size': 0,
                'revenue': 0,
                'net_earnings': 0,
                'queue_length': [],
                'waiting_time': [],
                'waiting_time_s': [],
                'customer_satisfaction': {'very_satisfied': 0, 'satisfied': 0, 'unsatisfied': 0},
                'age_distribution': [],
                'queue_choices': {'standard': 0, 'self': 0},
                'product_costs': 0,  # Add this line to store total product costs
                'malfunctions': [],
                's_malfunctions': [],
                'n_malfunctions': [],
                'open_hours': 0

            }

            for day_idx, day in enumerate(days_of_week):
                # Monte Carlo simulation for daily variation
                daily_variation = np.random.choice(possible_changes)

                # Yearly variation remains the same
                month = (_ // 4) % 12
                yearly_variation = np.random.normal(loc=0, scale=self.params['yearly_variation'])

                # Customer count influenced by both daily and yearly variations
                # hourly_customer_counts = []
                # for hour in range(open_time, close_time):
                #   peak1_customers = np.random.normal(loc=self.params['mu_hours']/open_hours, scale=sigma_hours)
                #   peak2_customers = np.random.normal(loc=self.params['mu_hours']/open_hours, scale=sigma_hours)
                #   combined_customers = peak1_customers * np.exp(-0.5 * ((hour - peak1_time) / sigma_hours)**2) + \
                #                        peak2_customers * np.exp(-0.5 * ((hour - peak2_time) / sigma_hours)**2)
                #   hourly_customer_counts.append(max(int(combined_customers), 0))

                # customer_count = sum(hourly_customer_counts)
                # self.results['customer_count'].append(customer_count)

                customer_count = np.random.normal(
                    loc=max(self.params['mu_hours'] + daily_variation + yearly_variation, self.params['mu_min_hours']),
                    scale=self.params['sigma_hours']
                )
                customer_count = max(int(customer_count), 0)
                self.results['customer_count'].append(customer_count)

                # Generate data for customer satisfaction, basket price, and spending
                for _ in range(customer_count):
                    satisfaction = np.clip(np.random.normal(0.5, 0.2), 0, 1)
                    alter_now = np.clip(np.random.normal(0.03, 0.01), 0.01, 0.05)  # losowanie z przedzialu 0.01 - 0.05
                    more_or_less = np.random.choice([True, False])
                    if (more_or_less == True):
                        alter_now += alter_basket
                    else:
                        alter_now = alter_basket - alter_now

                    if (alter_now > 1):
                        alter_now = 1
                    basket_price = np.clip(np.random.normal(35, 20), 15, None)

                    # Additional factors influencing spending based on satisfaction
                    # if satisfaction > 0.7:
                    #    basket_price *= 1.1  # Buy more things if very satisfied
                    # elif satisfaction < 0.3:
                    #    basket_price *= 0.9  # Forget something if unsatisfied

                    # Altering basket price based on how many items were available
                    basket_price *= alter_now

                    # Forgot item
                    forgot_item = np.random.rand()
                    if forgot_item < 0.1:
                        basket_price *= 0.8  # Forget some items (10% probability)

                    # Bought more
                    bought_more = np.random.rand()
                    if bought_more < 0.15:
                        basket_price *= 1.2  # Buy more items (15% probability)

                    # Super spender
                    super_spender = np.random.rand()
                    if super_spender < 0.02:  # 2% probability of being a super spender
                        basket_price *= 2.0  # Spend twice as much

                    # Low spender
                    low_spender = np.random.rand()
                    if low_spender < 0.3:  # 30% probability of spending less
                        basket_price *= 0.7  # Spend 30% less

                    spending = basket_price
                    product_cost = basket_price / (
                            1 + self.params['markup_percentage'] / 100)  # Calculate product cost without markup
                    self.results['product_costs'] += product_cost

                    self.results['average_satisfaction'].append(satisfaction)
                    self.results['average_basket_price'].append(basket_price)
                    self.results['average_spending'].append(spending)

                self.results['employee_costs'] = np.clip(np.random.normal(1500, 700), 500, None) * checkouts_number
                self.results['revenue'] = sum(self.results['average_spending'])
                self.results['net_earnings'] = self.results['revenue'] - self.results['employee_costs'] - self.results[
                    'product_costs']  # Subtract product costs from net earnings
                # Initialize queue counts for the day
                daily_standard_queue = 0
                daily_self_queue = 0

                # Adding queue
                hourly_customers = customer_count / open_hours

                n_malfunctions = 0  ##
                s_malfunctions = 0  ##
                malfunctions = 0  ##

                avg_self = 0
                avg_normal = 0

                for hour in range(open_time, close_time):
                    hourly_standard_queue = 0
                    hourly_self_queue = 0
                    new_checkouts_number = checkouts_number
                    new_selfcheckouts_number = selfcheckouts_number
                    if (np.random.rand() < 0.0):
                        altering = int(np.clip(np.random.normal(1.5, 0.25), 1, 2))
                        new_checkouts_number -= altering
                        if (new_checkouts_number < 1):
                            n_malfunctions += checkouts_number - 1
                            malfunctions += checkouts_number - 1
                        else:
                            n_malfunctions += altering  ##
                            malfunctions += altering  ##
                    if (np.random.rand() < 0.0):
                        altering = int(np.clip(np.random.normal(2.5, 0.75), 1, 3))
                        new_selfcheckouts_number -= altering
                        if (new_selfcheckouts_number < 1):
                            s_malfunctions += selfcheckouts_number - 1
                            malfunctions += selfcheckouts_number - 1
                        else:
                            s_malfunctions += altering  ##
                            malfunctions += altering  ##

                    if (new_checkouts_number < 1):
                        new_checkouts_number = 1
                    if (new_selfcheckouts_number < 1):
                        new_selfcheckouts_number = 1

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
                    # self.results['waiting_time'].append(self.calculate_avg(standard_waiting_time, hourly_standard_queue, checkout_time), self.calculate_avg(self_waiting_time,hourly_self_queue,selfcheckout_time))
                    # self.results['waiting_time_s'].append(self.calculate_avg(self_waiting_time,hourly_self_queue,selfcheckout_time))
                    # self.results['waiting_time'].append((self.calculate_avg(standard_waiting_time,
                    #                   hourly_standard_queue, checkout_time),
                    #  self.calculate_avg(self_waiting_time, hourly_self_queue, selfcheckout_time)))
                    # print(self.calculate_avg(standard_waiting_time, hourly_standard_queue, checkout_time))
                    # print(self.calculate_full(standard_waiting_time))
                    # print(hourly_standard_queue)
                    # print(self.calculate_avg(self_waiting_time, hourly_self_queue, checkout_time))
                    avg_self += self.calculate_avg(self_waiting_time, hourly_self_queue, selfcheckout_time)
                    avg_normal += self.calculate_avg(standard_waiting_time, hourly_standard_queue, checkout_time)
                    # print(self.calculate_avg(self_waiting_time, hourly_self_queue, selfcheckout_time))
                self.results['n_malfunctions'].append(n_malfunctions)  ##
                self.results['s_malfunctions'].append(s_malfunctions)  ##
                self.results['malfunctions'].append(malfunctions)  ##
                avg_self /= open_hours

                avg_normal /= open_hours

                self.results['waiting_time'].append(avg_normal)
                self.results['waiting_time_s'].append(avg_self)

                self.results['queue_length'].append((daily_standard_queue, daily_self_queue))

            self.yearsTimeResults.append(self.results)

    def calculate_time(self, queue, checkouts, time):
        waiting_time = []
        # print(checkouts)
        for i in range(queue):
            # print(i)
            if i < checkouts:
                waiting_time.append(time)
            else:
                waiting_time.append(time + (time * (i // checkouts)))
                # print(i)
                # print(time * (i //checkouts))

        return waiting_time

    def calculate_avg(self, queue, len, checkout_time):
        if (queue == 0 or len == 0):
            return checkout_time
        else:
            return sum(queue) / len

    def calculate_full(self, queue):
        if (queue != 0):
            return sum(queue)

    def calculate_satisfaction(self, standard_waiting_times, self_waiting_times):
        satisfaction = {'very_satisfied': 0, 'satisfied': 0, 'unsatisfied': 0}

        for time in standard_waiting_times:
            if time < 2.5:  # 3
                satisfaction['very_satisfied'] += 1
            elif time < 3.5:  # 5
                satisfaction['satisfied'] += 1
            else:
                satisfaction['unsatisfied'] += 1

        for time in self_waiting_times:
            if time < 1.5:  # 2
                satisfaction['very_satisfied'] += 1
            elif time < 2.5:  # 4
                satisfaction['satisfied'] += 1
            else:
                satisfaction['unsatisfied'] += 1

        return satisfaction