import os
import time
from dotenv import load_dotenv
from USCEfficiency import USCEfficiency 

load_dotenv()

def format_email(email):
  return email.replace('@', '%40')


email = format_email(os.environ.get('EMAIL'))
password = os.environ.get('PASSWORD')


t1 = time.time()
if __name__ == '__main__':
  instance = USCEfficiency(email,password)
  instance.start()

t2 = time.time()

total = t2 - t1
print(f"Code executed in {total} seconds")

