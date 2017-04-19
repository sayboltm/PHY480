#include <iostream>
#include <fstream>
#include <iomanip> 
#include <cmath>    //  Mathematical functions like sin, cos etc
#include <string>   //  what does this mean? 
// use namespace for output and input
using namespace std;  // Why namespace? 

// object for output files, for input files use ifstream
ofstream ofile;
// Functions used, why is this an inline function?
inline double f(double x){return 100.0*exp(-10.0*x);
}
inline double exact(double x) {return 1.0-(1-exp(-10))*x-exp(-10*x);}

// Begin main program
int main(int argc, char *argv[]){
  int exponent; 
  string filename; //  This is a useful way to define a text string, alternatively you can use characters
    // We read also the basic name for the output file and the highest power of 10^n we want
    if( argc <= 1 ){
          cout << "Bad Usage: " << argv[0] <<
              " read also file name on same line and max power 10^n" << endl;
          exit(1);
    }
        else{
        filename = argv[1]; // first command line argument after name of program
        exponent = atoi(argv[2]);
    }

    /*  Many lines of comments start like this
    // Loop over powers of 10
    for (int i = 1; i <= exponent; i++){
      int  n = (int) pow(10.0,i);
      // Declare new file name
      string fileout = filename;
      // Convert the power 10^i to a string
      string argument = to_string(i);
      // Final filename as filename-i-
      fileout.append(argument);

      //   To be filled inn during lab session



      ofile.open(fileout);
      ofile << setiosflags(ios::showpoint | ios::uppercase);
      //      ofile << "       x:             approx:          exact:       relative error" << endl;
      for (int i = 1; i < n;i++) {
	double xval = x[i];
 	 double RelativeError = fabs((exact(xval)-solution[i])/exact(xval));
         ofile << setw(15) << setprecision(8) << xval;
         ofile << setw(15) << setprecision(8) << solution[i];
         ofile << setw(15) << setprecision(8) << exact(xval);
         ofile << setw(15) << setprecision(8) << log10(RelativeError) << endl;
      }
      ofile.close();
      delete [] x; delete [] d; delete [] b; delete [] solution;
    }
    */  //  End of long set of comments
    return 0;   // returns zero upon success
}


