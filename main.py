import os
from dotenv import load_dotenv
from USCEfficiency import USCEfficiency 

load_dotenv()

def format_email(email):
  return email.replace('@', '%40')


email = format_email(os.environ.get('EMAIL'))
password = os.environ.get('PASSWORD')


if __name__ == '__main__':
  instance = USCEfficiency(email,password)
  instance.start()
