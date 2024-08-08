#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //setting up variables
    int check = 0;
    int check2 = 0;
    long num;
    int num3 = 0;
    int num2 = 0;
    int counter = 0;

// get the users credit card number
    num = get_long("Credit Card info: ");

//check if the number is valid
    for(int i = 0; i < 16; i++)
    {
        num2  = num%10;
        num = ((num - num2)/10);
//adding the even numbers to the check
        if(counter%2 == 0)
        {
            check = check + num2;
        }
        else
        {
            num2 = num2 * 2;
            if(num2 > 10)
            {
                check2 = check2 + (num2%10);
                check2 = check2 + ((num2 - (num2%10))/10);
            }
            else
            {
                check2 = check2 + num2;
            }
        }
        counter = counter + 1;
    }
    check2 = check2 + check;

//if the credit card number is vaild then say so and if not say that it isn't
    if(check2%10 == 0)
    {
        printf("Vaild \n");
    }
    else
    {
        printf("Invaild \n");
    }
}
