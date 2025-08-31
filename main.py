#Q1
print("Enter the loan principal:")
principal = int(input())
print("Enter the monthly payment:")
payment = int(input())

months = principal // payment
if principal % payment != 0:
    months += 1

print(f"It will take {months} months to repay the loan")

#Q2
print("Enter the loan principal:")
principal = int(input())

print('What do you want to calculate?')
print('type "m" - for number of monthly payments,')
print('type "p" - for the monthly payment:')
choice = input().strip()

if choice == "m":
    print("Enter the monthly payment:")
    payment = int(input())
    months = principal // payment
    if principal % payment != 0:
        months += 1
    if months == 1:
        print("It will take 1 month to repay the loan")
    else:
        print(f"It will take {months} months to repay the loan")

elif choice == "p":
    print("Enter the number of months:")
    months = int(input())
    # round up the payment
    payment = (principal + months - 1) // months
    last_payment = principal - (months - 1) * payment
    if last_payment == payment:
        print(f"Your monthly payment = {payment}")
    else:
        print(f"Your monthly payment = {payment} and the last payment = {last_payment}.")

#Q3
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float, required=True)
args = parser.parse_args()

i = args.interest / (12 * 100)

if args.periods is None and args.payment is not None and args.principal is not None:
    n_raw = math.log(args.payment / (args.payment - i * args.principal), 1 + i)
    n = math.ceil(n_raw)

    years = n // 12
    months = n % 12

    parts = []
    if years == 1:
        parts.append("1 year")
    elif years > 1:
        parts.append(f"{years} years")
    if months == 1:
        parts.append("1 month")
    elif months > 1:
        parts.append(f"{months} months")

    when = " and ".join(parts) if parts else "0 months"
    print(f"It will take {when} to repay this loan!")

elif args.payment is None and args.principal is not None and args.periods is not None:
    A = args.principal * i * (1 + i) ** args.periods / ((1 + i) ** args.periods - 1)
    payment = math.ceil(A)
    print(f"Your monthly payment = {payment}!")

elif args.principal is None and args.payment is not None and args.periods is not None:
    P = args.payment * ((1 + i) ** args.periods - 1) / (i * (1 + i) ** args.periods)
    principal = math.floor(P)
    print(f"Your loan principal = {principal}!")

#Q4
import math
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--type")
    parser.add_argument("--principal")
    parser.add_argument("--payment")
    parser.add_argument("--periods")
    parser.add_argument("--interest")
    args, _ = parser.parse_known_args()

    def to_float(v):
        try:
            return float(v) if v is not None else None
        except ValueError:
            return None

    def to_int(v):
        try:
            return int(v) if v is not None else None
        except ValueError:
            return None

    principal = to_float(args.principal)
    payment = to_float(args.payment)
    periods = to_int(args.periods)
    interest = to_float(args.interest)

    return args.type, principal, payment, periods, interest

def incorrect():
    print("Incorrect parameters")
    sys.exit()

def validate(type_, principal, payment, periods, interest):
    provided = sum(x is not None for x in [type_, principal, payment, periods, interest])
    if type_ not in ("annuity", "diff"):
        incorrect()
    if interest is None:
        incorrect()
    if provided < 4:
        incorrect()
    for v in [principal, payment, periods, interest]:
        if v is not None and v <= 0:
            incorrect()
    if type_ == "diff" and payment is not None:
        incorrect()

def ceil(x):
    return math.ceil(x - 1e-12)

def annuity_payment(principal, periods, i):
    return ceil(principal * i * (1 + i) ** periods / ((1 + i) ** periods - 1))

def annuity_periods(principal, payment, i):
    n = math.log(payment / (payment - i * principal), 1 + i)
    return ceil(n)

def annuity_principal(payment, periods, i):
    p = payment / (i * (1 + i) ** periods / ((1 + i) ** periods - 1))
    return math.floor(p)

def format_duration(months):
    years = months // 12
    rem = months % 12
    parts = []
    if years:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if rem:
        parts.append(f"{rem} month{'s' if rem > 1 else ''}")
    if not parts:
        parts.append("0 months")
    return " and ".join(parts)

_type, principal, payment, periods, interest = parse_args()
validate(_type, principal, payment, periods, interest)

i = interest / (12 * 100.0)

if _type == "diff":
    total = 0
    for m in range(1, periods + 1):
        d_m = principal / periods + i * (principal - (principal * (m - 1)) / periods)
        d_m = ceil(d_m)
        total += d_m
        print(f"Month {m}: payment is {int(d_m)}")
    overpayment = int(total - principal)
    print(f"\nOverpayment = {overpayment}")
else:
    missing = [principal is None, payment is None, periods is None].count(True)
    if missing != 1:
        incorrect()

    if payment is None:
        pay = annuity_payment(principal, periods, i)
        print(f"Your annuity payment = {int(pay)}!")
        overpayment = int(pay * periods - principal)
        print(f"Overpayment = {overpayment}")
    elif principal is None:
        p = annuity_principal(payment, periods, i)
        print(f"Your loan principal = {int(p)}!")
        overpayment = int(payment * periods - p)
        print(f"Overpayment = {overpayment}")
    else:
        n = annuity_periods(principal, payment, i)
        print(f"It will take {format_duration(n)} to repay this loan!")
        overpayment = int(payment * n - principal)
        print(f"Overpayment = {overpayment}")