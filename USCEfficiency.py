import requests
from bs4 import BeautifulSoup
from re import sub
from time import sleep
from decimal import Decimal
from Results import Results


class USCEfficiency:
  base_url = 'https://www.urbansportsclub.com/en'
  login_url = 'https://urbansportsclub.com/en/login'
  get_headers = {'User-Agent': 'Mozilla/5.0'}

  def __init__(self, email, password):
    self.email = email
    self.password = password 
    self.session = requests.Session()


  def start(self):
    self.login()
    self.get_number_of_check_ins()
    self.get_total_amount_paid()
    self.print_results()

  def parse_amount(self, amount):
    return Decimal(sub(r'[^\d.]', '', amount)) / Decimal(100)

  def parse_row(self, row):
    columns = row.find_all('div')
    price = columns[-1]
    return price.text.strip()


  def login(self):
    self.get_headers = {'User-Agent': 'Mozilla/5.0'}
    login_response = self.session.get(self.base_url, headers=self.get_headers)
    login_soup = BeautifulSoup(login_response.text, 'html.parser')

    # Find DOM element: hidden <input>
    login_form = login_soup.find(id='login-form')
    hidden_input = login_form.find(type='hidden')

    # Extract values from hidden input
    hidden_key = hidden_input['id']
    hidden_value = hidden_input['value']

    # Configure headers and data from hidden keys
    data = f'{hidden_key}={hidden_value}&check=&email={self.email}&password={self.password}&remember-me=1'
    post_headers = {
      'content-type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0',
      'x-newrelic-id': hidden_key
    }
    self.session.post(self.login_url, data=data, headers=post_headers)
    sleep(1)


  def get_number_of_check_ins(self): 
    membership_response = self.session.get(self.base_url + '/profile/membership', headers=self.get_headers)
    membership_soup = BeautifulSoup(membership_response.text, 'html.parser')

    # Find DOM element with value: <span>142</span> Check-ins
    check_ins = membership_soup.find('span', class_='smm-checkin-stats__total')

    self.number_of_checkins = Decimal(check_ins.text.strip())
    sleep(1)


  def get_total_amount_paid(self):
    payment_history_response = self.session.get(self.base_url + '/profile/payment-history', headers=self.get_headers)
    payment_history_soup = BeautifulSoup(payment_history_response.text, 'html.parser')

    # Find DOM elements: table and rows
    # Find DOM element with value: <span>60,00€</span>
    table = payment_history_soup.find('div', class_='smm-payment-history__table')
    rows = table.select('div .smm-payment-history__table-row')

    prices_column = map(self.parse_row, rows)
    list_of_prices = map(self.parse_amount, prices_column)

    self.total_cost = sum(list_of_prices)


  def print_results(self):
    results = Results(self.number_of_checkins, self.total_cost)
    results.display()