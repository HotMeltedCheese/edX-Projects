from cs50 import get_int
from sys import exit

def main():
    #get the users credit card number
    card_number = get_int("Number: ")
    #get the length of the credit card number
    numlen = len(str(card_number))
    #check if the credit card number is vaild
    vaild = card_vaild(card_number, numlen)
    #if the credit card number is not vaild then say invaild
    print(vaild)
    if not vaild:
        print("INVALID")
    elif numlen == 15:
        print("AMEX")
    elif numlen == 16:
        if((int)(card_number / 100000000000000)) in [51,52,53,54,55]:
            print("MASTERCARD")
        else:
            print("VISA")
    else:
        print("VISA")


#takes in the credit card number and the length of the credit card number
#return a boolean stating whether the credit card number is vaild or not.
def card_vaild(number, numlen):
    #store the value of the current number
    modvalue = 0
    #store the total of the numbers
    total = 0
    if numlen not in [13, 15, 16]:
        return False
    for i in range(numlen):
        modvalue = number % 10
        #add every number starting from the first digit and increasing by increments of 2 each time
        if(i % 2) == 0:
            print(f"gfirst {modvalue}")
            total = total + modvalue
        #add every number times 2 starting from the second digit increasing by increments of 2 each time
        else:
            modvalue = modvalue * 2
            #adds only one part of the interger at a time
            while modvalue != 0:
                total = total + (modvalue % 10)
                print(modvalue % 10)
                modvalue = (int)(modvalue / 10)
        #move onto the next number in the card number
        number = (int)(number/10)
    #if the total is 20 return true as the card number is vaild else return false
    print(total)
    if total == 20:
        return True
    return False


main()