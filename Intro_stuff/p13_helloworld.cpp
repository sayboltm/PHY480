// Hello world code with exception handling
using namespace std;
#include <cstdlib>
#include <cmath>
#include <iostream>
int main (int argc, char* argv[])
{
// Read in output file, abort if there are too few command-line arguments
    if( argc <= 1 ){
        cout << "Bad Usage: " << argv[0] <<
        " read also a number on the same line, e.g., prog.exe 0.2" << endl;
        exit(1); // here the program stops.
}
// convert the text argv[1] to double using atof:
    double r = atof(argv[1]);
    double s = sin(r);
    cout << "Hello, World! sin(" << r << ")=" << s << endl;
// success
    return 0;
}