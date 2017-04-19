#include <iostream>
#include <string>

using namespace std;

int main() 
{

int i = 0;

cout << "Printing forward loop" << endl;

int n = 10;

for (int i=1; i < n; i++)
	{
		string output = to_string(i);
		cout << output << endl;
	}

cout << "Printing backward loop" << endl;

for (int i = n; i > 1; i--)
	{
		string output = to_string(i);
		cout << output << endl;
	}

return 0;
}
