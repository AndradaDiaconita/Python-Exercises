#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include "aggregate.h"
#include "singular.h"


#define DEFAULT_PREC 5
#define MAX_SIZE 256




// TYPE IN UBUNTU!!!! gcc -Wall aggregate.c singular.c mathpipe.c -o mathpipe -lm
// RUN THIS FORMAT FOR ANSWER!!!! cat sample.txt | ./mathpipe sum -size=2


// Function to create a jagged array from values and sizeOf
double **createJagArr(double *values, int *sizeOf, int numrows);

// Function to find the size of a string
int FindSize(const char *str);

// Function to find the precision specified in the string
int FindPrecision(const char *str);



int main(int argumentMain, char *argumentArray[])
{
    // Buffer to store each line
    char line[MAX_SIZE];
    // Delimiter used to tokenize the line
    const char delimiter[] = " ";

    // Array to store values from input
    double *mathpipeArray = NULL;
    // Current size of the array
    int sizeOfArrayInitial = 0;

    // Array to store sizeOf of each row
    int *sizeOf = NULL;
    // Current number of rows
    int numRows = 0;



    // Read input lines until end of file
    while (fgets(line, MAX_SIZE, stdin) != NULL)
    {
        // Parse the string buffer and add values to the array
        // Record size of each row
        int rowSize = 0;



        // Tokenize the line using the delimiter
        char *tokensChar = strtok(line, delimiter);
        while (tokensChar != NULL)
        {
            // Convert tokensChar to a double value
            double value = strtod(tokensChar, NULL);
            // Resize the array
            mathpipeArray = realloc(mathpipeArray, (sizeOfArrayInitial + 1) * sizeof(double));
            // Add value to the array
            mathpipeArray[sizeOfArrayInitial++] = value;
            // Get the next tokensChar
            tokensChar = strtok(NULL, delimiter);
            // Increment row size
            rowSize++;
        }

        sizeOf = realloc(sizeOf, (numRows + 1) * sizeof(double));
        sizeOf[numRows++] = rowSize;
    }


    // Print error message and end the program if the file is empty
    if (mathpipeArray == NULL)
    {
        fprintf(stderr, "FATAL ERROR in line 45!!\n");
        return 1;
    }







    // Extract size, precision, and function name from user's inputs
    int prec;
    char function[5];

    int userSize = sizeOf[0];

    int userPrec = DEFAULT_PREC;

    bool shiftOf = false;
    bool prints = false;
    
    double bys;
    bool filter = false;

    char filterType[7];
    double comparisons;



    for (int i = 0; i < argumentMain; i++)
    {
        // Find the string that contains the size
        const char *substring = strstr(argumentArray[i], "size");
        if (substring != NULL)
        {
            // Find the position of the character "="
            const char *equal_sign = strchr(substring, '=');
            if (equal_sign != NULL)
            {
                // Extract the substring after the "=" character
                const char *size_string = equal_sign + 1;

                // Convert the substring to an integer to get size inputted by user
                userSize = atoi(size_string);
            }
        }



        // Find the precision specified in the argument
        prec = FindPrecision(argumentArray[i]);
        if (prec != -1)
        {
            userPrec = prec;
        }


        // Perform case-insensitive check on the function name inputted by the user
        // Convert the function name to uppercase
        if (strcasecmp(argumentArray[i], "COUNT") == 0 || strcasecmp(argumentArray[i], "MIN") == 0 || strcasecmp(argumentArray[i], "MAX") == 0 || strcasecmp(argumentArray[i], "SUM") == 0 || strcasecmp(argumentArray[i], "AVG") == 0 || strcasecmp(argumentArray[i], "PAVG") == 0)
        {
            strcpy(function, argumentArray[i]);
            for (int j = 0; j < strlen(function); j++)
            {
                function[j] = toupper(function[j]);
            }
        }
       
        // Check if SHIFT argument is present
        if (strcasecmp(argumentArray[i], "SHIFT") == 0)
        {
            shiftOf = true;
            bys = strtod(argumentArray[i + 1], NULL);
        }



        // Check if PRINT argument is present
         if (strcasecmp(argumentArray[i], "PRINT") == 0)
        {
            prints = true;
        }



        // Record the filter type and value
        if (strcasecmp(argumentArray[i], "FILTER") == 0)
        {
            filter = true;
            int hasDigit = 0;

            for (int j = 0; argumentArray[i + 1][j] != '\0'; j++)
            {
                if (isdigit(argumentArray[i + 1][j]))
                {
                    hasDigit = 1;
                    break;
                }
            }


            if (hasDigit)
            {
                comparisons = strtod(argumentArray[i + 1], NULL);
                strcpy(filterType, argumentArray[i + 2]);
            }

            else
            {
                comparisons = strtod(argumentArray[i + 2], NULL);
                strcpy(filterType, argumentArray[i + 1]);
            }
        }
    }

    // prints error message and end program if user inputs a non-positive size
    if (userSize <= 0)
    {
        fprintf(stderr, "FATAL ERROR! in line 74!!!\n");
        return 1;
    }







    // Array to store adjusted row sizeOf
    int *newSize = NULL;
    // Number of adjusted rows
    int newRows = 0;

    for (int i = 0; i < numRows; i++)
    {

        while (sizeOf[i] > userSize)
        {
            // Resize the newSize array
            newSize = realloc(newSize, (newRows + 1) * sizeof(int));
            // Add userSize to newSize array
            newSize[newRows++] = userSize;
            // Decrease sizeOf[i] by userSize
            sizeOf[i] -= userSize;
        }



        // Resize the newSize array
        newSize = realloc(newSize, (newRows + 1) * sizeof(int));

        // Add sizeOf[i] to newSize array
        newSize[newRows++] = sizeOf[i];


    }

    // Create the jagged array
    double **jagarray = createJagArr(mathpipeArray, newSize, newRows);









    // Execute the input's request
    aggregate(function, jagarray, newSize, newRows, userPrec);

    if (prints == true)
    {
        printJagArr(jagarray, newSize, newRows, userPrec);
    }

    if (shiftOf == true)
    {
        shiftEl(jagarray, newSize, newRows, bys);
        printJagArr(jagarray, newSize, newRows, userPrec);
    }

    enum filter_type value;


    if (filter == true)
    {
        if (strcasecmp(filterType, "EQ") == 0)

        {
            value = EQ;
        }
        


        else if (strcasecmp(filterType, "GEQ") == 0)

        {
            value = GEQ;
        }



        else if (strcasecmp(filterType, "LEQ") == 0)

        {
            value = LEQ;
        }



        else if (strcasecmp(filterType, "NEQ") == 0)

        {
            value = NEQ;
        }



        else if (strcasecmp(filterType, "GREATER") == 0)

        {
            value = GREATER;
        }



        else if (strcasecmp(filterType, "LESS") == 0)

        {
            value = LESS;
        }




        filterEl(value, jagarray, newSize, newRows, comparisons);


        printJagArr(jagarray, newSize, newRows, userPrec);

    }

    // Free the allocated memory
    for (int i = 0; i < newRows; i++)

    {
        free(jagarray[i]);
    }



    return 0;

}






int FindPrecision(const char *str)
{
    // Check if the string contains the substring "size"
    const char *substring = strstr(str, "prec");
    if (substring != NULL)

    {

        // Find the position of the character "="
        const char *equal_sign = strchr(substring, '=');
        if (equal_sign != NULL)

        {
            // Extract the substring after the "=" character
            const char *size_string = equal_sign + 1;

            // Convert the substring to an integer
            int prec = atoi(size_string);
            return prec;
        }


    }



    // Return a default value if the substring "size" is not found
    return -1;
}


double **createJagArr(double *values, int *sizeOf, int numrows)
{
    // Position of the value array
    int k = 0;

    // Declare the array of pointers for the rows
    double **jagarray = malloc(numrows * sizeof(double *));

    // Iterate over each row
    for (int i = 0; i < numrows; i++)

    {
        // Allocate memory for the current row based on its size
        jagarray[i] = malloc(sizeOf[i] * sizeof(double));

        // Copy values from the array of values to the current row
        for (int j = 0; j < sizeOf[i]; j++)

        {
            jagarray[i][j] = values[k];
            k++;
        }


    }



    return jagarray;
}

