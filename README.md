## About

USC is a sports app where the user pays a fixed monthly fee for access to various participating sports venues (yoga studios, swimming pools, gyms, etc.). This script does the following:

1. Logs into the USC web app.
2. Fetches the total number of check-ins.
3. Fetches the payment history table, thus calculating the total amount paid since adoption of the app.
4. Returns the up-to-date Euros per check-in rate.

## Setup

Create a `.env` file with the relevant USC email and password.

```
EMAIL=
PASSWORD=
```

## Sample output

```
Urban Sports Club stats:
Total payment amount (EUR):  2496.27
Number of check-ins:  347
EUR / check-in:  7.193861671469740634005763689
```
