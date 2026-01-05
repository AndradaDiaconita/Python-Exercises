#include <float.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "aggregate.h"


// TYPE IN UBUNTU!!!! gcc -Wall aggregate.c singular.c mathpipe.c -o mathpipe -lm
// RUN THIS FORMAT FOR ANSWER!!!! cat sample.txt | ./mathpipe sum -size=2




// Function to count the number of elements in each row of jagged array
static int *countEl(double **jagarray, int *sizeOf, int theRows)


{

    // Allocate memory for the siz of the array
    int *MainArray = malloc(theRows * sizeof(int));

    // Iterate over each row
    for (int i = 0; i < theRows; i++)
    {
        MainArray[i] = sizeOf[i];
    }

    return MainArray;

}



// Function to calculate the sum of elements in each row of jagged array
static double *Sum(double **jagarray, int *sizeOf, int theRows)

{

    // Allocate memory for the sum array
    double *MainArray = malloc(theRows * sizeof(double));

    // Iterate over each row
    for (int i = 0; i < theRows; i++)
    {
        // Iterate over the elements of the current row
        for (int j = 0; j < sizeOf[i]; j++)
        {
            // Add the element to the sum
            MainArray[i] += jagarray[i][j];
        }
    }

    return MainArray;

}



// Function to find the minimum element in each row of jagged array
static double *MinWhere(double **jagarray, int *sizeOf, int theRows)

{
    // Allocate memory for the minimum of the array
    double *MainArray = malloc(theRows * sizeof(double));

    // Iterate over each row
    for (int i = 0; i < theRows; i++)
    {
        // Make the minimum value become the max value possible
        double min = DBL_MAX;

        // Find the minimum element in the current row
        // Iterate over the elements of the current row
        for (int j = 0; j < sizeOf[i]; j++)
        {
            if (jagarray[i][j] < min)
            {
                min = jagarray[i][j];
            }
        }

        // Store the minimum value in the smallest min array
        MainArray[i] = min;
    }

    return MainArray;

}



// Function to find the maximum element in each row of jagged array
static double *MaxWhere(double **jagarray, int *sizeOf, int theRows)

{
    // Allocate memory for the maximums array
    double *MainArray = malloc(theRows * sizeof(double));

    // Iterate over each row
    for (int i = 0; i < theRows; i++)
    {
        // Initialize the maximum value to the most minimum possible value
        double max = DBL_MIN;

        // Find the maximum element in the current row
        for (int j = 0; j < sizeOf[i]; j++)
        {
            if (jagarray[i][j] > max)
            {
                max = jagarray[i][j];
            }
        }

        // Store the maximum value in the maximums array
        MainArray[i] = max;
    }

    return MainArray;

}



// Function to calculate the pseudo average of minimum and maximum values in each row of jagged array
static double *PseuAve(double *min, double *max, int theRows)

{
    // Allocate memory for the pseudo array
    double *MainArray = malloc(theRows * sizeof(double));

    // Iterate over each row
    for (int i = 0; i < theRows; i++)
    {
        // Calculate the pseudo average
        MainArray[i] = (max[i] + min[i]) / 2;
    }
    return MainArray;

}



// Function to calculate the average of elements in each row of jagged array
static double *Aver(double *sum, int *sizeOf, int theRows)

{
    // Allocate memory for the averages array
    double *MainArray = malloc(theRows * sizeof(double));

    // Iterate over each row
    for (int i = 0; i < theRows; i++)
    {
        // Calculate the average by dividing the sum by the size of the row
        MainArray[i] = sum[i] / sizeOf[i];
    }
    return MainArray;

}





// Main aggregate function
void aggregate(const char *function, double **jagarray, int *sizeOf, int theRows, int prec)

{


    if (strcmp(function, "COUNT") == 0)
    {
        // Call the countEl function to get the array of element counts
        int *MainArray = countEl(jagarray, sizeOf, theRows);
        
        // Print the element counts
        for (int i = 0; i < theRows; i++)
        {
            printf("%d ", MainArray[i]);
        }
        printf("\n");

        // Free the memory allocated for the array
        free(MainArray);
    }




    else if (strcmp(function, "MAX") == 0)
    {
        // Call the MaxWhere function to get the array of maximum values
        double *MainArray = MaxWhere(jagarray, sizeOf, theRows);

        // Print the maximum values
        for (int i = 0; i < theRows; i++)
        {
            if (prec == 0)
            {
                printf("%.0f", ceil(MainArray[i]));
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
            else
            {
                printf("%.*f", prec, MainArray[i]);
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
        }
        printf("\n");

        // Free the memory allocated for the array
        free(MainArray);
    }




    else if (strcmp(function, "MIN") == 0)
    {
        // Call the MinWhere function to get the array of minimum values
        double *MainArray = MinWhere(jagarray, sizeOf, theRows);

        // Print the minimum values
        for (int i = 0; i < theRows; i++)
        {
            if (prec == 0)
            {
                printf("%.0f", ceil(MainArray[i]));
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
            else
            {
                printf("%.*f", prec, MainArray[i]);
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
        }
        printf("\n");

        // Free the memory allocated for the array
        free(MainArray);
    }





    else if (strcmp(function, "AVG") == 0)
    {

        // Call the Sum function to get the array of sums
        double *thearray = Sum(jagarray, sizeOf, theRows);

        // Call the Aver function to get the array of averages
        double *MainArray = Aver(thearray, sizeOf, theRows);


        // Print the averages
        for (int i = 0; i < theRows; i++)
        {
            if (prec == 0)
            {
                printf("%.0f", ceil(MainArray[i]));
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
            else
            {
                printf("%.*f", prec, MainArray[i]);
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
        }



        printf("\n");



        // Free the memory allocated for the arrays
        free(thearray);
        free(MainArray);
    }





    else if (strcmp(function, "SUM") == 0)
    {

        // Call the Sum function to get the array of sums
        double *MainArray = Sum(jagarray, sizeOf, theRows);


        // Print the sums
        for (int i = 0; i < theRows; i++)
        {
            if (prec == 0)
            {
                printf("%.0f", ceil(MainArray[i]));
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
            else
            {
                printf("%.*f", prec, MainArray[i]);
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
        }


        printf("\n");
        free(MainArray);
    }




    else if (strcmp(function, "PAVG") == 0)
    {
        // Call the MinWhere function to get the array of minimum values
        double *thearray = MinWhere(jagarray, sizeOf, theRows);

        // Call the MaxWhere function to get the array of maximum values
        double *secondarray = MaxWhere(jagarray, sizeOf, theRows);

        // Call the PseuAve function to get the array of pseudo averages
        double *MainArray = PseuAve(thearray, secondarray, theRows);


        // Print the pseudo averages
        for (int i = 0; i < theRows; i++)
        {
            if (prec == 0)
            {
                printf("%.0f", ceil(MainArray[i]));
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
            else
            {
                printf("%.*f", prec, MainArray[i]);
                if (i < theRows - 1)
                {
                    printf(" ");
                }
            }
        }


        printf("\n");


        // Free the memory allocated for the arrays
        free(thearray);
        free(secondarray);
        free(MainArray);
    }

    
}