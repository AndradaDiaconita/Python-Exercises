#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <float.h>
#include <string.h>
#include "singular.h"


// TYPE IN UBUNTU!!!! gcc -Wall aggregate.c singular.c mathpipe.c -o mathpipe -lm
// RUN THIS FORMAT FOR ANSWER!!!! cat sample.txt | ./mathpipe sum -size=2



void printJagArr(double **jagarray, int *sizeOf, int numrows, int prec)
{
    // Iterate over each row
    for (int i = 0; i < numrows; i++)
    {
        // Check if the size of the current row is greater than 0
        if (sizeOf[i] > 0)
        {
            // Print the elements of the current row
            for (int j = 0; j < sizeOf[i]; j++)
            {
                // Check if the size of the current row is 0 and break the loop if so
                if (sizeOf[i] == 0)
                {
                    break;
                }

                // Check the precision value to determine the format of printing
                if (prec == 0)
                {
                    // Print the element with no decimal places
                    printf("%.0f ", ceil(jagarray[i][j]));
                    // Check if there are more rows to print and add a space if needed
                    if (i < numrows - 1)
                    {
                        printf(" ");
                    }
                }
                else
                {
                    // Print the element with the specified precision
                    printf("%.*f ", prec, jagarray[i][j]);
                    // Check if there are more rows to print and add a space if needed
                    if (i < numrows - 1)
                    {
                        printf(" ");
                    }
                }
            }
            printf("\n"); // Print a new line after printing each row
        }
    }
}

void filterEl(enum filter_type filter, double **jagarray, int *sizeOf, int numrows, double comparison)
{

    // Iterate over each row
    for (int i = 0; i < numrows; i++)
    {
        // Index for writing the modif. values
        int index = 0;

        // Iterate over the elements of the current row
        for (int j = 0; j < sizeOf[i]; j++)
        {
            // Check the filter type
            switch (filter)
            {
            case EQ:
                // Check if the current el is equal to the given value
                if (jagarray[i][j] == comparison)
                {
                    // Keep the value by changing it to the modif array
                    jagarray[i][index] = jagarray[i][j];
                    index++;
                }
                break;
            case NEQ:
                // Check if the current element is not equal to the provided value
                if (jagarray[i][j] != comparison)
                {
                    jagarray[i][index] = jagarray[i][j];
                    index++;
                }
                break;

            case LEQ:
                 // Check if the current element is less than or equal to the provided value
                if (jagarray[i][j] <= comparison)
                {
                    jagarray[i][index] = jagarray[i][j];
                    index++;
                }
                break;

            case GEQ:
                // Check if the current element is greater than or equal to the provided value
                if (jagarray[i][j] >= comparison)
                {
                    jagarray[i][index] = jagarray[i][j];
                    index++;
                }
                break;
           
           case GREATER:
                // Check if the current element is greater than the provided value
                if (jagarray[i][j] > comparison)
                {
                    jagarray[i][index] = jagarray[i][j];
                    index++;
                }
                break;

            case LESS:
                // Check if the current element is less than the provided value
                if (jagarray[i][j] < comparison)
                {
                    jagarray[i][index] = jagarray[i][j];
                    index++;
                }
                break;
            
            }
        }

        // Update the size of the row to the number of modified values
        sizeOf[i] = index;
    }
}


void shiftEl(double **jagarray, int *sizeOf, int numrows, double bys)
{
    // Iterate over each row
    for (int i = 0; i < numrows; i++)
    {
        // Iterate over the elements of the current row
        for (int j = 0; j < sizeOf[i]; j++)
        {
            // Shift the element by the specified amount
            jagarray[i][j] += bys;
        }
    }
}




