import math
from decimal import Decimal

PRICE_PER_MONTH = 59.00
DIVIDER = '---------------------'

class Results:
  def __init__(self, number_of_checkins, total_cost, cost_per_month = PRICE_PER_MONTH):
    self.number_of_checkins = number_of_checkins
    self.total_cost = total_cost
    self.cost_per_month = Decimal(cost_per_month)
    

  def eur_per_checkin(self):
    return self.total_cost / self.number_of_checkins

  def checkins_improval_threshold(self):
    return self.cost_per_month / self.eur_per_checkin()

  def assuming_n_check_ins(self, n):
    numerator = self.total_cost + self.cost_per_month
    denominator = self.number_of_checkins + Decimal(n)
    return round(numerator / denominator, 2)

  def print_for_n(self,n):
    s = f"  {n} checkins:\t{self.assuming_n_check_ins(n)} EUR / checkin"
    print(s)

  def display(self):
    print('Urban Sports Club – Euros per check-in:')
    print(DIVIDER)
    print('Total payment amount (EUR) : ', self.total_cost)
    print('Number of check-ins: ', self.number_of_checkins)
    print('EUR / check-in: ', round(self.eur_per_checkin(), 2))
    print(DIVIDER)
    print('To improve this rate:', f"{math.ceil(self.checkins_improval_threshold())} check-ins in the next 30 days")
    print(DIVIDER)
    print('In the next 30 days, n checkins will yield the following results:')
    self.print_for_n(2)
    self.print_for_n(3)
    self.print_for_n(5)
    self.print_for_n(8)
    self.print_for_n(10)
    self.print_for_n(15)
    self.print_for_n(30)
    print(DIVIDER)


