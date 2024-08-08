#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //going to store the average RGB value of the pixel in average
    //total is going to store the total value of all RGB values
    double average_BGR = 0.0;
    int total_BGR = 0;
    int rounded_BGR = 0;

    //goes through the entire heigth of the picture
    for(int row = 0; row < height; row++)
    {
        //goes through the entire width of the picture
        for(int column = 0; column < width; column++)
        {
            //find the total RGB value and then divide by 3 to find average
            total_BGR = image[row][column].rgbtBlue + image[row][column].rgbtGreen + image[row][column].rgbtRed;
            average_BGR = total_BGR/3.0;
            rounded_BGR = average_BGR + 0.5;

            //set RGB value of pixel to average value to grey scale it
            image[row][column].rgbtRed = rounded_BGR;
            image[row][column].rgbtGreen = rounded_BGR;
            image[row][column].rgbtBlue = rounded_BGR;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //creates the vaules that will store the values sepia
        double sepia_red = 0.0;
        double sepia_blue = 0.0;
        double sepia_green = 0.0;

    //creates the values that will store the rounded verison of the sepia
    int rounded_red = 0;
    int rounded_blue = 0;
    int rounded_green = 0;

    //goes through the entire height of the picture
    for(int row = 0; row < height; row++)
    {
        //goes through the entire width of picture
        for(int column = 0; column < width; column++)
        {
            //set the values of the intergers back to zero
            sepia_red = 0.0;
            sepia_blue = 0.0;
            sepia_green = 0.0;

            rounded_red = 0;
            rounded_blue = 0;
            rounded_green = 0;
            //caluclate the values that created the sepia
            sepia_red = .393 * image[row][column].rgbtRed + .769 * image[row][column].rgbtGreen + .189 * image[row][column].rgbtBlue;
            sepia_blue = .272 * image[row][column].rgbtRed + .534 * image[row][column].rgbtGreen + .131 * image[row][column].rgbtBlue;
            sepia_green = .349 * image[row][column].rgbtRed + .686 * image[row][column].rgbtGreen + .168 * image[row][column].rgbtBlue;

            //if the value is greater than 255 round down to 255
            if(sepia_red > 255)
            {
                sepia_red = 255;
            }
            if(sepia_blue > 255)
            {
                sepia_blue = 255;
            }
            if(sepia_green > 255)
            {
                sepia_green = 255;
            }

            //rounds the sepia value to the nearest interger
            rounded_red = sepia_red + 0.5;
            rounded_blue = sepia_blue + 0.5;
            rounded_green = sepia_green + 0.5;

            // sets the RGB values of the pixels to the sepia values
            image[row][column].rgbtRed = rounded_red;
            image[row][column].rgbtBlue = rounded_blue;
            image[row][column].rgbtGreen = rounded_green;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //going to store the rgb value of a pixel when swapping
    int tgreen = 0;
    int tred = 0;
    int tblue = 0;

    //stores the pixel on the opposite side
    int os = 0;

    //get half of the width of the image and rounds it
    double half_width = width / 2;
    int rounded_width = width + 0.5;

    //goes through the height of the picture
    for(int row = 0; row < height; row++)
    {
        os = width - 1;
        //goes through each row the pictrue
        for(int column = 0; column < half_width; column++)
        {
            //if trying to swap the same pixel break the loop
            if(os == column)
            {
                break;
            }

            //stores the rgb values of the pixel so when swapped not lost
            tgreen = image[row][column].rgbtGreen;
            tred = image[row][column].rgbtRed;
            tblue = image[row][column].rgbtBlue;

            //sets the current pixel RGB value to the pixel that is on the opposite side
            image[row][column].rgbtGreen = image[row][os].rgbtGreen;
            image[row][column].rgbtRed = image[row][os].rgbtRed;
            image[row][column].rgbtBlue = image[row][os].rgbtBlue;

            //sets the opposite sied pixel RGB to the current pixels old value
            image[row][os].rgbtGreen = tgreen;
            image[row][os].rgbtRed = tred;
            image[row][os].rgbtBlue = tblue;

            //move on to the next pixel
            os--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //creates a 2d array that will store the blurred pixels
    RGBTRIPLE copy[height][width];

    int sph = -1;
    int spv = -1;

    int total_red;
    int total_blue;
    int total_green;

    double average_red;
    double average_blue;
    double average_green;

    int rounded_red;
    int rounded_blue;
    int rounded_green;

    int counter;

    for(int row = 0; row < height; row++)
    {
        for(int column = 0; column < width; column++)
        {
            //set the values back to 0
            total_red = 0;
            total_blue = 0;
            total_green = 0;
            counter = 0;

            //make a copy of the current pixel so it is not lost
            copy[row][column].rgbtBlue = image[row][column].rgbtBlue;
            copy[row][column].rgbtGreen = image[row][column].rgbtGreen;
            copy[row][column].rgbtRed = image[row][column].rgbtRed;
            for(int current_row = 0; current_row < 3; current_row++)
            {
                for(int current_column = 0; current_column < 3; current_column++)
                {
                    //if we are past the bit map break the loop since there is nothing left
                    if(column + sph > width - 1)
                    {
                        break;
                    }

                    //if we are before the bit map starts then add one then move on the next pixel
                    if(column + sph < 0)
                    {
                        sph++;
                        continue;
                    }

                    //if we are getting rgb values from perivous pixels use the copy
                    if((row + current_row) < row || ((row + current_row) == row && (column + sph) < column))
                    {
                        total_blue = total_blue + copy[row + spv][column + sph].rgbtBlue;
                        total_green = total_green + copy[row + spv][column + sph].rgbtGreen;
                        total_red = total_red + copy[row + spv][column + sph].rgbtRed;
                        counter++;
                        continue;
                    }

                    total_blue = total_blue + image[row + spv][column + sph].rgbtBlue;
                    total_green = total_green + image[row + spv][column + sph].rgbtGreen;
                    total_red = total_red + image[row + spv][column + sph].rgbtRed;
                    counter++;
                }
                spv++;
            }
            average_red = total_red/counter;
            average_blue = total_blue/counter;
            average_green = total_green/counter;

            rounded_red = average_red + 0.5;
            rounded_blue = average_blue + 0.5;
            rounded_green = average_green + 0.5;

            image[row][column].rgbtRed = rounded_red;
            image[row][column].rgbtBlue = rounded_blue;
            image[row][column].rgbtGreen = rounded_green;
        }
    }
}

