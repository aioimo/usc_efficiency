import os
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from dotenv import load_dotenv
from re import sub
from time import sleep

load_dotenv()


base_url = 'https://www.urbansportsclub.com/en'
login_url = 'https://urbansportsclub.com/en/login'


def format_email(email):
  return email.replace('@', '%40')


def parse_row(row):
  columns = row.find_all('div')
  price = columns[-1]
  return price.text.strip()


def parse_amounts(amount):
  return Decimal(sub(r'[^\d.]', '', amount)) / Decimal(100)


def print_results(total_cost, number_of_checkins, eur_per_checkin):
  print('Urban Sports Club – Euros per check-in:')
  print('Total payment amount (EUR): ', total_cost)
  print('Number of check-ins: ', number_of_checkins)
  print('EUR / check-in: ', eur_per_checkin)


email = format_email(os.environ.get('EMAIL'))
password = os.environ.get('PASSWORD')


## Start the session
session = requests.Session()


## Handle login 
get_headers = {'User-Agent': 'Mozilla/5.0'}
login_response = session.get(base_url, headers=get_headers)
login_soup = BeautifulSoup(login_response.text, 'html.parser')

# Find DOM element: hidden <input>
login_form = login_soup.find(id='login-form')
hidden_input = login_form.find(type='hidden')

# Extract values from hidden input
hidden_key = hidden_input['id']
hidden_value = hidden_input['value']

# Configure headers and data from hidden keys
data = f'{hidden_key}={hidden_value}&check=&email={email}&password={password}&remember-me=1'
post_headers = {
  'content-type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0',
  'x-newrelic-id': hidden_key
}

# Send login POST request 
session.post(login_url, data=data, headers=post_headers)
sleep(1)


## Find total number of check-ins
membership_response = session.get(base_url + '/profile/membership', headers=get_headers)
membership_soup = BeautifulSoup(membership_response.text, 'html.parser')

# Find DOM element with value: <span>142</span> Check-ins
check_ins = membership_soup.find('span', class_='smm-checkin-stats__total')

number_of_checkins = Decimal(check_ins.text.strip())
sleep(1)

## Find total amount paid
payment_history_response = session.get(base_url + '/profile/payment-history', headers=get_headers)
payment_history_soup = BeautifulSoup(payment_history_response.text, 'html.parser')

# Find DOM elements: table and rows
# Find DOM element with value: <span>60,00€</span>
table = payment_history_soup.find('div', class_='smm-payment-history__table')
rows = table.select('div .smm-payment-history__table-row')

prices_column = map(parse_row, rows)
list_of_prices = map(parse_amounts, prices_column)

total_cost = sum(list_of_prices)
eur_per_checkin = total_cost / number_of_checkins

## Print results
print_results(total_cost, number_of_checkins, eur_per_checkin)

