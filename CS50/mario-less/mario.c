#include <cs50.h>
#include <stdio.h>

//prints bricks out
//takes in space which is the amount of space between the start and the first brick
//takes in the amount of bricks that should be printed out after the space
void print_bricks(int space, int bricks);

int main(void)
{
    //asks the user for the height of the structure and that the number is between 1 and 8
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while(height < 1 || height > 8);

    //stores the amount of space between the start and the first brick
    int space = height - 1;

    //stores the amonut of bricks that should be printed
    int bricks = 1;

    //prints out the structure requested
    for(int i = 0; i < height; i++)
    {
        //prints out bricks
        print_bricks(space, bricks);
        //print out the next line
        printf("\n");
        //reduce the amount of space by one
        space--;
        //increase the amount of bricks printed out
        bricks++;
    }

    //return 0 to indicate that the program was successful
    return 0;
}

void print_bricks(int space, int bricks)
{
    //prints out spaces
    for(int i = 0; i < space; i++)
    {
        printf(" ");
    }

    //prints out bricks
    for(int i = 0; i < bricks; i++)
    {
        printf("#");
    }
}
