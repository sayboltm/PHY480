#include <stdio.h>

int main()
{
    int var; // Define an integer variable var
    int *p; // Define a pointer to an integer
    p = &var; // Extract the address of var
    var = 421; // Change content of var
    printf("Address of integer variable var : %p\n", &var);
    printf("Its value: %d\n", var); // 421
    printf("Value of integer pointer p : %p\n", p); // = &var
// The content of the variable pointed to by p is *p
    printf("The value p points at : %d\n", *p);
// Address where the pointer is stored in memory
    printf("Address of the pointer p : %p\n", &p);
    return 0;
}