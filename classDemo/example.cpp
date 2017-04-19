#include <iostream>

class Complex
	{
	private:
		//Private stuff, can access with friend functions from outside
		double real, imag;
	public:
		//Public stuff
		//
	//Need constructor,destructor (when init this will create)
	//Constructor: function same name as class
		Complex();
		Complex(double);
		Complex(double,double);
		~Complex(){}; //Don't need to do anything
		// make malloc const/destructor thing
	//Define print function inside class
	void print();
	
	//Can overload operators
	Complex operator+(Complex,Complex);

	}number,optionalcomplexclassdelcarations;

//Some constructors
Complex::Complex(){
	real=0.0;
	imag=0.0;
}

Complex::Complex(double re){
	real=re;
	imag=0.0;
}

//Init whole shit give 2 niumbers
Complex::Complex(double re, double im){
	real=re;
	imag=im;
}

void Complex::print(){
	std::cout << "(" << real << "," << imag << ")" << std::endl;
}

Complex operator+(Complex a, Complex b){
	return Complex(a.real + b.real, a.imag + b.imag);
}
//Destructor
//Complex::~Complex(){}; //Define here or within

int main(int argc, char*argv[]){
	double real, imag;

	//ask for input
	std::cout << "Real: ";
	std::cin >> real;
	std::cout << "Imaginary: ";
	std::cin >> imag;

	Complex number1; //Init from 1st constructor, none given
	Complex number2(real); //2nd one, because 1 double input
	Complex number3(real,imag);
	Complex number4 = number2 + number3;

	// Wont work because private
	//std::cout << number3.real << std::endl;
	//std::cout << number3.imag << std::endl;
	
	//Use define function instead
	//Use '.' instead of '::' in c++??
	number1.print();
	number2.print();
	number3.print();
	return 0;
}

