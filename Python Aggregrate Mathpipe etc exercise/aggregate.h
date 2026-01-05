#ifndef AGGREGATE_H
#define AGGREGATE_H


// TYPE IN UBUNTU!!!! gcc -Wall aggregate.c singular.c mathpipe.c -o mathpipe -lm
// RUN THIS FORMAT FOR ANSWER!!!! cat sample.txt | ./mathpipe sum -size=2




// Function declaration for the aggregate function
void aggregate(const char *function, double **jagarray, int *sizeOf, int numrows, int prec);



#endif
