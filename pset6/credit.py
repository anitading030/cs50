from cs50 import get_int, get_string
import re


def main():
    while True:
        card = get_string("Card number: ")
        if int(card) > 0:
            break

    sum1 = 0
    sum2 = 0
    reverse = card[len(card)::-1]
    for i in str(reverse)[1::2]:
        sum1 += int(i) * 2 % 10 + int(int(i) * 2 / 10)

    for j in str(reverse)[0::2]:
        sum2 += int(j)

    check_digit = sum1 + sum2

    if check_digit % 10 == 0:
        if len(card) == 15 and re.search("^3(4|7)", card):
            print("AMEX")
        elif len(card) == 16 and re.search("^5(1|2|3|4|5)", card):
            print("MASTERCARD")
        elif (len(card) == 13 or len(card) == 16) and re.search("^4", card):
            print("VISA")
        else:
            print("INVALID")

    else:
        print("INVALID")


main()
