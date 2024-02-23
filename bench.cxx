#include <iostream>
#include <chrono>
using namespace std;

int main() {

      
  // sum of two numbers in stored in variable sumOfTwoNumbers

    int i=0;
    int j=0;
    long int length=100000;
        
  
    double* array{ new double[length]{} };

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    
    for (i=0;i<length;i++) {
        array[i]=i;
    }


    for (j=0;j<10000;j++) {
    for (i=0;i<length;i++) {
        array[i]=array[i]*2;
    }}

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

    std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << "[ms]" << std::endl;
    //std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count() << "[ns]" << std::endl;

    
  // prints sum 
  //cout << first_number << " + " <<  second_number << " = " << sum;     

  return 0;
}
