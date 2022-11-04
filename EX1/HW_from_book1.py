
def zan_valzan():
    num = input("please enter 5 digits number\n")
    print_num_values(num)


def print_num_values(num):
    print("you entered number:", num)
    print("the digits of that number are:", end="")
    temp = 0
    for digit in num:
        print(digit, end=",")
        temp += int(digit)
    print("\nthe sum is:", temp)


def is_valid():
    num = ""
    while not num.isnumeric() or len(num) != 5:
        num = input("please enter 5 digits number\n")
    return num


def de_zavu():
    num = is_valid()
    print_num_values(num)
