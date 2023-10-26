from math import ceil, log
import argparse
from sys import argv

MONTHS_IN_YEAR = 12
TYPE_DIFF = "diff"
TYPE_ANNUITY = "annuity"


def get_periods_text(p: int) -> str:
    years = p // MONTHS_IN_YEAR
    months = p % MONTHS_IN_YEAR
    years_plural = years > 1
    months_plural = months > 1
    return "{y}{yend}{u}{m}{mend}".format(
        y=str(years) + " year" if years > 0 else '',
        yend="s" * years_plural,
        u=" and " if years > 0 and months > 0 else '',
        m=str(months) + " month" if months > 0 else '',
        mend="s" * months_plural)


def calc_xx(n, p):
    x = (1 + n) ** p
    return n * x / (x - 1)


def arg_to_float(a):
    return float(a) if a is not None else 0.0


def check_non_negative(lst):
    return all(num >= 0 for num in lst)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--payment")
    parser.add_argument("--principal")
    parser.add_argument("--periods")
    parser.add_argument("--interest")
    args = parser.parse_args()

    payment = arg_to_float(args.payment)
    principal = arg_to_float(args.principal)
    periods = arg_to_float(args.periods)
    interest = arg_to_float(args.interest)
    nominal = interest / (MONTHS_IN_YEAR * 100)
    sum_of_payments = 0
    overpayment = 0

    # args checks for valid values
    if (args.type not in [TYPE_DIFF, TYPE_ANNUITY] or
            args.type == "diff" and args.payment is not None or
            args.interest is None or
            len(argv) < 5 or
            not check_non_negative([payment, principal, periods, interest])):
        print("Incorrect parameters")
        return

    if args.type == TYPE_DIFF:
        for i in range(int(periods)):
            payment = ceil(principal / periods + nominal * (principal - (principal * i / periods)))
            sum_of_payments += payment
            print(f"Month {i+1}: payment is {payment}")

        overpayment = sum_of_payments - principal
    else:
        if args.payment is None:
            payment = ceil(principal * calc_xx(nominal, periods))
            print(f"Your monthly payment = ", payment, "!", sep='')
        elif args.principal is None:
            principal = ceil(payment / calc_xx(nominal, periods))
            print("Your loan principal = ", principal, "!", sep='')
        else:
            periods = ceil(log(payment / (payment - nominal * principal), 1 + nominal))
            print("It will take", get_periods_text(periods), "to repay this loan!")

        overpayment = periods * payment - principal

    print()
    print("Overpayment =", ceil(overpayment))


if __name__ == "__main__":
    main()
