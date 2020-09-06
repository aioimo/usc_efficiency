import requests
from bs4 import BeautifulSoup
from time import sleep
from re import sub
from decimal import Decimal
from dotenv import load_dotenv
import os

load_dotenv()

base_url = "https://www.urbansportsclub.com/en"
login_url = 'https://urbansportsclub.com/en/login'
headers = {'User-Agent': 'Mozilla/5.0'}

def parse_email(email):
  return email.replace("@", "%40")

email = parse_email(os.environ.get('EMAIL'))
password = os.environ.get('PASSWORD')



session = requests.Session()

r = session.get(base_url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

login_form = soup.find(id="login-form")
hidden_input = login_form.find(type="hidden")

hidden_id = hidden_input['id']
hidden_value = hidden_input['value']

base_data = "&check=&email=" + email + "&password=" + password + "&remember-me=1"

data = hidden_id + "=" + hidden_value + base_data

request_headers = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0', 'x-newrelic-id': hidden_id}


s = session.post(login_url, data=data, headers=request_headers)

sleep(2)

s = session.get(base_url + '/profile/membership', headers=headers)
soup = BeautifulSoup(s.text, 'html.parser')

# all_stats = soup.find("div", class_="smm-checkin-stats")
check_ins = soup.find("span", class_="smm-checkin-stats__total")

number_of_total_checkins = Decimal(check_ins.text.strip())


sleep(2)

r_2 = session.get(base_url + '/profile/payment-history', headers=headers)

soup_payment_history = BeautifulSoup(r_2.text, 'html.parser')

table = soup_payment_history.find("div", class_="smm-payment-history__table")
rows = table.select("div .smm-payment-history__table-row")

def parse_row(row):
  columns = row.find_all("div")
  price = columns[-1]
  return price.text.strip()


def parse_amounts(amount):
  return Decimal(sub(r'[^\d.]', '', amount)) / Decimal(100)



prices_unparsed = map(parse_row, rows)
prices = map(parse_amounts, prices_unparsed)
total_cost = sum(prices)

average_cost_per_checkin = total_cost / number_of_total_checkins

print("The results are.....")
print("Total cost: ", total_cost)
print("Number of checkins: ", number_of_total_checkins)
print("Average EUR / checkin: ", average_cost_per_checkin)
