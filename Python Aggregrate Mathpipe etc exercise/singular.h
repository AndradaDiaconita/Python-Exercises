#ifndef SINGULAR_H
#define SINGULAR_H


// TYPE IN UBUNTU!!!! gcc -Wall aggregate.c singular.c mathpipe.c -o mathpipe -lm
// RUN THIS FORMAT FOR ANSWER!!!! cat sample.txt | ./mathpipe sum -size=2



// The enum defines different types of filters that can be used.
// EQ represents equal, NEQ represents not equal, GEQ represents greater than or equal to,
// LEQ represents less than or equal to, LESS represents less than, and GREATER represents greater than.
enum filter_type
{


    EQ = 0,
    NEQ = 1,
    GEQ = 2,
    LEQ = 3,
    LESS = 4,
    GREATER = 5

    
};


// This function shifts the elements in a jagged array (an array of arrays) by a specified amount.
// It takes the jagged array, the sizeOf array (containing the sizeOf of each sub-array), the number of rows (sub-arrays), and the shift amount as parameters.
void shiftEl(double **jagarray, int *sizeOf, int numrows, double bys);

// This function filters the elements in a jagged array based on a specified filter and comparison value.
// It takes the filter type (enum), the jagged array, the sizeOf array, the number of rows (sub-arrays), and the comparison value as parameters.
void filterEl(enum filter_type filter, double **jagarray, int *sizeOf, int numrows, double comparison);

// This function prints the jagged array.
// It takes the jagged array, the sizeOf array, the number of rows (sub-arrays), and the precision as parameters.
void printJagArr(double **jagarray, int *sizeOf, int numrows, int prec);

// This ends the #ifndef directive.
#endif
