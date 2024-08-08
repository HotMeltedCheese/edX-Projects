#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //check to see if file was attached
    if(argc == 1)
    {
        printf("File Not Found");
        return 1;
    }

    //opens the image file
    FILE *file = fopen(argv[1], "r");

    //check to see if file exists
    if(file == NULL)
    {
        printf("File doesn't exist");
        return 2;
    }

    //reassigns the name of unit8_t to BYTE
    typedef uint8_t BYTE;

    //create a buffer that will store the information read
    BYTE *buffer = malloc(512 * sizeof(BYTE));

    //create a pointer that points to the file the image is going to be stored in
    FILE *img = NULL;

    //creates a pointer that will store the file name
    char *filename = malloc(sizeof(char) * 8);

    //creates a int that will store the amount of images accessed.
    int img_counter = 0;

    //reads the file until the end is reached
    while(fread(buffer, 1, 512, file) == 512)
    {
        //if the start of the new file is opened either open a new file
        //or open a new file and close the old one
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if there are no files open the first file
            if(img_counter == 0)
            {
                sprintf(filename, "%03i.jpg", img_counter);
                img = fopen(filename, "w");
            }
            //if a file is already opened close the old file and open a new file
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", img_counter);
                img = fopen(filename, "w");
            }
            img_counter++;
        }
        //if there is a open file write the information to the new file.
        if(img_counter > 0)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    //close the last file after end of file is reached
    fclose(img);

    //free memory
    free(buffer);
    free(filename);
    fclose(file);

    //return 0 to indicate that the program was successful
    return 0;
}